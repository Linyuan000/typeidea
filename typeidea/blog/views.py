from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None

#     # if tag_id:
#     #     try:
#     #         tag = Tag.objects.get(id=tag_id)
#     #     except Tag.DoesNotExist:
#     #         post_list=[]
#     #     else:
#     #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) #过滤掉草稿和已删除文章
#     # else:
#     #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL) #status=1
#     #     if category_id:
#     #         try:
#     #             category = Category.objects.get(id=category_id)
#     #         except Category.DoesNotExist:
#     #             category = None
#     #         else:
#     #             post_list = Post.objects.filter(category_id=category_id) #会去找此分类下的所有文章
    
    
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id) #使用model自定义方法
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()

#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     } 
#     context.update(Category.get_navs()) #传递一个字典，把字典内容更新到Context中
#     return render(request, 'blog/list.html', context=context) #注意templates的路径


# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
#     # return HttpResponse('ok')


#class-based view最难理解的地方在于不了解底层逻辑,感觉自己什么代码都没写,只需要配置,其他的Django就帮你做完了,所以逻辑有些晦涩,之后要再看
class CommonViewMixin: #导航和侧边栏的基础数据
    def get_context_data(self, **kwargs): #用来获取上下文数据并传入模板中
        context = super().get_context_data(**kwargs) #当IndexView继承时,它去继承了ListView的context?
        context.update({
            'sidebars': SideBar.get_all(),
        }) 
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView): #首页数据 ListVIew获取多条数据
    queryset = Post.latest_posts()
    paginate_by = 5 #分页功能,每页5个
    context_object_name = 'post_list' #如果不设置这一项, 在模板中要使用object_list变量
    template_name = 'blog/list.html'


class CategoryView(IndexView): #分类列表页
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id') #self.kwargs的数据是从URL里拿到的
        category = get_object_or_404(Category, pk=category_id) #获取对象的实例,不存在抛404
        context.update({
            'category': category,
        })
        return context
    
    def get_queryset(self): #用来获取指定model或者Queryset数据
        #重写queryset, 根据分类过滤
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView): #同上
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView): #DetailView只获取一条数据
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id' #这一项是干嘛用的?为什么可以不用self.kwargs?

    
    
    


