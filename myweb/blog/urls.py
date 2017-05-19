from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^register$', views.register, name="register"),
    url(r'^(?P<id>[\w-]+)/$', views.details, name="details"),
    url(r'^(?P<id>[\w-]+)/edit/$', views.blog_update, name="update"),
    url(r'^create$', views.article_create, name="create"),
    url(r'^blogs$', views.blogall, name="blogall"),
    url(r'^login$', views.user_login, name="login"),
    url(r'^logout$', views.user_logout, name="logout"),
    url(r'^myblog$', views.myblog, name="myblog"),
]
