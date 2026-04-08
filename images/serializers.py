from typing import Any

from PIL import Image
from rest_framework import serializers

from .models import Images


class ImageSerializer(serializers.ModelSerializer[Images]):
    class Meta:
        model = Images
        fields = ["id", "user", "image", "updated_at"]
        read_only_fields = ["id", "user", "updated_at"]

    def validate_image(self, value: Any):
        # 1. Custom Extension Validation (Optional extra check)
        valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        import os

        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension.")

        # 2. File Size Validation (e.g., limit to 2MB)
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise serializers.ValidationError("File too large. Size should not exceed 2MB.")

        return value


class ImageResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class ImageCropSerializer(ImageResizeSerializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()


class ImageFilterSerializer(serializers.Serializer):
    grayscale = serializers.BooleanField()
    sepia = serializers.BooleanField()


class ImageTransformationSerializer(serializers.Serializer):
    resize = ImageResizeSerializer(required=False)
    crop = ImageCropSerializer(required=False)
    rotate = serializers.IntegerField(required=False, min_value=0, max_value=360)
    format = serializers.CharField(required=False)
    image_filter = ImageFilterSerializer(required=False)

    def __init__(self, *args, **kwargs):
        # Extract the image instance to get metadata
        instance = kwargs.get("instance")
        if instance and hasattr(instance, "image"):
            with Image.open(instance.image.path) as img:
                width, height = img.size

            # Set initial values for the fields
            initial = kwargs.get("initial", {})
            initial.update(
                {
                    "resize": {"width": width, "height": height},
                    "crop": {"x": 0, "y": 0, "width": width, "height": height},
                    "format": img.format,
                }
            )
            kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # Access the image via self.instance to validate bounds
        if self.instance:
            with Image.open(self.instance.image.path) as img:
                orig_w, orig_h = img.size

            if "crop" in attrs:
                c = attrs["crop"]
                if (c["x"] + c["width"] > orig_w) or (c["y"] + c["height"] > orig_h):
                    raise serializers.ValidationError("Crop area is out of bounds.")
        return attrs

    def to_representation(self, instance):
        """
        This ensures that when you call serializer.data in a GET request,
        it actually populates the fields with the image metadata.
        """
        with Image.open(instance.image.path) as img:
            width, height = img.size

        return {
            "resize": {"width": width, "height": height},
            "crop": {"x": 0, "y": 0, "width": width, "height": height},
            "rotate": 0,
            "format": img.format,
            "image_filter": {"grayscale": False, "sepia": False},
        }
