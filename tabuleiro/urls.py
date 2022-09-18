from django import views
from django.urls import path

from . import views

app_name = 'tabuleiro'

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('reiniciar/<str:jogo>', views.reiniciar, name='reiniciar'),
    path('jogada/<str:btn>/<str:jogo>/<str:simbolo>', views.jogada, name='jogada'),
]