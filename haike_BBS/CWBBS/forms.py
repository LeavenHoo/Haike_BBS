# -*- encoding: utf-8 -*-
from django import forms
from .models import *
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category','summary','text')#想要表单显示什么就写什么

class BBS_userForm(forms.ModelForm):
    class Meta:
        model = BBS_user
        fields = ('user', 'signature','photo','fens_counts','experiences','photo')#想要表单显示什么就写什么

class BBS_userForm1(forms.Form):
        nickname=forms.CharField(label=u'昵称',required=False)
        signature=forms.CharField(label=u'签名',required=False,widget=forms.TextInput())
        password=forms.CharField(label=u'密码*',widget=forms.PasswordInput(),required=False)
        password_check=forms.CharField(label=u'确认密码*',required=False,widget=forms.PasswordInput(),)
        photo = forms.ImageField(label=u'头像',required=False)
        email = forms.EmailField(label=u'电子邮件',required=False)
        
        
class BBS_userprofileForm(forms.ModelForm):
    class Meta:
        model = BBS_user
        fields = ( 'signature','photo')#想要表单显示什么就写什么
    
class UserForm(forms.Form): #这里不能用forms.ModelForm，否则页面无法正常显示表单
#     class Meta:
#         model=User
#         fields = ('username', 'password')
        username = forms.CharField(label=u'用户名*',max_length=100,required=True)
        password = forms.CharField(label=u'密码*',widget=forms.PasswordInput(),required=True)
        password_check=forms.CharField(label=u'确认密码*',widget=forms.PasswordInput(),)
        nickname = forms.CharField(label=u'昵称*',required=True,widget=forms.TextInput(attrs={'class': 'nickname',}))
        email = forms.EmailField(label=u'电子邮件',required=False)
class CommentForm(forms.ModelForm):
    class Meta:
        model=Bbs_comment
        fields=('comment_content',)
        widgets = {
            'comment_content': forms.Textarea(attrs={'cols': 80, 'rows': 10,'placeholder':u'评论',}),
            }