"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.index, name="home"),
    # url(r'^register$', views.register, name="register"),
    # url(r'^blog/details$', views.details, name="details"),
    # url(r'^blog/blogs$', views.blogall, name="blogall"),
    # url(r'^login$', views.user_login, name="login"),
    # url(r'^logout$', views.user_logout, name="logout"),
    # url(r'^myblog$', views.myblog, name="myblog"),
    url(r'^blog/', include("blog.urls", namespace='blog')),
    url(r'^change-password$', auth_views.password_change,
        name="chang-password"
        ),
    url(r'^password-change-done$', auth_views.password_change_done,
        {'template_name': 'blog/password_change_done.html'},
        name="password_change_done"
        ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
