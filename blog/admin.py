from django.contrib import admin

# Register your models here.
from .models import Post
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','publish','status')
    list_filter=('title','body')
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=('status','publish')
    