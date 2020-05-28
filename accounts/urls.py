from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('create/', views.Create_account.as_view(), name='account_create'),
    path('login/', views.Account_login.as_view(), name='account_login'),
    path('logout/', views.Logout.as_view(), name='account_logout'),
]