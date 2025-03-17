from django.urls import path
from . import views 

urlpatterns = [ 
    #path('home', views.index, name='citizens-index'),

    #---------------------- CONTRACTS -----------------------
    path('contracts', views.contracts, name='contracts'),
    path('contracts/list', views.contracts_list, name='contracts-list'),
    path('contracts/search', views.contracts_search, name='contracts-search'),
    path('contracts/form', views.contracts_form, name='contracts-form'),
    path('contracts/remove', views.contracts_remove, name='contracts-remove'),
]

