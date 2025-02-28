from django.urls import path
from . import views 

urlpatterns = [ 
    path('home', views.index, name='citizens-index'),

    #---------------------- CITIZENS -----------------------
    path('citizens', views.citizens, name='citizens'),
    path('citizens/list', views.citizens_list, name='citizens-list'),
    path('citizens/search', views.citizens_search, name='citizens-search'),
    path('citizens/form', views.citizens_form, name='citizens-form'),
    path('citizens/remove', views.citizens_remove, name='citizens-remove'),


    #---------------------- COMPANIES -----------------------
    #path('companies', views.companies, name='companies'),
    #path('companies/list', views.companies_list, name='companies-list'),
    #path('companies/search', views.companies_search, name='companies-search'),
    #path('companies/form', views.companies_form, name='companies-form'),
    #path('companies/remove', views.companies_remove, name='companies-remove'),
]

