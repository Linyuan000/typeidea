from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin): #过滤当前用户数据
    
    def get_queryset(self, request): #控制所需要获取的对象,除超级用户外,只能看到自己创建的信息
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user #把owner字段设定为当前登录用户
        return super().save_model(request, obj, form, change) #python2的写法 super(CategoryAdmin, self)