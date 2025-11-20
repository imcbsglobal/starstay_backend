from rest_framework import serializers
from .models import Visitor, Showcase
from django.contrib.auth.models import User
from .models import Visitor, Showcase, Demonstration


# --------------------- VISITOR SERIALIZER ---------------------
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


# --------------------- USER REGISTRATION SERIALIZER ---------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )


# --------------------- SHOWCASE SERIALIZER ---------------------
class ShowcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showcase
        fields = [
            "id",
            "title",
            "description",
            "media_type",
            "media_file",
            "website_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        media_type = data.get("media_type", getattr(self.instance, "media_type", None))
        media_file = data.get("media_file", getattr(self.instance, "media_file", None))
        website_url = data.get("website_url", getattr(self.instance, "website_url", None))

        if media_type == "image" and not media_file:
            raise serializers.ValidationError("media_file is required for image type")

        if media_type == "video" and not website_url:
            raise serializers.ValidationError("website_url is required for video type")

        return data


class DemonstrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demonstration
        fields = [
            "id",
            "title",
            "description",
            "media_type",
            "media_file",
            "website_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        media_type = data.get("media_type", getattr(self.instance, "media_type", None))
        media_file = data.get("media_file", getattr(self.instance, "media_file", None))
        website_url = data.get("website_url", getattr(self.instance, "website_url", None))

        if media_type == "image" and not media_file:
            raise serializers.ValidationError("media_file is required for image type")

        if media_type == "video" and not website_url:
            raise serializers.ValidationError("website_url is required for video type")

        return data
