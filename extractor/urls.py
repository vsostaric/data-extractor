from django.urls import path

from extractor import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-file', views.index, name='indexsubmit'),
    path('get-filter-result', views.filter, name='filtersubmit'),
    path('file', views.file, name='filesubmit')
]
