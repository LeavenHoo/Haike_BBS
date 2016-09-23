# -*-coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404,render_to_response,HttpResponseRedirect,HttpResponse
from .models import *
from django.template.context_processors import request
from django.views.generic import RedirectView
from .forms import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import auth
from peutils import is_valid
from django.utils import timezone
import time
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger#分页
from django.views.decorators.cache import cache_page #缓存
from django.views.decorators.cache import cache_control#缓存更新
import json 
from django.http import JsonResponse
from upload import handle_uploaded_file
from django.conf import settings
from httplib2 import Response

# Create your views here.
category=Category.objects.all().order_by('-id')
def index(request):   
    posts_list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')#'-'是按降序排序，省略是按升序排列
    paginator = Paginator(posts_list, 5)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    #return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})
    return render_to_response('cwbbs/post_list.html', {'posts': posts, 'page':True,'user':request.user,'categories':category})

#@cache_page(60 * 5)
@cache_control(must_revalidate=True, max_age=600)
def post_detail(request,pk):
    '''
    遍历META字典

    values = request.session.items()
#     if request.session.has_key('permission')==False:
#         request.session['permission']='allow'
#     else:
#         request.session['permission']='not_allow'
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
    #print html
    '''
    
    
     
    is_author=0#初始化默认请求用户不是文章作者
    comments=Bbs_comment.objects.filter(post_id=pk,father_comment_id=0).order_by('create_time')#获取灵轮列表
    
    #print request.cookies
    if request.user.is_authenticated():#is_authenticated()必须要加括号，否则即使不登录也为TRUE
        #print "nimei"
        if int(User.objects.get(username=str(request.user.username)).id)==BBS_user.objects.get(id=Post.objects.get(id=pk).author_id).user.id:
            
            is_author=1
        else:
            #visitor_session=Session.objects.filter(pk= str(request.session.session_key ))
        
            if request.session.has_key('permission')==False:
                
                post=Post.objects.get(id=pk)
                post.views+=1
                experiences=BBS_user.objects.get(id=post.author_id).experiences
                BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+5)
                post.save()
                request.session['permission']='('+str(pk)+')'
                #print 11,request.session['permission']
            else:
                if '('+pk+')' in request.session['permission']:
                    #print 111,request.session['permission']
                    pass
                else:
                    #print 12,request.session['permission']
                    post=Post.objects.get(id=pk)
                    post.views+=1
                    if BBS_user.objects.filter(id=post.author_id):
                        experiences=BBS_user.objects.get(id=post.author_id).experiences
                        BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+1)
                    post.save()
                    request.session['permission']=request.session['permission']+'('+str(pk)+')'
                
    else:
        if request.session.has_key('permission')==False:
            
            post=Post.objects.get(id=pk)
            post.views+=1
            experiences=BBS_user.objects.get(id=post.author_id).experiences
            BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+1)
            post.save()
            request.session['permission']='('+str(pk)+')'
            #print 21,request.session['permission']
        else:
            if '('+pk+')' in request.session['permission']:
                pass
                #print 211,request.session['permission']
            else:
                #print 22,request.session['permission']
                post=Post.objects.get(id=pk)
                post.views+=1
                experiences=BBS_user.objects.get(id=post.author_id).experiences
                BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+1)
                post.save()
                request.session['permission']=request.session['permission']+'('+str(pk)+')'
                #print request.session['permission']
    post = get_object_or_404(Post, pk=pk)
    #category=Category.objects.all().order_by('-id')
    
   
#     sessionStore = SessionStore()
#     sessionStore["comment_judge"] = ""                  #  字串映射
#     sessionStore["dict"] = {};                     #  可以定义多级的字典结构
#     sessionStore["dict"]["key1"]="value1"
#     sessionStore["dict"]["key2"]="value2"
#     sessionStore.save();
#     print(sessionStore.session_key);
#     print(sessionStore.keys());
# 
    
#         if request.META['HTTP_ORIGIN']#获取用户访问的网站:
#             print request.META['HTTP_ORIGIN']
#         else:
#             print 'No'
#        print 'request.POST.get(r''next''):',request.POST.get('next')
    if request.method=='POST' :
        if request.user.is_authenticated():
            cf=CommentForm(request.POST)
            #print 'sessionStore.items()',sessionStore.items()
            if request.session.has_key('has_commented')==True:
            #if sessionStore.has_key('comment_judge'):
                if str(pk) in request.session['has_commented'].split(','):
                    masage=u'请勿重复提交评论'
                    return HttpResponseRedirect('/post/'+str(pk)+"?args1="+json.dumps(masage ))
                else:
                    if   cf.is_valid():
                        ct_post=cf.save(commit=False)
                        ct_post.user_id=BBS_user.objects.get(user_id=User.objects.get(username=str(request.user.username)).id).id
                        ct_post.post_id=pk
                        ct_post.create_time=timezone.now()
                        ct_post.comment_content=str(request.POST['comment_content'])
                        ct_post.save()
                        set_post=Post.objects.get(id=pk)          
                        set_post.comments_count+=1
                        set_post.save()

                        request.session['has_commented'] =request.session['has_commented']+ str(pk)+','
                        #session = Session.objects.get(pk=session_key)
                        #print session["comment_judge"]
                    return HttpResponseRedirect('/post/'+str(pk)+'/', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category})
        
            
            else:
                if   cf.is_valid():
                    ct_post=cf.save(commit=False)
                    
                    ct_post.user_id=User.objects.get(username=str(request.user.username)).id
                    ct_post.post_id=pk
                    ct_post.create_time=timezone.now()
                    ct_post.comment_content=str(request.POST['comment_content'])
                    ct_post.save()
                    set_post=Post.objects.get(id=pk)          
                    set_post.comments_count+=1
                    set_post.save()
                    request.session['has_commented'] = str(pk)+','
                    #print 'sessionStore',sessionStore["comment_judge"]
                    #comments=Bbs_comment.objects.filter(post_id=pk,father_comment_id=0)#重新刷新评论列表
                    #print 1
                    #print request.POST.tt
                    #cf.comment_content=''
                    cf=CommentForm()
                    return HttpResponseRedirect('/post/'+str(pk)+'/', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category})   
 
                     #return redirect(reverse('cwbbs.views.post_detail',request, args=[pk]))
                else:
                    #print 2
                    cf=CommentForm()
                    cf.comment_content='不合法'
                    return render_to_response('cwbbs/post_detail.html', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category},context_instance=RequestContext(request))
        else:
            cf=UserForm()
            masage=u'请登录后再评论'
            #print 122
            request.session['masage']=masage
            response = HttpResponseRedirect('/login/')
            return response

            #return redirect('cwbbs.views.login_view')
    else:
        #print 3
        cf=CommentForm() 
        return render_to_response( 'cwbbs/post_detail.html', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category},context_instance=RequestContext(request))
    #print 4
    cf=CommentForm()   
    return render_to_response( 'cwbbs/post_detail.html', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category},context_instance=RequestContext(request))

@cache_control(must_revalidate=True, max_age=600)
def post_list(request,pk):
    
    if (pk == '5'):
        posts_list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')#'-'是按降序排序，省略是按升序排列
    else:
        posts_list = Post.objects.filter(published_date__isnull=False,category=pk).order_by('-published_date')#'-'是按降序排序，省略是按升序排列
    #Bbs_comment.objects.filter(post_id=pk).order_by('create_time')
    paginator = Paginator(posts_list, 5)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    #return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})
    return render_to_response('cwbbs/post_list.html', {'posts': posts, 'page':True,'user':request.user,'categories':category})


@login_required
def post_delete(request,pk):
    #print request
    post = get_object_or_404(Post, pk=pk)
    comments=Bbs_comment.objects.filter(post_id=pk,father_comment_id=0)
    sub_comment_dict={}
    for comment in comments:
        sub_comemets=Bbs_comment.objects.filter(father_comment_id=comment.pk)
    if int(User.objects.get(username=str(request.user.username)).id)==int(Post.objects.get(id=pk).author_id):
         is_author=1
         experiences=BBS_user.objects.get(id=post.author_id).experiences
         BBS_user.objects.filter(id=post.author_id).update(experiences=experiences-5)
         post.delete()
         
         posts=Post.objects.filter(published_date__isnull=False).order_by('-published_date')
         return render(request, 'cwbbs/index.html', {'posts': posts,'categories':category})
    else:
         is_author=0
         
    cf=CommentForm()
    return render(request, 'cwbbs/post_detail.html', {'post': post,'cf':cf,'is_author':is_author,'comments':comments,'categories':category})
    
    
@login_required
def post_publish(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    #print dir(post)
    post.published_date=timezone.now()
    post.save()
    experiences=BBS_user.objects.get(id=post.author_id).experiences
    BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+5)
    return redirect('post_detail', pk=pk)

@login_required
def post_new(request):
    #print request.POST
    if request.user.is_authenticated():

        if request.method == "POST":
            form = PostForm(request.POST)
            #print dir(form)
            #print form
            if form.is_valid():
                post = form.save(commit=False)
                post.author = BBS_user.objects.get(user__username=request.user)
                print request.POST
                if request.POST.has_key('cancle'):
                    form = PostForm()
                    print 'cancle'
                    return redirect('index')
                elif request.POST.has_key('publish'):
                    #print type(post.published_date),post.published_date,"--",type(timezone.now)
                    
                    post.published_date=timezone.now() #必须加(),否则数据类型有问题，出现 expected string or buffer  错误
                    post.save()
                    print 'publish_new_post',post.author_id
                    #pk=post.id
                    experiences=BBS_user.objects.get(id=post.author_id).experiences
                    BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+5)
                    return redirect('post_detail', pk=post.pk)
                else:
                    #print type(post.published_date),post.published_date,"--",type(timezone.now)
                    print 'draft'
                    post.save()
                    return redirect('post_detail', pk=post.pk)
            else:
                return HttpResponse(u'输入不合法')   
                
        else:
            form = PostForm()
    form = PostForm()
    return render(request, 'cwbbs/post_new.html', {'form': form,'categories':category})

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    #print request.method
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        #print form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = BBS_user.objects.get(user__username=request.user)
            post.category_id=1
            if request.POST.has_key('cancle'):
                form = PostForm(instance=post)
                return redirect('post_detail', pk=post.pk)
            elif request.POST.has_key('publish'):
                #print type(post.published_date),post.published_date,"--",type(timezone.now)
                post.published_date=timezone.now() #必须加(),否则数据类型有问题，出现 expected string or buffer  错误
            #print 'detail'
                post.save()
            else:
                pass
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    #print 'edit'
    return render(request, 'cwbbs/post_edit.html', {'form': form,'post':post,'pk':pk,'categories':category})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True,author=BBS_user.objects.get(user=request.user )).order_by('-created_date')
    if posts:
        return render(request, 'cwbbs/post_draft_list.html', {'posts': posts,'categories':category})
    else:
        return render(request, 'cwbbs/post_draft_list.html', {'posts': posts,'categories':category})
   
def register(request):
    import re
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')#
    #一个小应用，判断一段文本中是否包含简体中：
    
    

    #curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());
    errors=""
    if request.method == "POST":
        uf = UserForm(request.POST) 
        post_uf=BBS_userForm1(request.POST,request.FILES)  
        print request.FILES   
        if uf.is_valid() and post_uf.is_valid():   
            #获取表单信息
            #print request.POST
            username_reg = request.POST['username']
            match = zhPattern.search(username_reg)
            if match:
                return render_to_response('cwbbs/register.html',{"errors":u'禁止中文登录名','uf':UserForm(),'puf':BBS_userForm1(),'categories':category},context_instance=RequestContext(request))
            password_reg = request.POST['password']
            password_check = request.POST['password_check']
            nickname_reg = request.POST['nickname']
            email_reg=request.POST['email']
            photo_reg=post_uf.cleaned_data['photo']
            upload_img=handle_uploaded_file(photo_reg,username_reg)
            user_exists=BBS_user.objects.filter(nickname=nickname_reg)
            if user_exists:
                uf = UserForm()
                return render_to_response('cwbbs/register.html',{"errors":u'昵称'+nickname_reg+'已存在，请换一个注册','uf':uf,'puf':BBS_userForm1(),'categories':category},context_instance=RequestContext(request))

            print nickname_reg
            if password_reg != password_check:
                print password_reg,password_check
                return render_to_response('cwbbs/register.html',{"errors":u'前后密码不一致','uf':UserForm(),'puf':BBS_userForm1(),'categories':category},context_instance=RequestContext(request))

#             if request.POST['email']:
#                 emai_reg = request.POST['email']
#             else:
#                 emai_reg=''
            
            filterResult = User.objects.filter(username = username_reg)
            if filterResult:
                return render_to_response('cwbbs/register.html',{"errors":u'用户名已存在','uf':UserForm(),'puf':BBS_userForm1(),'categories':category},context_instance=RequestContext(request))
            else:
                #email = uf.cleaned_data['email']
                #返回注册成功页面
                user = User.objects.create_user(username=username_reg, password= password_reg,email=email_reg,is_staff=1)
                author=BBS_user.objects.create(user=user,nickname=nickname_reg,photo='static/cwbbs/images/'+str(upload_img))#创建一对一关系的外键
                user_login=authenticate(username=username_reg, password=password_reg)
                login(request, user_login)
                request.session['login_from'] = request.META.get('HTTP_REFERER')
                return render_to_response('cwbbs/success.html',{'username':user_login.username,'last_url':request.session['login_from']},context_instance=RequestContext(request))
                #return HttpResponseRedirect('/login.html')
                #return render_to_response('cwbbs/success.html',{'username':username_reg},context_instance=RequestContext(request))
        else:
             #print 'uf.is_unvalid'
             uf = UserForm()
             return render_to_response('cwbbs/register.html',{"errors":u'输入不全或不合法','uf':uf,'puf':BBS_userForm1(),'categories':category},context_instance=RequestContext(request))

    else:
         uf = UserForm()
    return render_to_response('cwbbs/register.html',{'uf':uf,'puf':BBS_userForm1(),"errors":'','categories':category},context_instance=RequestContext(request))   
    
#登陆
def login_view(request):
    #c = {}
    #c.update(csrf(request))
#     if request.REQUEST.has_key('masage'):
#         masage=request.REQUEST['masage']
#         print 'masage',masage
#     else:
    if request.session.has_key('masage'):
        masage=request.session['masage']   
        request.session.pop('masage') 
    else:
        masage=''
    if request.user.is_authenticated():
        return redirect('index')
    else:
        errors= []  
        account=None  
        password=None  
        if request.method == 'POST' :  
            if not request.POST.get('account',''):  
                errors.append(u'未输入正确账号')  
            else:  
                account = request.POST.get('account','')  
            if not request.POST.get('password',''):  
                errors.append(u'未输入正确密码')  
            else:  
                password_req= request.POST.get('password','')  
            if account is not None and password_req is not None : 
                user = authenticate(username=account, password=password_req)
                if user is not None :  
                    if user.is_active:  
                        login(request,user)  
                         
                        #print "yes"
                        return redirect('/category/5/')
                        # return HttpResponseRedirect('/')  
                    else:  
                        errors.append('账号被禁用')  
                else :  
                    errors.append('无效账号')  
        #return render_to_response('cwbbs/login.html', {'errors': errors})  
    return render(request,'cwbbs/login.html',{'errors': errors,'categories':category,'masage':masage},context_instance=RequestContext(request))

#退出
def logout(request):
    auth.logout(request)
    response = HttpResponse('logout !!')
    #print 'logout'
    #清理cookie里保存username
    response.delete_cookie('username')
    return redirect(index)

@login_required
@cache_control(must_revalidate=True, max_age=600)
def user_profile(request,pk):
    #print 'user_profile'
    #print request.user.username
    #is_myself=1 if (User.objects.get(username=request.user.username).id=pk) else 0
    if request.user.is_authenticated(): 
        is_authenticated=True 
    else: 
        is_authenticated=False
    user=get_object_or_404(User, pk=pk)
    author=BBS_user.objects.get(user__username=str(request.user))
    author_level=author.user_level
    posts=Post.objects.filter(author=author).order_by('-published_date')
    #print user
    #user = get_object_or_404(BBS_user, user_id=pk)
    #author=get_object_or_404()
    #print str(user.username),pk

    if request.method == "POST":
        #print settings.STATIC_URL
        puf = BBS_userForm1(request.POST,request.FILES)
        #print request.POST
        if puf.is_valid():
            post_user=BBS_user.objects.get(user__username=request.user)
            #print request.user,post_user
            nickname_req=puf.cleaned_data['nickname']
            signature_req=puf.cleaned_data['signature']
            password_req=puf.cleaned_data['password']
            password_check=puf.cleaned_data['password_check']
            email_req=puf.cleaned_data['email']
            photo_req=puf.cleaned_data['photo']
            if post_user:
                #print 'post_user'
                
                if nickname_req:
                    #print 'nickname_req'
                    post_user.nickname=nickname_req
                if signature_req:
                    #print 'signature_req'
                    post_user.signature=signature_req
                if email_req:
                    #print 'password_req'
                    user=User.objects.get(username=request.user)
                    user.email=email_req
                    user.save()
                if photo_req:
                    #print 'photo_req'
                    upload_img=handle_uploaded_file(photo_req,request.user.username)
                    post_user.photo='static/cwbbs/images/'+str(upload_img)
                if password_req and password_req==password_check:
                    #print 'password_req'
                    user=User.objects.get(username=request.user)
                    user.set_password(password_req)
                    user.save()
                    user_login=authenticate(username=user.username, password=password_req)
                    login(request,user_login)
                    #print 'photo,change'
               
                #print  'result:',post_user,photo_req,upload_img
                    
                    
                
                post_user.save()
                puf=BBS_userForm1()
                return HttpResponseRedirect('/user/'+pk+'/')
        else:
            return  HttpResponse("not valid")
        puf=BBS_userForm1()
        return render(request, 'cwbbs/user_profile.html', {'user': user,'puf':puf,'author':author,'posts':posts,'is_authenticated':is_authenticated,'categories':category})
    else:
        puf = BBS_userForm1()
    return render(request, 'cwbbs/user_profile.html', {'user': user,'puf':puf,'author':author,'posts':posts,'is_authenticated':is_authenticated,'categories':category})


@login_required()
def user_detail(request,pk):
    #print request.user
    author=get_object_or_404(BBS_user, id=pk)
  # author=BBS_user.objects.get(id=pk)
    user1=User.objects.get(id=author.user_id)
    posts=Post.objects.filter(author=author).order_by('-published_date')
    #print user.id ,User.objects.get(username=request.user).id
    if request.user.is_authenticated():
        if User.objects.get(username=request.user).id==user1.id:
            return redirect('user_profile',pk=user1.id)
    return render(request, 'cwbbs/user_detail.html', {'user1': user1,'author':author,'posts':posts,'categories':category})
    
@login_required    
def comment(request,pk):
    if request.method=="POST":
        cf=CommentForm(request.post)
        
@login_required        
def post_comment(request):
    if request.method=="POST":
        print request.POST
        #cf=CommentForm(request.post)
        return JsonResponse(1)
 
@login_required        
def comment_usefulornot(request,pk):
    print comment_usefulornot,pk,request.POST['post_id']
    #statue字段说明：0为未定义，1为作者接受，2为访客接受，3为访客拒绝
    if request.POST['who_click']=='is_author':
        if request.user.is_authenticated():
            user_id_req=BBS_user.objects.get(user=request.user).id
            statue_req=comment_statue.objects.filter(post_id=request.POST['post_id'],statue=1)
        if statue_req:
            #print 'repeat'
            comment_post_user_accept=Bbs_comment.objects.get(id=pk).post_user_accept
            masage=u'请勿重复采纳'
            useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
            print 'useful_count',useful_count,pk
            unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
            post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1).count()
            if post_user_accept:
                post_user_accept=1
            else:
                post_user_accept=0
            data = {
                  'useful_count':useful_count,
                  'unuseful_count':unuseful_count,
                  'post_user_accept':post_user_accept,
                  'masage': masage #将[models.Model]->[dict]
                  }
            #json_data = json.dumps(data)
            #print 'www',post_praise
            return HttpResponse(json.dumps(data),content_type='application/json')
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
    #         pass
        else:
            #print 232
            
            comment_statue.objects.create(user=BBS_user.objects.get(user=request.user),post_id=request.POST['post_id'],comment_id=pk,statue=1)

            #更新评论信息  
            comment_s=Bbs_comment.objects.get(id=pk)
            comment_s.post_user_accept=1
            comment_s.save()

            comment_author_id=Bbs_comment.objects.get(id=pk).user_id
            experiences=BBS_user.objects.get(id=comment_author_id).experiences
            BBS_user.objects.filter(id=comment_author_id).update(experiences=experiences+2)
            #post_praise=Post.objects.get(id=pk).praise
            useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
            unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
            post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1).count()
            if post_user_accept:
                post_user_accept=1
            else:
                post_user_accept=0
            data = {
                  'useful_count':useful_count,
                  'unuseful_count':unuseful_count,
                  'post_user_accept':post_user_accept,
                  }
            return HttpResponse(json.dumps(data),content_type='application/json')
    
    #处理访客POST
    elif request.POST['who_click']=='is_visitor': 
            
        if request.user.is_authenticated():
            user_id_req=BBS_user.objects.get(user=request.user).id
            statue_req=comment_statue.objects.filter(comment_id=pk,user_id=user_id_req)
            #print User.objects.get(username=request.user).id,Bbs_comment.objects.get(id=pk).user_id
            if User.objects.get(username=request.user).id==Bbs_comment.objects.get(id=pk).user_id:
                #comment_post_user_accept=Bbs_comment.objects.get(id=pk).statue
                masage=u'无法采纳 or 拒绝自己的评论'
                print masage
                useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
                unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
                post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1)
                if post_user_accept:
                    post_user_accept=1
                else:
                    post_user_accept=0
                print 'useful_count',useful_count
                data = {
                      'useful_count':useful_count,
                      'unuseful_count':unuseful_count,
                      'post_user_accept':post_user_accept,
                      'masage': masage #将[models.Model]->[dict]
                      }
                #json_data = json.dumps(data)
                #print '请勿重复接受或拒绝'
                return HttpResponse(json.dumps(data),content_type='application/json')
                
            #print pk,user_id_req
            if statue_req:
                #print 'repeat'
                #comment_post_user_accept=Bbs_comment.objects.get(id=pk).post_user_accept
                masage=u'请勿重复采纳或拒绝'
                useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
                unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
                print 'unuseful_count111:',unuseful_count,pk
                post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1).count()
                if post_user_accept:
                    post_user_accept=1
                else:
                    post_user_accept=0
                data = {
                      'useful_count':useful_count,
                      'unuseful_count':unuseful_count,
                      'post_user_accept':post_user_accept,
                      'masage': masage #将[models.Model]->[dict]
                      }
                #json_data = json.dumps(data)
                print '请勿重复采纳或拒绝'
                return HttpResponse(json.dumps(data),content_type='application/json')
            else:
                #print 232
                if request.POST['statue']=='is_useful':
                    comment_statue.objects.create(user=BBS_user.objects.get(user=request.user),comment_id=pk,post_id=request.POST['post_id'],statue=2)
                elif  request.POST['statue']=='is_unuseful':  
                    comment_statue.objects.create(user=BBS_user.objects.get(user=request.user),comment_id=pk,post_id=request.POST['post_id'],statue=3)    
                else:
                    useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
                    unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
                    post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1).count()
                    if post_user_accept:
                        post_user_accept=1
                    else:
                        post_user_accept=0
                    data = {
                          'useful_count':useful_count,
                          'unuseful_count':unuseful_count,
                          'post_user_accept':post_user_accept,
                          'masage':u'无效的输入'+request.POST['statue']
                          }
                    return HttpResponse(json.dumps(data),content_type='application/json')
            #print pk,request.path   
            comment_s=Bbs_comment.objects.get(id=pk)
            #comment_s.post_user_accept=True
#             comment_s.post_id=request.POST['post_id']
#             comment_s.save()
            useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
            unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
            if request.POST['statue']=='is_useful':
                Bbs_comment.objects.filter(id=pk).update(useful_counts=useful_count)
            else:
                Bbs_comment.objects.filter(id=pk).update(unuseful_counts=unuseful_count)
            comment_author_id=Bbs_comment.objects.get(id=pk).user_id
            print 'comment_author_id:',comment_author_id
            experiences=BBS_user.objects.get(id=comment_author_id).experiences
            BBS_user.objects.filter(id=comment_author_id).update(experiences=experiences+1)

            #post_praise=Post.objects.get(id=pk).praise
            #useful_count=comment_statue.objects.filter(comment_id=pk,is_useful=1).count()
            #unuseful_count=comment_statue.objects.filter(comment_id=pk,is_useful=0).count()
            post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1)
            if post_user_accept:
                post_user_accept=1
            else:
                post_user_accept=0
            data = {
                  'useful_count':useful_count,
                  'unuseful_count':unuseful_count,
                  'post_user_accept':post_user_accept,
                  }
            return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        useful_count=comment_statue.objects.filter(comment_id=pk,statue=2).count()
        unuseful_count=comment_statue.objects.filter(comment_id=pk,statue=3).count()
        post_user_accept=comment_statue.objects.filter(comment_id=pk,statue=1)
        if post_user_accept:
            post_user_accept=1
        else:
            post_user_accept=0
        data = {
              'useful_count':useful_count,
              'unuseful_count':unuseful_count,
              'post_user_accept':post_user_accept,
              }
        return HttpResponse(json.dumps(data),content_type='application/json')   
        
        
#@login_required        
def praise(request,pk): 
    #print  request.POST
    if request.POST.has_key('p_praise'):
        if request.user.is_authenticated():
            user_id_req=User.objects.get(username=request.user).id
            praise_req=Praise_post.objects.filter(p_post_id=pk,user_id=user_id_req)
        else:
            somebody=User.objects.get(username='somebody')#前提是创建了somebody用户
            #print 1.1
            if Praise_post.objects.filter(user=somebody,p_post_id=pk,is_up=1,sessionid=request.session.session_key ):
                #print 1.2
                post_praise=Post.objects.get(id=pk).praise
                masage=u'请勿重复点赞'
                data = {
                      'post_praise':post_praise,
                      'masage': masage #将[models.Model]->[dict]
                      }
                #json_data = json.dumps(data)
                #print 'www',post_praise
                #Entry.objects.filter(blog__name='foo').update(comments_on=False)  #正确更新语法
                return HttpResponse(json.dumps(data),content_type='application/json')
            else:
                #request.session['praise_permission']  ='false'
                Praise_post.objects.create(user=User.objects.get(username='somebody'),p_post_id=pk,is_up=1,sessionid=request.session.session_key )
                praise_num=Post.objects.get(id=pk).praise+1
                #print pk,request.path   
                post=Post.objects.get(id=pk)
                post.praise+=1
                post.save()
                experiences=BBS_user.objects.get(id=post.author_id).experiences
                BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+1)
                #print 'save'
                post_praise=Post.objects.get(id=pk).praise
                data={'post_praise':post_praise}
                return HttpResponse(json.dumps(data),content_type='application/json')
#         if request.method == 'POST':
#             print 1
#             if request.POST.has_key('name'):
#                 print 'has_name'
#         else:
#             print 2
        if praise_req:
            #print 'repeat'
            post_praise=Post.objects.get(id=pk).praise
            masage=u'请勿重复点赞'
            data = {
                  'post_praise':post_praise,
                  'masage': masage #将[models.Model]->[dict]
                  }
            #json_data = json.dumps(data)
            #print 'www',post_praise
            return HttpResponse(json.dumps(data),content_type='application/json')
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
    #         pass
        else:
            #print 232
            Praise_post.objects.create(user=request.user,p_post_id=pk,is_up=True)
            praise_num=Post.objects.get(id=pk).praise+1
            #print pk,request.path   
            post=Post.objects.get(id=pk)
            post.praise+=1
            post.save()
            experiences=BBS_user.objects.get(id=post.author_id).experiences
            BBS_user.objects.filter(id=post.author_id).update(experiences=experiences+1)
            #print 'save'
    #         massage=u'点赞成功'
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
            #return HttpResponse ("点赞成功！")
    #     elif request.has_key("praise_comment"):
    #         pass
    #     elif request.has_key("praise_user"):
    #         pass
    #     else:
    #         pass
        post_praise=Post.objects.get(id=pk).praise
        data={'post_praise':post_praise}
        return HttpResponse(json.dumps(data),content_type='application/json')
    
    #处理对用户的赞--------------------------------------------------------------------
    elif request.POST.has_key("u_praise"):
        
        #print  author_id
        if request.user.is_authenticated():
            user_id_req=User.objects.get(username=request.user).id
            author_id=BBS_user.objects.get(user_id=pk).id
            praise_req=Praise_user.objects.filter(p_user_id=author_id,user_id=user_id_req)
#         else:
#             somebody=User.objects.get(username='somebody')#前提是创建了somebody用户
#             #print 1.1
#             if Praise_user.objects.exists(user=somebody,p_user_id=pk,is_up=1,sessionid=request.session.session_key ):
#                 #print 1.2
#                 user_praise=BBS_user.objects.get(id=author_id).praise
#                 masage=u'请勿重复点赞'
#                 data = {
#                       'user_praise':user_praise,
#                       'masage': masage #将[models.Model]->[dict]
#                       }
#                 #json_data = json.dumps(data)
#                 #print 'www',post_praise
#                 #Entry.objects.filter(blog__name='foo').update(comments_on=False)  #正确更新语法
#                 return HttpResponse(json.dumps(data),content_type='application/json')
#             else:
#                 #request.session['praise_permission']  ='false'
#                 Praise_user.objects.create(user=User.objects.get(username='somebody'),p_user_id=author_id,is_up=1,sessionid=request.session.session_key )
#                 praise_num=BBS_user.objects.get(id=author_id).praise+1
#                 print 'BBS_user',1
#                 user=BBS_user.objects.get(id=pk)
#                 print 'BBS_user',2
#                 user.praise+=1
#                 user.save()
#                 experiences=BBS_user.objects.get(id=author_id).experiences
#                 BBS_user.objects.filter(id=author_id).update(experiences=experiences+1)
#                 #print 'save'
#                 user_praise=BBS_user.objects.get(id=author_id).praise
#                 data={'user_praise':user_praise}
#                 return HttpResponse(json.dumps(data),content_type='application/json')
        if praise_req:
            
            #print 'repeat'
            user_praise=BBS_user.objects.get(id=author_id).praise
            masage=u'请勿重复点赞'
            data = {
                  'user_praise':user_praise,
                  'masage': masage #将[models.Model]->[dict]
                  }
            #json_data = json.dumps(data)
            #print 'www',post_praise
            return HttpResponse(json.dumps(data),content_type='application/json')
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
    #         pass
        else:
            print 232
            Praise_user.objects.create(user=request.user,p_user_id=author_id,is_up=True)
            praise_num=BBS_user.objects.get(id=author_id).praise+1
            #print pk,request.path   
            user=BBS_user.objects.get(id=author_id)
            user.praise+=1
            user.save()
            experiences=BBS_user.objects.get(id=author_id).experiences
            BBS_user.objects.filter(id=author_id).update(experiences=experiences+1)
            #print 'save'
    #         massage=u'点赞成功'
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
            #return HttpResponse ("点赞成功！")
    #     elif request.has_key("praise_comment"):
    #         pass
    #     elif request.has_key("praise_user"):
    #         pass
    #     else:
    #         pass
        user_praise=BBS_user.objects.get(id=author_id).praise
        data={'user_praise':user_praise}
        return HttpResponse(json.dumps(data),content_type='application/json')
    elif request.POST.has_key("c_praise"):
        if request.user.is_authenticated():
            user_id_req=User.objects.get(username=request.user).id
            praise_req=Praise_comment.objects.filter(p_comment_id=pk,user_id=user_id_req)
        else:
            somebody=User.objects.get(username='somebody')#前提是创建了somebody用户
            #print 1.1
            if Praise_comment.objects.exists(user=somebody,p_comment_id=pk,is_up=1,sessionid=request.session.session_key ):
                #print 1.2
                comment_praise=Bbs_comment.objects.get(id=pk).praise
                masage=u'请勿重复点赞'
                data = {
                      'comment_praise':comment_praise,
                      'masage': masage #将[models.Model]->[dict]
                      }
                #json_data = json.dumps(data)
                #print 'www',post_praise
                #Entry.objects.filter(blog__name='foo').update(comments_on=False)  #正确更新语法
                return HttpResponse(json.dumps(data),content_type='application/json')
            else:
                #request.session['praise_permission']  ='false'
                Praise_comment.objects.create(user=User.objects.get(username='somebody'),p_post_id=pk,is_up=1,sessionid=request.session.session_key )
                #praise_num=Bbs_comment.objects.get(id=pk).praise+1
                #print pk,request.path   
                comment=Bbs_comment.objects.get(id=pk)
                comment.praise+=1
                comment.save()
                experiences=BBS_user.objects.get(id=comment.user_id).experiences
                BBS_user.objects.filter(id=comment.user_id).update(experiences=experiences+1)
                #print 'save'
                comment_praise=Bbs_comment.objects.get(id=pk).praise
                data={'comment_praise':comment_praise}
                return HttpResponse(json.dumps(data),content_type='application/json')
        if praise_req:
            #print 'repeat'
            comment_praise=Bbs_comment.objects.get(id=pk).praise
            masage=u'请勿重复点赞'
            data = {
                  'comment_praise':comment_praise,
                  'masage': masage #将[models.Model]->[dict]
                  }
            #json_data = json.dumps(data)
            #print 'www',post_praise
            return HttpResponse(json.dumps(data),content_type='application/json')
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
    #         pass
        else:
            #print 232
            Praise_comment.objects.create(user=request.user,p_comment_id=pk,is_up=True)
            #praise_num=Post.objects.get(id=pk).praise+1
            #print pk,request.path   
            comment=Bbs_comment.objects.get(id=pk)
            comment.praise+=1
            comment.save()
            experiences=BBS_user.objects.get(id=comment.user_id).experiences
            BBS_user.objects.filter(id=comment.user_id).update(experiences=experiences+1)
            #print 'save'
    #         massage=u'点赞成功'
    #         return HttpResponse(json.dumps(massage), content_type='application/json')
            #return HttpResponse ("点赞成功！")
    #     elif request.has_key("praise_comment"):
    #         pass
    #     elif request.has_key("praise_user"):
    #         pass
    #     else:
    #         pass
        comment_praise=Bbs_comment.objects.get(id=pk).praise
        data={'comment_praise':comment_praise}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        pass
    #return HttpResponse ("嘛都没干！")