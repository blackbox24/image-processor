from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Images


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Images) -> bool:
        return obj.user == request.user
