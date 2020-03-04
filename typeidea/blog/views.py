from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category

# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list=[]
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) #过滤掉草稿和已删除文章
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL) #status=1
    #     if category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             post_list = Post.objects.filter(category_id=category_id) #会去找此分类下的所有文章
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    } 
    context.update(Category.get_navs()) #传递一个字典，把字典内容更新到Context中
    return render(request, 'blog/list.html', context=context) #注意templates的路径

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
    # return HttpResponse('ok')
