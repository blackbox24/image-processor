from django.urls import path

from . import views

urlpatterns = [
    path("",views.ListCreateImageView.as_view(), name="list_create_image_view"),
]
