from django.shortcuts import render, HttpResponse
# 玩玩
from django.http import JsonResponse
from django.contrib import auth
from rest_framework import status
from rest_framework.authentication import TokenAuthentication  # 权限认证
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin  # 通用视图类+mixins
from rest_framework.permissions import AllowAny, IsAuthenticated  # token认证
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, CreateAPIView, \
    DestroyAPIView  # 通用视图子类
# 玩玩
from django.views import View

# 比如我信要查询所有文章，我们就要views.py文件头部把文章表从数据模型导入
from .models import Article, Category, Banner, Tag, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 将视图重复的查询，添加到全局变量，然后在这里返回到locals()里面
def global_variable(request):
    allcategory = Category.objects.all()  # 导航上的分类
    remen = Article.objects.filter(tui_id=2)[:6]  # 查询推荐位ID为2的文章
    tags = Tag.objects.all()
    return locals()


# 首页
def index(request):
    banner = Banner.objects.filter(is_active=True)[0:4]  # 查询所有幻灯图数据，并进行切片
    tui = Article.objects.filter(tui__id=1)[:3]  # 查询推荐位ID为1的文章
    allarticle = Article.objects.all().order_by('-id')[0:10]
    # hot = Article.objects.all().order_by('?')[:10]#随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('-views')[:10]  # 通过浏览数进行排序
    link = Link.objects.all()
    # 这行不知道什么问题，输出是元组，非django.db.models.query.QuerySet，所以数据到不了模板，注释勿删
    # 找到原因了，不能有逗号：link = Link.objects.all(),有逗号的话会提取出为tuple
    context = {
        'banner': banner,  # 把查询到的幻灯图数据封装到上下文
        'tui': tui,  # 阅读
        'allarticle': allarticle,
        'hot': hot,
        'link': link,
    }
    return render(request, 'index.html', locals())


# 列表页
def list(request, lid):
    list = Article.objects.filter(category_id=lid).order_by('-created_time')
    # 需要添加order_by('-created_time')，否则没有排序，分页会报错
    cname = Category.objects.get(id=lid)
    page = request.GET.get('page', 1)
    # 这里不能用page = request.GET.get('page')会报错Paginator.page() should raise PageNotAnInteger when given a NoneType value
    pagintor = Paginator(list, 5)  # 将查询出的list分页，五条每页
    try:
        list = pagintor.page(page)  # 获取当前页码
    except Paginator:
        list = pagintor.page(1)  # 如果用户输入页码不是整数，显示第一页
    except EmptyPage:
        list = pagintor.page(pagintor.num_pages)  # 如果用户输入页数不在系统的页码伦，显示最后一页
    return render(request, 'list.html', locals())


# 内容页
def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category_id).last()
    # 比当前文章发布的时间小就是上一篇，比当前文章发布时间大就是下一篇
    # category=show.category.id，则是指定查询的文章为当前分类下的文章。
    show.views = show.views + 1  # 访问一次，浏览数+1
    show.save()
    return render(request, 'show.html', locals())


# 标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 通过文章标签进行查询
    tname = Tag.objects.get(name=tag)
    page = request.GET.get('page', 1)
    pagintor = Paginator(list, 5)
    try:
        list = pagintor.page(page)  # 获取当前页码
    except Paginator:
        list = pagintor.page(1)  # 如果用户输入页码不是整数，显示第一页
    except EmptyPage:
        list = pagintor.page(pagintor.num_pages)  # 如果用户输入页数不在系统的页码伦，显示最后一页
    return render(request, 'tags.html', locals())


# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss).order_by('-created_time')
    # title__icontain是忽略大小写
    # 获取关键字后，通过标题进行匹配
    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码记录
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果输入的页码数不在列表，显示最后一页
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    return render(request, 'page.html', locals())


class Login2(View):
    def get(self, request):
        return HttpResponse("GET 方法")

    def post(self, request):
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == "admin" and pwd == "123":
            return HttpResponse("POST 方法")
        else:
            return HttpResponse("POrtST 方法 1")


class LoginViewSet(APIView):
    '''登录获取token方法'''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse(data={"code": 401,
                                 "msg": "用户名或密码不对!"}, status=401)
        # 删除原有的Token
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        # 创建新的Token
        token = Token.objects.create(user=user)
        return JsonResponse({"code": 200,
                             "msg": "login success!",
                             "data": {"username": user.username, "token": token.key}
                             }, status=200)


class articleView(View):
    '''
    详情视图
    '''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户
    def get1(self, request):
        # 序列化展示全部数据
        art_list = Article.objects.all()
        serizlizers = ArticleSerializer(instance=art_list, many=True)
        return JsonResponse(serizlizers.data, safe=False)

    def get2(self, request, pk):
        # 序列化展示一条数据
        try:
            art = Article.objects.get(id=pk)
            serializer = ArticleSerializer(art, many=False)
            return JsonResponse(instance=serializer.data, safe=False, status=201)
        except Article.DoesNotExist:
            return HttpResponse({'message: 查询的数据不存在'}, status=404)


class articleAPI(APIView):
    '''
    APIView是REST framework提供的所有视图的基类，继承自Django的View父类。
    传入到视图方法中的是REST framework的Request对象，而不是Django的HttpRequeset对象；
    在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。
    '''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    def get(self, request, pk, format=None):
        if pk:
            try:
                art = Article.objects.get(id=pk)
                serializer = ArticleSerializer(art, many=False)
                # return JsonResponse(serializer.data, safe=False, status=201)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Article.DoesNotExist:
                return HttpResponse({'message: 查询的数据不存在'}, status=404)
        else:
            art = Article.objects.all()
            serializer = ArticleSerializer(art, many=True)
            return JsonResponse(serializer.data, safe=False, status=201)

    def post(self, request, format=None):
        verify_data = ArticleSerializer(data=request.data)  # 只改这里
        if verify_data.is_valid():
            verify_data.save()
            return JsonResponse({"code": "200", "message": "create some data!", "data": request.data})
        else:
            return JsonResponse(verify_data.errors)


class articleGenericAPIView(GenericAPIView):
    '''
    通用视图类GenericAPIView,继承自apiview.主要增加了操作序列化器和数据库查询的方法，作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时，可搭配一个或多个Mixin扩展类。
    serializer_class：指明视图使用的序列化器
    queryset： 指明使用的数据查询集
    '''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self, request):
        serializer = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200, data=serializer.data)


class articleGenericMixinAPIView(GenericAPIView, CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                                 DestroyModelMixin, UpdateModelMixin):
    '''
    GenericAPIView和视图扩展类Mixins进行代码的简写
    CreateModelMixin[添加一条数据]
    ListModelMixin[获取所有数据]
    RetrieveModelMixin[获取一条数据]
    DestroyModelMixin[删除一条数据]
    UpdateModelMixin[更新一条数据]
    '''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self, request):
        return self.list(request)

    

    def post(self, request):
        # 添加数据
        return self.create(request)


class article5GenericAPIView(CreateAPIView, ListAPIView, DestroyAPIView):
    '''
    GenericAPIView通用视图子类通用视图子类
    CreateAPIView 添加一条数据
    ListAPIView 获取所有数据
    UpdateAPIView 更新一条数据
    RetrieveAPIView 获取一条数据
    DestroyAPIView 删除一条数据
    RetrieveUpdateDestroyAPIView 获取一条数据 更新一条数据 删除一条数据
    '''
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    def get(self, request):
        return self.list(request)
