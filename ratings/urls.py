from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('modules/', views.modules, name='modules'),
    path('professors/ratings/', views.professors_ratings, name='professors_ratings'),
    path('professor/<str:professor_id>/module/<str:module_code>/', views.professor_rating_in_module, name='professor_rating_in_module'),
    path('rate/', views.rate, name='rate'),
]
