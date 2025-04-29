"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from ratings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ratings.urls')),  # 这里假设你的应用名是 'ratings'
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('modules/', views.modules, name='modules'),
    path('professors/ratings/', views.professors_ratings, name='professors_ratings'),
    path('professor/<str:professor_id>/module/<str:module_code>/', views.professor_rating_in_module, name='professor_rating_in_module'),
    path('rate/', views.rate, name='rate'),
]
