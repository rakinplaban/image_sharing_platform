from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import User,Role,Permission,Images,Categories,User_role,Role_permission,Image_category,Like
# Register your models here.
class images_display(admin.ModelAdmin):
    list_display = ("id","title","url","status","location","description")

class role_display(admin.ModelAdmin):
    list_display = ("id","name","status")

class categories_display(admin.ModelAdmin):
    list_display = ("id","name","slug")

class permission_display(admin.ModelAdmin):
    list_display = ("id","name","status","slug")

class User_display(admin.ModelAdmin):
    list_display = ("id","username","full_name","phone","address","email","status")

class Like_display(admin.ModelAdmin):
    list_display = ("id","user","image","timestamp")

class Image_cate_display(admin.ModelAdmin):
    list_display = ("id","images","category")

admin.site.register(User,User_display)
admin.site.register(Images,images_display)
admin.site.register(Role,role_display)
admin.site.register(Categories,categories_display)
admin.site.register(Permission,permission_display)
admin.site.register(Like,Like_display)
admin.site.register(User_role)
admin.site.register(Role_permission)
admin.site.register(Image_category,Image_cate_display)