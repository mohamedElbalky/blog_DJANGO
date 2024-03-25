from taggit.models import Tag

from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Comment, Post
from .forms import EmailPostForm, CommentForm, SearchForm


def post_list_view(request, tag_slug=None):
    post_qs = Post.objects.filter(status=Post.Status.PUBLISHED)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_qs = post_qs.filter(tags__in=[tag])

    posts_per_page = 3
    paginator = Paginator(post_qs, posts_per_page)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {"posts": posts, "tag": tag}
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

    # list similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)  # get tags IDs for each post
    similar_posts = Post.objects.filter(
        tags__in=post_tags_ids, status=Post.Status.PUBLISHED
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish_at"
    )  # sort similar posts by the number of tags

    # display add comment form
    comment_form = CommentForm()

    context = {
        "post": post,
        "comment_form": comment_form,
        "similar_posts": similar_posts,
    }

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

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())


def post_search_view(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            
            search_vector = SearchVector("title", "body")
            search_query = SearchQuery(query, config="english")
            
            results = (
                Post.objects.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query, status=Post.Status.PUBLISHED)
                .order_by("-rank")
            )

    context = {"form": form, "query": query, "results": results}
    return render(request, "blog/post/search.html", context)
