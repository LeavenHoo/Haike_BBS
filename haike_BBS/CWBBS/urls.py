# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail,name="post_detail"),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.post_comment, name='post_comment'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/draft/$', views.post_draft_list, name='post_draft'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_profile, name='user_profile'),
    url(r'^user/(?P<pk>[0-9]+)/detail/$', views.user_detail, name='user_detail'),
    #url(r'^user/(?P<pk>[0-9]+)/change/$', views.user_profile_change, name='user_profile_change'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.post_list, name='category'),
    url(r'^register/$',views.register,name = 'register'),
    url(r'^accounts/login/$',views.login_view,name = 'login'),#不知道是否会与admi的url冲突
    url(r'^login/$',views.login_view,name = 'login'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^delete/(?P<pk>[0-9]+)/$',views.post_delete,name = 'post_delete'),
    url(r'^praise/(?P<pk>[0-9]+)/$',views.praise,name = 'praise'),
    url(r'^comment_usefulornot/(?P<pk>[0-9]+)/$',views.comment_usefulornot,name = 'comment_usefulornot')
    
)