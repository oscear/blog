from django.db import models
# from stdimage.models import StdImageField
# from datetime import datetime
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField

# 导入Django自带用户模块

# Create your models here.
# 文章分类
class Category(models.Model):
    name = models.CharField(verbose_name='博客分类', max_length=100)
    index = models.IntegerField(verbose_name='分类排序', default=999)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签', max_length=100)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 推荐排行
class Tui(models.Model):
    name = models.CharField(verbose_name='推荐排行', max_length=100)

    class Meta:
        verbose_name = '推荐排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField(verbose_name='文章', max_length=100)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=False, null=False)
    # 使用外键关联分类表与分类是一对多关系
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 使用外键关系关联表和标签是多对多关系
    img = models.ImageField(upload_to='article_img/', verbose_name='文章图片', blank=True, null=True)
    # body = models.TextField(verbose_name='文章正文')
    body = UEditorField('内容', width=800, height=500,
                        toolbars="full", imagePath="upimg/", filePath="upfile/",
                        upload_settings={"imageMaxSize": 1204000},
                        settings={}, command=None, blank=True
                        )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    """
    文章作者，这里User是从django.contrib.auth.models导入的。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    """
    views = models.PositiveIntegerField(verbose_name='阅读量', default=0)
    tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 创建时间
    modified_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 更新时间

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# banner
class Banner(models.Model):
    text_info = models.CharField(verbose_name='标题', max_length=50, default='')
    img = models.ImageField(verbose_name='轮播图', upload_to='banner/')
    link_url = models.URLField(verbose_name='图片联接', max_length=200)
    is_active = models.BooleanField(verbose_name='是否是actice', default=False)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text_info


# 友情联接
class Link(models.Model):
    name = models.CharField(verbose_name='连接名称', max_length=20)
    linkurl = models.URLField(verbose_name='连接', max_length=100)

    class Meta:
        verbose_name = '友情连接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
# 友情联接
