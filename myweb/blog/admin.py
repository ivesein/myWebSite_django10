#-*- coding:utf-8 -*-
from django.contrib import admin

from .models import MyUser, Article

# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_login', 'score')


admin.site.register(MyUser, MyUserAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'publish', 'update')
    list_filter = ['publish'] 	# 添加发布日期的过滤器
    search_fields = ['content']		# 添加按内容搜索
    list_display_links = ['title']  # 将title设置为超链接
    # list_editable = ['title'] 将title字段设置为可编辑的


admin.site.register(Article, ArticleAdmin)
