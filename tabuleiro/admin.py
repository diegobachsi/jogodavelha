from django.contrib import admin

from .models import Jogos, Tabuleiro

class TabuleiroAdmin(admin.ModelAdmin):

    list_display = ['id_jogo', 'campos']
    search_fields = ['id_jogo', 'campos']

admin.site.register(Tabuleiro, TabuleiroAdmin)

class JogosAdmin(admin.ModelAdmin):

    list_display = ['id', 'jogador_one', 'jogador_two', 'modalidade', 'criado_em']
    search_fields = ['id', 'jogador_one', 'jogador_two', 'modalidade', 'criado_em']

admin.site.register(Jogos, JogosAdmin)