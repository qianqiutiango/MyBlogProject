from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

"""
我设置了3个表格：文章（Post）、分类（Category）以及标签（Tag），下面就来分别编写它们对应的Python类。
"""

class Category(models.Model):
    """
    Django的模型必须继承models.Model类
    在 Category 中只设置了一个字段 name(分类名)
    数据类型为 CharField ，即字符型，最大长度为100
    """
    name = models.CharField(max_length=100)
    # 通过内部类Meta来配置MODELS的一些特性
    class Meta:
        verbose_name = '分类'
        # plural为复数，中文没有区别
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    Tag 和 Category类似，有一个标签名字段（name）
    """

    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        # plural为复数，中文没有区别
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章设置了文章标题(title)，文章正文（body），文章创建时间(created_time)和修改时间(modified_time)，文章摘要（excerpt）
    以及引用的分类和标签
    """
    # 每一个Model都有一个save方法，这个方法包含了将model数据保存到数据库中的逻辑
    # 注意在指定完modified_time的值时，要调用父类的save以执行数据保存回数据库的逻辑



    # 为了方便的生成URL，定义一个get_absolute_url方法

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    # 文章标题，字符型，最大长度为70
    title = models.CharField('标题',max_length=70)

    # 文章正文，我们使用了 TextField，适合大段的文字
    body = models.TextField('正文')

    # 表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField('创建时间',default=timezone.now())
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要，可以没有，所以设置为非空
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField('摘要',max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey
    # 即一对多的关联关系。同时传入一个 on_delete 参数用来指定当关联的数据被删除时
    # 被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此
    # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。

    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签',blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和
    # Category 类似。
    # on delete设置为级联删除
    author = models.ForeignKey(User,verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0,editable=False)
    class Meta:
        verbose_name = '文章'
        # plural为复数，中文没有区别
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
# Create your models here.
