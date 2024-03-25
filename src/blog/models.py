from taggit.managers import TaggableManager

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone



class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, unique_for_date="publish_at")
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(default=timezone.now)
    # image = models.ImageField(upload_to='posts')

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish_at"]
        indexes = [
            models.Index(fields=["-publish_at"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse(
            "blog:post_detail",
            kwargs={
                "slug": self.slug,
                
                "year": self.publish_at.year,
                "month": self.publish_at.month,
                "day": self.publish_at.day,
                
                "hour": self.publish_at.hour,
                "minute": self.publish_at.minute,
                "second": self.publish_at.second,
            },
        )

class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post.title}'