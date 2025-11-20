from django.db import models
import os

# --------------------- VISITOR MODEL ---------------------
class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# --------------------- SHOWCASE MODEL ---------------------

def showcase_upload_path(instance, filename):
    return f"showcase/{filename}"

class Showcase(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    # FileField supports both images & videos.
    media_file = models.FileField(
        upload_to=showcase_upload_path,
        blank=True,
        null=True
    )

    # YouTube URL for video items
    website_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    def delete(self, *args, **kwargs):
        if self.media_file:
            if os.path.isfile(self.media_file.path):
                os.remove(self.media_file.path)
        super().delete(*args, **kwargs)


# Add this function before the Demonstration class
def demonstration_upload_path(instance, filename):
    return f"demonstrations/{filename}"

# Add this new model after Showcase model
class Demonstration(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    # For images
    media_file = models.FileField(
        upload_to=demonstration_upload_path,
        blank=True,
        null=True
    )

    # For YouTube videos
    website_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"

    def delete(self, *args, **kwargs):
        if self.media_file:
            if os.path.isfile(self.media_file.path):
                os.remove(self.media_file.path)
        super().delete(*args, **kwargs)