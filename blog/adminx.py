# from django.contrib import admin
#
# # Register your models here.
import xadmin
from xadmin import views
from .models import Banner, Category, Tag, Tui, Article, Link


class ThemeSetting(object):
    ''' 设置主题 '''
    enable_themes = True  # 使用主题
    use_bootswatch = True  ## bootswatch是一款基于bootstrap的汇集了多种风格的前端UI解决方案
    # user_theme: \
    #     [
    #         {
    #         'name': 'Cerulean',
    #         'css': 'https://bootswatch.com/3/cerulean/bootstrap.css'
    #         }
    #     ]


class GlobalSetting(object):
    """对后台管理标记信息进行命名，全局设置"""
    # 后台头部信息
    site_title = '博客后台管理'
    # 后台底部信息
    site_footer = '奥斯卡'
    # 左侧样式以下拉形式展开（折叠样式）
    menu_style = 'accordion'
    # 设置models的全局图标, Article, Category 为表名
    # 图标使用的这个地址：http://www.fontawesome.com.cn/
    global_search_models = [Article, Category]
    global_models_icon = {
        Article: "fa fa-pencil-square",
        Category: "fa fa-cloud",
        Banner: "fa fa-bath",
        Tag: "fa fa-tags",
        Link: "fa fa-link",
        Tui: "fa fa-flag"

    }


# @admin.register(object)
class ArticleAdmin(object):
    # list_display 定义显示列， search_fields表示搜索字段， list_filter表示筛选字段
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'created_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面
    # model_icon = 'fa fa-graduation-cap'
    # 表指定图标


class BannerAdmin(object):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')


class CategoryAdmin(object):
    list_display = ('id', 'name', 'index')


class TagAdmin(object):
    list_display = ('id', 'name')


class TuiAdmin(object):
    list_display = ('id', 'name')


class LinkAdmin(object):
    list_display = ('id', 'name', 'linkurl')

xadmin.site.register(views.BaseAdminView, ThemeSetting)  # 使用主题
xadmin.site.register(views.CommAdminView, GlobalSetting)  # 全局设置
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Tui, TuiAdmin)
xadmin.site.register(Link, LinkAdmin)
