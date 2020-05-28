from time import sleep

from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import CreateView, TemplateView
from .forms import UserCreateForm, LoginForm


# アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            # フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            # フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'create.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'create.html', {'form': form, })


# ログイン機能
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form, })


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'logout.html'

    """
    def get(self, request, *args, **kwargs):

        return render(request, 'index.html')
    """
