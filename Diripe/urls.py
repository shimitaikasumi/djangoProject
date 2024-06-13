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
    path('employeeinfchg_list/', views.employeeinfchg_list, name='employeeinfchg_list'),
    path('employeeinfchg_search/', views.employeeinfchg_search, name='employeeinfchg_search'),
    path('confirmation_re/', views.confirmation_re, name='confirmation_re'),
    path('confirmation_re/<int:empid>', views.confirmation_re, name='confirmation_re'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('confirmation_pat/', views.confirmation_pat, name='confirmation_pat'),
    path('confirmation_pat/<int:patid>', views.confirmation_pat, name='confirmation_pat'),
]