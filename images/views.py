import io

from django.db.models import QuerySet
from django.http import FileResponse
from PIL import Image, ImageOps
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Images
from .paginations import CustomPagination
from .permissions import IsOwnerPermission
from .serializers import ImageSerializer, ImageTransformationSerializer
from .rate_limiting import ImageTransFormationLimiter


class ListCreateImageView(ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    pagination_class = CustomPagination
    throttle_classes = (ImageTransFormationLimiter,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Images]:
        return Images.objects.filter(user=self.request.user.pk).prefetch_related()


class RetrieveUpdateDeleteImageView(RetrieveUpdateDestroyAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (
        IsAuthenticated,
        IsOwnerPermission,
    )
    throttle_classes = (ImageTransFormationLimiter, )
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    lookup_field = "id"


class ImageTransformationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsOwnerPermission,
    )
    serializer_class = ImageTransformationSerializer
    throttle_classes = (ImageTransFormationLimiter, )

    def get(self, request, id):
        try:
            image = Images.objects.get(id=id)
        except Images.DoesNotExist:
            return Response("Image does not exist", status=status.HTTP_404_NOT_FOUND)
        # This will now include the image's actual width/height in the 'initial' data
        self.check_object_permissions(request, image)
        serializer = ImageTransformationSerializer(instance=image)

        return Response(serializer.data)

    def post(self, request, id, *args, **kwargs):
        try:
            image = Images.objects.get(id=id)
        except Images.DoesNotExist:
            return Response("Image does not exist", status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, image)
        serializer = self.serializer_class(data=request.data, instance=image)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        img = Image.open(image.image.path)
        data = serializer.validated_data

        if "resize" in data:
            img = img.resize(
                (data["resize"]["width"], data["resize"]["height"]), Image.Resampling.LANCZOS
            )

        if "crop" in data:
            c = data["crop"]
            # crop(left, top, right, bottom)
            img = img.crop((c["x"], c["y"], c["x"] + c["width"], c["y"] + c["height"]))

        if "rotate" in data and data["rotate"] != 0:
            img = img.rotate(data["rotate"], expand=True)

        if "image_filter" in data:
            f = data["image_filter"]
            if f.get("grayscale"):
                img = ImageOps.grayscale(img)
            if f.get("sepia"):
                # Simple sepia implementation
                img = self._apply_sepia(img)

        # 3. Save to a memory buffer to return as a response
        # ... inside your post method after crop/resize ...

        if img.size[0] <= 0 or img.size[1] <= 0:
            return Response(
                {"error": "Transformation resulted in an empty image."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        buffer = io.BytesIO()
        img_format = data.get("format", img.format or "JPEG").upper()
        img.save(buffer, format=img_format)
        buffer.seek(0)

        return FileResponse(buffer, content_type=f"image/{img_format.lower()}")

    def _apply_sepia(self, img):
        # Convert to RGB if not already
        img = img.convert("RGB")
        width, height = img.size
        pixels = img.load()
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
        return img
