from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch

from .models import Comment, Post
from .forms import EmailPostForm, CommentForm


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
        Post.objects.prefetch_related(
            Prefetch("comments", queryset=Comment.objects.filter(active=True))
        ),
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish_at__year=year,
        publish_at__month=month,
        publish_at__day=day,
        publish_at__hour=hour,
        publish_at__minute=minute,
        publish_at__second=second,
    )
    
    comment_form = CommentForm()
    context = {"post": post, 'comment_form':comment_form}

    return render(request, "blog/post/detail.html", context)


def post_share_view(request, id):
    """
    Share post --> send it by Email
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        id=id,
    )
    form = EmailPostForm()
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_date = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_date['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n{clean_date['name']}'s comments: {clean_date['comments']}"

            send_mail(
                subject,
                message,
                "elbalky4@gmail.com",
                [clean_date["to"]],
                fail_silently=False,
            )
            sent = True
    context = {"form": form, "sent": sent, "post": post}
    return render(request, "blog/post/share.html", context)


@require_POST
def add_post_comment_view(request, post_id):
    """
    Comment on a post
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        id=post_id,
    )

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())