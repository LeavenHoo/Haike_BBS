# -*-coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from _tkinter import create
from _elementtree import Comment
from test.test_imageop import MAX_LEN
from django.template.defaultfilters import default
import south
from pip._vendor.pkg_resources import require
from django.conf import settings
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#from test.test_imageop import MAX_LEN
#from django.template.defaultfilters import default
# Create your models here.

class Category (models.Model):
    name=models.CharField(max_length=32,unique=True)
    #author=models.ForeignKey('BBS_user')
    def  __unicode__(self):
        return self.name

class BBS_user(models.Model):
    user=models.OneToOneField(User)#不能用ForeignKey
    nickname=models.CharField(max_length=16,unique=True)
    signature=models.CharField(max_length=128,default='This guy is too lazy to write anything here')
    praise=models.IntegerField(default=0)
    fens_counts=models.IntegerField(default=0)
    experiences=models.IntegerField(default=0)
    user_level=models.CharField(max_length=12,default='level1')
    photo=models.ImageField(upload_to=str(settings.MEDIA_ROOT),default=str(settings.MEDIA_ROOT)+"/default.jpg")
    def  __unicode__(self):
        return  self.user.username #传对象的话会出错
    
class Post(models.Model):
    author = models.ForeignKey(BBS_user)
    category=models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    # title=title.decode('utf-8')
    summary=models.TextField(max_length=300,blank=True, null=True)
    text = models.TextField()
    #image=models.ImageField(upload_to='photo')
    # test=text.decode('utf-8')
    
    views=models.IntegerField(default=0)
    type=models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    update=models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    ranking=models.IntegerField(default=0)
    praise=models.IntegerField(default=0)
    comments_count=models.IntegerField(default=0)
#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()
        #jiang'def  __str__(self)'改成'def  __unicode__(self)'以处理保存中文字符后出现的UnicodeEncodeError: 'ascii' codec can't encode characters 
    def  __unicode__(self):
        return self.title

    


class Bbs_comment(models.Model):
    user=models.ForeignKey(BBS_user)#不能用OneToOne
    post=models.ForeignKey(Post)
    comment_content=models.TextField(max_length=1000,default="",null=True)
    father_comment_id=models.IntegerField(null=False,default=False)
    create_time=models.DateTimeField(default=timezone.now)
    praise=models.IntegerField(default=0)
    useful_counts=models.IntegerField(default=0)
    unuseful_counts=models.IntegerField(default=0)
    post_user_accept=models.BooleanField(default=0)
    def __unicode__(self):
        return self.post.title
class Praise_user (models.Model):
    user=models.ForeignKey(User)
    p_user_id=models.IntegerField(default=0)
    is_up=models.BooleanField(default=False)
    sessionid=models.CharField(max_length=50,null=True)
    def __unicode__(self):
        return self.user__username
class Praise_post (models.Model):
    user=models.ForeignKey(User)
    p_post_id=models.IntegerField(default=0)
    is_up=models.BooleanField(default=False)
    sessionid=models.CharField(max_length=50,null=True)
    def __unicode__(self):
        return self.user__username   
class Praise_comment (models.Model):
    user=models.ForeignKey(User)
    p_comment_id=models.IntegerField(default=0)
    is_up=models.BooleanField(default=False)
    sessionid=models.CharField(max_length=50,null=True)
    def __unicode__(self):
        return self.user__username
class comment_statue (models.Model):
    user=models.ForeignKey(BBS_user)
    comment_id=models.IntegerField(default=0,null=True)
    post_id=models.IntegerField(default=0,null=True)
    statue=models.IntegerField(default=0)#0为未定义，1为作者接受，2为访客接受，3为访客拒绝


    def __unicode__(self):
        return self.comment_id                  