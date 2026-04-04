from django.db.models import QuerySet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Images
from .serializers import ImageSerializer
from .permissions import IsOwnerPermission


class ListCreateImageView(ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    queryset = Images.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Images]:
        return Images.objects.filter(user=self.request.user.pk).prefetch_related()


class RetrieveUpdateDeleteImageView(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated, IsOwnerPermission,)
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    lookup_field = "id"
