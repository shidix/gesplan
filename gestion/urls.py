#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.urls import path
from . import views, auto_views, operation_views, import_views

urlpatterns = [ 
    path('home', views.index, name='index'),

    #---------------------- COMPANIES -----------------------
    path('companies', views.companies, name='companies'),
    path('companies/list', views.companies_list, name='companies-list'),
    path('companies/search', views.companies_search, name='companies-search'),
    path('companies/form', views.companies_form, name='companies-form'),
    path('companies/remove', views.companies_remove, name='companies-remove'),

    #---------------------- FACILITIES -----------------------
    path('facilities', views.facilities, name='facilities'),
    path('facilities/list', views.facilities_list, name='facilities-list'),
    path('facilities/search', views.facilities_search, name='facilities-search'),
    path('facilities/form', views.facilities_form, name='facilities-form'),
    path('facilities/remove', views.facilities_remove, name='facilities-remove'),

    path('facilities/items', views.facilities_items, name='facilities-items'),
    path('facilities/items-add', views.facilities_items_add, name='facilities-items-add'),
    path('facilities/items-return', views.facilities_items_return, name='facilities-items-return'),
    path('facilities/items-remove', views.facilities_items_remove, name='facilities-items-remove'),

    #---------------------- TRUCKS -----------------------
    path('trucks', views.trucks, name='trucks'),
    path('trucks/list', views.trucks_list, name='trucks-list'),
    path('trucks/search', views.trucks_search, name='trucks-search'),
    path('trucks/form', views.trucks_form, name='trucks-form'),
    path('trucks/remove', views.trucks_remove, name='trucks-remove'),

    #---------------------- ROUTES -----------------------
    path('routes', views.routes, name='routes'),
    path('routes/list', views.routes_list, name='routes-list'),
    path('routes/view', views.routes_view, name='routes-view'),
    path('routes/search', views.routes_search, name='routes-search'),
    path('routes/form', views.routes_form, name='routes-form'),
    path('routes/remove', views.routes_remove, name='routes-remove'),

    #---------------------- EMPLOYEES -----------------------
    path('employees', views.employees, name='employees'),
    path('employees/list', views.employees_list, name='employees-list'),
    path('employees/search', views.employees_search, name='employees-search'),
    path('employees/form', views.employees_form, name='employees-form'),
    path('employees/save', views.employees_save, name='employees-save'),
    path('employees/remove', views.employees_remove, name='employees-remove'),
    path('employees/items', views.employees_items, name='employees-items'),
    path('employees/items-add', views.employees_items_add, name='employees-items-add'),
    path('employees/items-return', views.employees_items_return, name='employees-items-return'),
    path('employees/items-remove', views.employees_items_remove, name='employees-items-remove'),
    path('employees/contracts', views.employees_contracts, name='employees-contracts'),
    path('employees/contracts-add', views.employees_contracts_add, name='employees-contracts-add'),
    path('employees/contracts-remove', views.employees_contracts_remove, name='employees-contracts-remove'),

    #---------------------- ITEMS -----------------------
    path('items', views.items, name='items'),
    path('items/list', views.items_list, name='items-list'),
    path('items/search', views.items_search, name='items-search'),
    path('items/form', views.items_form, name='items-form'),
    path('items/remove', views.items_remove, name='items-remove'),

    #---------------------- OPERATION -----------------------
    path('operation/index', operation_views.index, name='operation-index'),
    path('operation/facility-waste', operation_views.facility_waste, name='operation-facility-waste'),

   #---------------------- IMPORT -----------------------
    path('import', import_views.import_db, name='import'),
    path('import-db', import_views.import_db_file, name='import-db'),

    #---------------------- AUTO -----------------------
    path('autosave_field/', auto_views.autosave_field, name='autosave_field'),
    path('autoremove_obj/', auto_views.autoremove_obj, name='autoremove_obj'),
]

