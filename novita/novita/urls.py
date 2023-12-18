"""
URL configuration for novita project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from catalog import views
from django.contrib.auth.views import LoginView, LogoutView
# from .views import BaseRegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('news/', include('catalog.urls')),
    path('news_add/', views.news_add, name="news_add"),
    path('create/', views.create, name="create"),
    path('editl/<int:id>/', views.editl, name='editl'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('person/', views.IndexView.as_view(), name='person'), # страница зарегистрированного
    path('login/', LoginView.as_view(template_name = 'login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'),
         name='logout'),
    path('signup/', views.BaseRegisterView.as_view(template_name = 'signup.html'), # регистрация
         name='signup'),
]

urlpatterns +=[
    path('accounts/', include('django.contrib.auth.urls')),
]