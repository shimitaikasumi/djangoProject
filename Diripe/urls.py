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
    path('employeeinfchg_list/', views.employeeinfchg_list, name='employeeinfchg_list'),
    path('employeeinfchg_search/', views.employeeinfchg_search, name='employeeinfchg_search'),
    path('confirmation_re/', views.confirmation_re, name='confirmation_re'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('patient_listr/', views.patient_listr, name='patient_listr'),
    path('confirmation_pat/', views.confirmation_pat, name='confirmation_pat'),
    path('patient_expired/', views.patient_expired, name='patient_expired'),
    path('patient_search/', views.patient_search, name='patient_search'),
    path('add_drug/', views.add_drug, name='add_drug'),
    path('error_page/', views.error_page, name='error_page'),
    path('drug_selection/', views.drug_selection, name='drug_selection'),
    path('treatment_confirmed/', views.treatment_confirmed, name='treatment_confirmed'),
    path('patient_pasthistory/', views.patient_pasthistory, name='patient_pasthistory'),
    path('deletion_drug/', views.deletion_drug, name='deletion_drug'),
    path('patient_search2/', views.patient_search2, name='patient_search2'),
]