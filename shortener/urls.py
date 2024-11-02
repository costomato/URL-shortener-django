from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shorten', views.shorten, name='shorten'),
    path('<str:suffix>', views.visit, name='visit')
]
