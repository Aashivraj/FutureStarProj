"""FutureStar_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import *
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    
    #User List URL
    path('User/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/edit/', UserEditView.as_view(), name='user_edit'),
    path('users/<int:user_id>/update/', UserEditView.as_view(), name='user_update'),
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),
    
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/create/', RoleCreateView.as_view(), name='role_create'),
    path('roles/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('roles/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('System-Settings/', System_Settings.as_view(),name="System_Settings"),


    #error
    path('error/', ErrorView.as_view(), name='error'),

    path('home/', Dashboard.as_view(),name="home"),





]
