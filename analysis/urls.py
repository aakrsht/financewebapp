from django.urls import path
from .views import file_upload_view, data_visualization, visualization_page

urlpatterns = [
    path('upload/', file_upload_view, name='file_upload'),
    path('data_visualization/', data_visualization, name='data_visualization'),
    path('visualization/', visualization_page, name='visualization_page'),
]
