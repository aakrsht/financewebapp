
from django.urls import path
from . import views

app_name = 'encryptor'

urlpatterns = [
    path('', views.encryptor_view, name='encryptor'),
    path('download/<path:path>/', views.download_file, name='download'),
    path('actual_download/<path:path>/', views.actual_download, name='actual_download'),
]
