from django.urls import path

from create_csv_files.views import *

urlpatterns = [
    path('data_schemas/', data_schemas, name='load'),
    path('data_sets/', data_sets, name='sets'),
    path('delete_schema/<int:idd>/', delSchema, name='del')
]
