from django.urls import path

from .views import *

urlpatterns = [
    path('', user_login, name='home'),
    path('new_schema/', new_schema, name="schema"),
    path('data_schemas/', data_schemas),
    path('data_sets/', data_sets, name='sets'),
    path('logout/', user_logout, name="logout"),
    path('new_schema/edit/<str:_id>/', edit_schema, name="edit"),
    path('new_schema/edit/<str:_id>/delete/<str:id_child>/', delete_column)
]
