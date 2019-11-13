from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from django.views.decorators.http import require_POST

from .forms import CommentForm
# 该函数被require_POST装饰器装饰，作用是限制这个视图只能通过POST请求触发
# 因为创建评论需要用户通过表单提交的数据，而提交表单通常都是POST请求，这样更安全

@require_POST
def comment(request,post_pk):
    # 先获取被评论的文章，因为需要把评论和文章关联起来
    # 我们使用了get_object_or_404
    # 这个函数的作用是当获取的文章Post存在时，则获取，否则返回404
    post = get_object_or_404(Post,pk=post_pk)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        return  redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误
    # 注意到这里被评论的文章post也传给了模板，因为我们需要根据post来生成表单的提交地址
    context = {
        'post':post,
        'form':form,
    }

    return render(request,'comments/preview.html',context=context)
# Create your views here.
