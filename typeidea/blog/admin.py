from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user #把owner字段设定为当前登录用户
        return super().save_model(request, obj, form, change) #python2的写法 super(CategoryAdmin, self)
    
    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = [] #加入'category', 'status'时,字段变成超链接,可以跳转
    
    list_filter = ['category', ] #list_filter = ('category',)
    search_fields = ['title', 'category__name']

    # actions_on_top = True #action操作栏的位置(top是默认)
    # actions_on_bottom = True
    date_hierarchy = 'created_time' #显示创建时间
    #编辑页面
    # save_on_top = True #save操作栏位置

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    # filter_vertical = ('tag',)
    # filter_horizontal = ('tag',) 多对多关系的插件效果

    def operator(self, obj): #自定义编辑按钮
        return format_html( #html的格式
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,)) #admin自定义名字
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
