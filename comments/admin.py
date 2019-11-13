from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    # Comment列表页展示的数据
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    # 需要提交的表单数据
    fields = ['name', 'email', 'url', 'text', 'post']

admin.site.register(Comment, CommentAdmin)
# Register your models here.
