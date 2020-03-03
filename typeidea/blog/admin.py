from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostadminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
# Register your models here.


# class PostInline(admin.TabularInline): #StackedInline样式不同 
#     fileds = ('title', 'desc')
#     extra = 1
#     model = Post


@admin.register(Category, site=custom_site) #定制site
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    # inlines = [PostInline, ] #在分类中可以编辑文章

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user #把owner字段设定为当前登录用户
    #     return super().save_model(request, obj, form, change) #python2的写法 super(CategoryAdmin, self)
    
    def post_count(self, obj):
        return obj.post_set.count() #查看一下post_set的用法
    
    post_count.short_description = '文章数量'

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter): #自定义过滤器值展示当前用户分类

    title = '分类过滤器'
    parameter_name = 'owner_category' #定义查询时URL参数的名字

    def lookups(self, request, model_admin): #返回要展示的内容和查询用的id
        return Category.objects.filter(owner=request.user).values_list('id', 'name') #使用values显示的是字典名name

    def queryset(self, request, queryset): #根据URL Query的内容返回列表页的数据 
        category_id = self.value() #拿到的是owner_category后的id
        if category_id:
            return queryset.filter(category_id) #queryset可以直接调用接口?
        return queryset

@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostadminForm
    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    list_display_links = [] #加入'category', 'status'时,字段变成超链接,可以跳转
    
    list_filter = [CategoryOwnerFilter] #list_filter = ('category',)
    search_fields = ['title', 'category__name'] #__搜索关联model的数据

    # actions_on_top = True #action操作栏的位置(top是默认)
    # actions_on_bottom = True
    date_hierarchy = 'created_time' #显示创建时间
    #编辑页面
    # save_on_top = True #save操作栏位置
    #exclude = ('owner',) 不显示owner

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            # 'description':'基础配置描述', #在基础配置下添加描述
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',), #设置为折叠状态
            'fields': ('tag', ),
        })
    )
    
    # filter_vertical = ('tag',)
    # filter_horizontal = ('tag',) 多对多关系的插件效果

    def operator(self, obj): #自定义编辑按钮
        return format_html( #html的格式
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,)) #admin自定义名字
        )
    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)

    # def get_queryset(self, request): #控制所需要获取的对象,除超级用户外,只能看到自己创建的信息
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(owner=request.user)
    
    # class Media: #加载Javascript和CSS资源(使用时后台页面会出bug,可能是版本问题,之后再测试)
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

@admin.register(LogEntry, site=custom_site) #操作日志
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

    def get_queryset(self, request): #这种方法只能禁止一般用户访问,如何不把操作日志展示给一般用户?
        if request.user.is_superuser:
            return super().get_queryset(request)
        