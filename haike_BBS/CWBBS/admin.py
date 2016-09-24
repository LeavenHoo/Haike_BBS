# -*-coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import  models
# Register your models here.
from .models import *
#from django_comments.models import Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','published_date','ranking','praise')
class Bbs_commentAdmin(admin.ModelAdmin):
    list_display = ('comment_content','create_time','useful_counts','unuseful_counts','post_user_accept')
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('author','title','published_date','ranking','praise')
#     
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('author','title','published_date','ranking','praise')   
    
admin.site.register(Post,PostAdmin)
admin.site.register(BBS_user)
admin.site.register(Category)
admin.site.register(Bbs_comment,Bbs_commentAdmin)
#admin.site.register(Comment)