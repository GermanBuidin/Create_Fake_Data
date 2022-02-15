from django.conf.urls.static import static
from django.urls import path

from create_csv_files.views import del_schema, download_files, list_schemas
from main_catalog import settings

urlpatterns = [
    path('data_schemas/', download_files, name='load'),
    path('list_schemas/', list_schemas, name='sets'),
    path('delete_schema/<str:document_id>/', del_schema, name='del')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)