from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path

from home import views

app_name = 'home'
urlpatterns = [
    path('', views.index_page, name='home'),
]