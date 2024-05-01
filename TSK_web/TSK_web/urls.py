"""
URL configuration for TSK_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from TSKsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:stat>/', views.profile, name='profile'),
    path('project_creation/', views.project_creation, name='project_creation'),
    path('project_detail/<str:stat>/<str:project_id>/', views.project_detail, name='project_detail'),
    path('update_task_cond/<int:task_id>/', views.update_task_cond, name='update_task_cond'),
    path('complaints', views.complaints, name='complaints'),
    path('create_complaint', views.create_complaint, name='create_complaint'),
    path('complaint_answer/<int:complaint_id>', views.complaint_answer, name='complaint_answer')
]
