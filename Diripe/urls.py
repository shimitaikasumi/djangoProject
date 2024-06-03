from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('admin/', views.admin_home, name='admin'),
    path('')
]