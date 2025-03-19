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

    #---------------------- LOTS -----------------------
    path('contracts/lots/<int:obj_id>', views.contracts_lots, name='contracts-lots'),
    path('contracts/lots/list', views.contracts_lots_list, name='contracts-lots-list'),
    path('contracts/lots/form', views.contracts_lots_form, name='contracts-lots-form'),
    path('contracts/lots/remove', views.contracts_lots_remove, name='contracts-lots-remove'),
    path('contracts/lots/upload', views.contracts_lots_upload, name='contracts-lots-upload'),
    path('contracts/lots/file-remove', views.contracts_lots_file_remove, name='contracts-lots-file-remove'),

]

