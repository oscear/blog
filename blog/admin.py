# from django.contrib import admin
#
# # Register your models here.
from blog import models
from django.contrib import admin
from .models import Banner, Category, Tag, Tui, Article, Link

admin.site.site_header = '奥斯卡'   # 后台显示
admin.site.site_title = 'Blog'     # 网站名称

# 导入需要管理的数据库表
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'tui', 'user', 'views', 'created_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面
    search_fields = ('category__name', 'title')
    # 搜索功能
    list_filter = ('created_time',)
    #界面右侧过滤器
    #fields = ['category', 'title']
    # 自定义编辑表单
    fieldsets = [('文章信息', {'fields': ['title', 'excerpt', 'body', 'img']}),
                 ('标签分类', {'fields': ['category', 'tags', 'tui']}),
                 ('作者信息', {'fields': ['user', 'views']})
                 ]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'linkurl')

# admin.site.register(models.Article)
