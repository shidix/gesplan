from django.urls import path
from . import views 

urlpatterns = [ 
    path('home', views.index, name='index'),

    #---------------------- COMPANIES -----------------------
    #path('companies', views.companies, name='companies'),
    #path('companies/list', views.companies_list, name='companies-list'),
    #path('companies/search', views.companies_search, name='companies-search'),
    #path('companies/form', views.companies_form, name='companies-form'),
    #path('companies/remove', views.companies_remove, name='companies-remove'),
]

