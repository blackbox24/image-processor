from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .serializers import ImageSerializer


class ListCreateImageView(ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
