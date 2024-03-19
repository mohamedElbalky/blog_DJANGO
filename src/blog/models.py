from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'  
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(default=timezone.now)
    # image = models.ImageField(upload_to='posts')
    
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    class Meta:
        ordering = ["-publish_at"]
        indexes = [
            models.Index(fields=["-publish_at"]),
        ]
        

    def __str__(self):
        return self.title
