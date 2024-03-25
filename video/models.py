from django.db import models
from cloudinary.models import CloudinaryField



# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = CloudinaryField(resource_type='video')
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.video and not self.video_url:  # Check if video is uploaded and video_url is not set
            print(self.video)  # Print the secure URL of the uploaded video
            self.video_url = self.video  # Set video_url to the secure URL of the uploaded video
        super().save(*args, **kwargs)  # Call the superclass's save method to save the object to the database

    def __str__(self):
        return self.title