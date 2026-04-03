from rest_framework import serializers

from .models import Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["user", "image", "updated_at"]
        read_only_fields = ["user", "updated_at"]

    def validate_image(self, value):
        # 1. Custom Extension Validation (Optional extra check)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension.")

        # 2. File Size Validation (e.g., limit to 2MB)
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise serializers.ValidationError("File too large. Size should not exceed 2MB.")

        return value