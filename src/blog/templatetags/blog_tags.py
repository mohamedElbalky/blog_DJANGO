from django import template
from django.db.models import Count

from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    """
    simple_tag: Processes the given data and returns a string
    """
    return Post.objects.filter(status=Post.Status.PUBLISHED).count()


@register.inclusion_tag("blog/post/latest_psots.html")
def show_latest_posts(count=3):
    """
    inclusion_tag: Processes the given data and returns a rendered template
    """
    latest_posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by(
        "-publish_at"
    )[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.objects.filter(status=Post.Status.PUBLISHED).annotate(total_commented=Count("comments")).order_by(
        "-total_commented",
        "publish_at"
    )[:count]
