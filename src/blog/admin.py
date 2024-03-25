from django.contrib import admin

from .models import Post, Comment



class PostComment(admin.StackedInline):
    model = Comment
    extra = 1


    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'is_published', 'publish_at','status']
    list_editable = ['is_published', 'status']
    list_filter = ['is_published', 'publish_at','status', 'created_at']
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_at']
    date_hierarchy = "publish_at"
    
    prepopulated_fields  = {'slug': ('title',)}
    raw_id_fields = ['author']
    inlines = [PostComment]
