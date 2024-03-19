from django.shortcuts import get_object_or_404, render


from .models import Post


def post_list_view(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/post/list.html", context)


def post_detail_view(request, id=None):
    post = get_object_or_404(Post, id=id)
    context = {"post": post}
    
    return render(request, "blog/post/detail.html", context)