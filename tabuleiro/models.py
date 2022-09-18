from datetime import datetime
from random import randrange
from django.db import models

class Tabuleiro(models.Model):

    id_jogo = models.CharField(max_length=50)
    campos = models.CharField(max_length=1)

class Jogos(models.Model):

    jogador_one = models.CharField(max_length=255)
    jogador_two = models.CharField(max_length=255)
    modalidade = models.CharField(max_length=2)
    vencedor = models.CharField(max_length=255, default="Partida não finalizada")
    criado_em =  models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.id}'




