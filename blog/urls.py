from django.urls import path

from . import  views
"""
我们首先从 django.urls 导入了 path 函数，
又从当前目录下导入了 views 模块。
然后我们把网址和处理函数的关系写在了 urlpatterns 列表里。

"""
# 通过app_name高速django这个urls.py模块属于blog应用，这叫做视图函数命名空间
app_name = 'blog'
urlpatterns = [
    # 绑定关系的写法是把网址和对应的处理函数作为参数传给path函数
    # 第一个参数是网址，第二个参数是处理函数
    # name是处理函数index的别名

    path('',views.index,name='index'),
    # 这条规则的含义是，以posts/开头，后跟一个整数，并且以/结尾，如posts/1/，此外
    # 这里的<int:pk>是django路由匹配规则的特殊写法，其作用是从用户访问的URL里
    # 把匹配到的数字捕获并作为关键字参数传给detail函数。比如用户访问
    # posts/255/时，<int:pk>匹配255，那么这个255会在调用视图函数detail时被传递进去
    # 实际上函数调用形式为：detail(request,pk=255)
    path('posts/<int:pk>/',views.detail,name = 'detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>/', views.tag, name='tag')
]