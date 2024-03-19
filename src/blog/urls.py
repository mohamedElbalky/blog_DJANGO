from django.urls import path


from . import views


app_name = 'blog'


urlpatterns = [
    path('posts/', views.post_list_view, name="post_list"),
    path('posts/<id>/', views.post_detail_view, name="post_detail"),
]
