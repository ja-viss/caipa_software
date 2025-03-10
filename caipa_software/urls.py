"""system_caipa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from caipa import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('new/', views.signup),
    path('profile/', views.profile, name='profile_users'),
    path('profile/create/', views.create),
    path('delete/<int:ced_id>/', views.delete, name='delete_estu'),
    path('profile/create/new/', views.create_estudiante2, name='create_estu'),
    path('complete/', views.search, name='search_estu'),
    path('complete/newedit/', views.update, name='update_estu'),
    path('pdf_stu/', views.search_pdf, name='pdf_stu'),
    path('pdf_stu/agender/', views.agender, name='agender_cite'),
    path('pdf_stu/print_pdf/', views.render_to_pdf, name='pdf_stu'),
    path('sigin/', views.sigin, name='sigin'),
    path('validate/', views.validate, name='validate_per'),
    path('register/', views.register_stu, name='register_stu'),



]
