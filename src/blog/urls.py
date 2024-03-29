from django.urls import path


from . import views


app_name = "blog"


urlpatterns = [
    path("posts/", views.post_list_view, name="post_list"),
    path(
        "posts/tag/<slug:tag_slug>/", views.post_list_view, name="post_list_by_tag"
    ),  # list posts by tags
    path(
        "posts/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<slug:slug>/",
        views.post_detail_view,
        name="post_detail",
    ),
    path("posts/<int:id>/share/", views.post_share_view, name="post_share"),
    path(
        "posts/<int:post_id>/comment/add/",
        views.add_post_comment_view,
        name="add_post_comment",
    ),
    path("posts/search/", views.post_search_view, name="post_search"),
]
