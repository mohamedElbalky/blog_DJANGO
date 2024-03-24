from django.shortcuts import get_object_or_404, render


from .models import Post


def post_list_view(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    context = {"posts": posts}
    return render(request, "blog/post/list.html", context)


def post_detail_view(request, year, month, day, hour, second, minute, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        
        publish_at__year=year,
        publish_at__month=month,
        publish_at__day=day,
        
        publish_at__hour=hour,
        publish_at__minute=minute,
        publish_at__second=second,
        
    )
    context = {"post": post}

    return render(request, "blog/post/detail.html", context)
