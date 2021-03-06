from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
    choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者') 
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_navs(cls):
        catogories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in catogories: #用if判断减少数据库访问的I/O操作
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

    def __str__(self): #如果不修改, Post的fields展示这个字段的时候会显示object对象
        return self.name
    

    class Meta:
        verbose_name = verbose_name_plural = '分类' #后台展示字段

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
    choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = verbose_name_plural = '标签'
    
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=225, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, 
    choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=2)


    @staticmethod
    def get_by_tag(tag_id): #根据标签id查找标签和文章(把复杂的view抽离成单独的函数)
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
            # 返回带有外键关系的QuerySet,以后使用外键关系不需要再次做数据库查询
        return post_list, tag
    
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, category
    
    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)
        
    
    @classmethod
    def hot_posts(cls): #可以用only只展示title和id字段
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
        

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] #根据id降序排列
     

    