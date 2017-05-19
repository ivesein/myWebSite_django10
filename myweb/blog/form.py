# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Article
# from .models import MyUser


def lowercase_email(emial):
    lower_email = emial
    return lower_email.lower()


class SignupForm(forms.ModelForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'placeholder': '3-15位字母汉字或数字'})
    # )
    # emial = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={'placeholder': '请填写正确的邮箱地址'})
    # )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': '密码长度至少为6位'})
    )
    conf_password = forms.CharField(
        label='确认密码',
        required=True, max_length=30,
        min_length=6,
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码不能超过30个字',
            'min_length': '密码不能少于6位'
        },
        widget=forms.PasswordInput(
            attrs={'placeholder': '请再次输入密码,确保与上次输入一至'})
    )

    class Meta:
        model = get_user_model()
        # model = MyUser
        fields = [
            'username',
            'password',
            'email'
        ]

    # def clean_username(self):
    #     # cleaned_data = super(SignupForm, self).clean()
    #     usermodel = get_user_model()
    #     username = self.cleaned_data.get("username")
    #     try:
    #         usermodel._default_manager.get(username=username)
    #     except usermodel.DoesNotExist:
    #         return username
    #     raise forms.ValidationError("该用户名已被占用")

    def clean_email(self):
        # cleaned_data = super(SignupForm, self).clean()
        usermodel = get_user_model()
        email = self.cleaned_data.get("email")
        lower_email = lowercase_email(email)
        try:
            usermodel._default_manager.get(email=lower_email)
        except usermodel.DoesNotExist:
            return lower_email
        raise forms.ValidationError("该邮箱已被人使用")

    def clean_conf_password(self):
        password = self.cleaned_data.get("password", False)
        conf_password = self.cleaned_data.get("conf_password")
        if not (password == conf_password):
            raise forms.ValidationError("两次输入的密码不一致")
        return conf_password


class LoginForm(forms.Form):
    # class Meta:
    #     model = get_user_model()
    #     fields = ['username', 'password']
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']
