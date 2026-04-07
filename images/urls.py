from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreateImageView.as_view(), name="list_create_image_view"),
    path("<int:id>/", views.RetrieveUpdateDeleteImageView.as_view(), name="rud_image_view"),
    path("<int:id>/transform/",views.ImageTransformationView.as_view(), name="transform_image_view"),
]
