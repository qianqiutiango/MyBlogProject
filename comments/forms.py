from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        # 表明使用的数据库Model是Comment
        model = Comment
        # 表示表单需要显示的字段
        fields = ['name', 'email', 'url', 'text']