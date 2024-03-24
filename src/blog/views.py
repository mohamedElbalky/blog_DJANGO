from django.shortcuts import get_object_or_404, render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def post_list_view(request):
    post_qs = Post.objects.filter(status=Post.Status.PUBLISHED)
    
    posts_per_page = 3
    paginator = Paginator(post_qs, posts_per_page)
    page_number = request.GET.get("page", 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
