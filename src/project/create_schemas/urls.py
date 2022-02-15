from django.urls import path

from .views import *

urlpatterns = [
    path('', user_login, name='home'),
    path('new_schema/', create_new_schema, name="schema"),
    path('logout/', user_logout, name="logout"),
    path('new_schema/edit/<str:document_id>/', edit_schema, name="edit"),
    path('new_schema/edit/<str:document_id>/delete/<str:id_row>/', delete_column)
]
