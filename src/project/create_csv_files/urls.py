from django.conf.urls.static import static
from django.urls import path

from create_csv_files.views import *
from proj import settings

urlpatterns = [
    path('data_schemas/', data_schemas, name='load'),
    path('data_sets/', data_sets, name='sets'),
    path('delete_schema/<str:idd>/', del_schema, name='del')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)