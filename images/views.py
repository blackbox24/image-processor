from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Images
from .paginations import CustomPagination
from .permissions import IsOwnerPermission
from .serializers import ImageSerializer, ImageTransformationSerializer


class ListCreateImageView(ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    pagination_class = CustomPagination

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
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    lookup_field = "id"


class ImageTransformationView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerPermission, )
    serializer_class = ImageTransformationSerializer

    def post(self, request, id, *args, **kwargs):
        try:
            image = Images.objects.get(id=id)
        except Images.DoesNotExist:
            return Response("Image does not exist",status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)