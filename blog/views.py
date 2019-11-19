from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from .models import Post,Category,Tag
import markdown
import re

def index(request):
    # -created_time表示逆序，不加-则表示正序
    posts = Post.objects.all().order_by('-created_time')
    # 每页显示4篇文章
    paginator = Paginator(posts,4)
    # 获取url中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给posts
    post_list = paginator.get_page(page)
    context = {'post_list': post_list}

    return render(request,'blog/index.html',context)

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    post.body = md.convert(post.body)
    # 使用正则表达式匹配，如果没有目录，则不显示
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request,'blog/detail.html',context={'post':post})

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    # 归档页面和首页展示文章的形式是一样的，因此直接复用了index
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
# Create your views here.
