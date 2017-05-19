# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect

from .form import SignupForm, LoginForm, ArticleForm

from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth import views as auth_views

from django.shortcuts import redirect

from django.contrib import messages
from .models import Article
# Create your views here.


def index(request):
    return render(request, "blog/index.html", {})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:home')
            else:
                messages.warning(request, "用户名或密码错,请重新输入!")
            # usermodel = get_user_model()
            # try:
            #     usermodel.objects.get(
            #         username=username, password=password)
            # except usermodel.DoesNotExist:
            #     messages.warning(request, "用户名或密码错误,请重新输入!")

            # else:
            #     auth_user = usermodel.objects.get(
            #         username=username, password=password)
            #     auth_login(request, auth_user)
            #     return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect('blog:home')


def register(request):
    # path = request.get_full_path()
    if request.method == 'POST':
        # data=request.POST
        # print data.get('username')
        form = SignupForm(data=request.POST, auto_id='%s')
        if form.is_valid():
            usermodel = get_user_model()
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = usermodel.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            # instance = form.save(commit=False)
            # instance.save()
            return redirect("blog:home")
    else:
        form = SignupForm(auto_id='%s')
    return render(request, 'blog/register.html', locals())


def details(request, id=None):
    instance = get_object_or_404(Article, id=id)
    context = {
        'author': instance.user,
        'image': instance.image,
        'title': instance.title,
        'content': instance.content,
        'publish': instance.publish,
        'update': instance.update,
        'id': instance.id
    }
    return render(request, 'blog/details.html', context)


def blogall(request):
    queryset = Article.objects.all()
    if queryset:
        context = {
            'objects': queryset,
        }
        return render(request, 'blog/blogall.html', context)
    else:
        raise Http404


# def myblogdetials(request):
#     username = request.user.username
#     instance = get_object_or_404(Article, user=username)
#     context = {
#         'author': instance.user,
#         'image': instance.image,
#         'title': instance.title,
#         'content': instance.content,
#         'publish': instance.publish,
#         'update': instance.update
#     }
#     return render(request, 'blog/myblog.html', context)

def myblog(request):
    userid = request.user.id
    print "userid:%s" % userid
    queryset = Article.objects.filter(user=userid)
    if not queryset:
        raise Http404
    else:
        context = {
            'objects_list': queryset,
        }
        return render(request, 'blog/myblog.html', context)


def blog_update(request, id=None):
    if not request.user.is_authenticated():
        messages.error(request, "您还没有登录,请登录后再进行编辑!")
        return redirect('blog:login')
    instance = get_object_or_404(Article, id=id)
    if request.user != instance.user:
        raise Http404

    form = ArticleForm(request.POST or None,
                       request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "您的博客更新成功!")
        # return redirect("blog:details")
    # return reverse("blog:details", kwargs={'id': instance.id})
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'blog/articleform.html', context)


def article_create(request):
    if not request.user.is_authenticated():
        messages.error(request, "请您登录后再发布文章!")
        return redirect('blog/login')
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "新文章发布成功!")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form
    }
    return render(request, 'blog/articleform.html', context)
