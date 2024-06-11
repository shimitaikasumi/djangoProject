from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('vendor_toroku/', views.vendor_toroku, name='vendor_toroku'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('vendor_search/', views.vendor_search, name='vendor_search'),
    path('empregistation/', views.empregistration, name='empregistation'),
    path('nachange_list/', views.nachange_list, name='nachange_list'),
    path('nachange_search/', views.nachange_search, name='nachange_search'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('confirmation/<int:empid>', views.confirmation, name='confirmation'),
]