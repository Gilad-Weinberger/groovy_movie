from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('actors/<str:actor_id>/', views.actor_detail, name='actor_detail'),
]
