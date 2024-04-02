from django.urls import path

from .views import * 

urlpatterns = [
    path('',  DeviceViewResults.as_view() ),
    path('seleciona-genero', seleciona_genero )
]
