from django.shortcuts import render
import random
from django.contrib import messages
from .models import Jogos, Tabuleiro

def index(request):

    template = 'inicio.html'

    context = {}

    opt = request.GET.get('opt')

    if opt == 'IA':
        context['opt'] = 'IA'
    if opt == 'x1':
        context['opt'] = 'x1'

    return render(request, template, context)


def iniciar(request):

    template = 'tabuleiro.html'

    context = {}

    #recebe os valores via POST
    jogador_one = request.POST['jogador_one']
    jogador_two= request.POST['jogador_two']
    if jogador_two == '':
        jogador_two = 'Robot'
    simbolo = request.POST['simbolo']
    modalidade = request.POST['modalidade']

    #grava o jogo
    jogo = Jogos(jogador_one=jogador_one, jogador_two=jogador_two, modalidade=modalidade)
    jogo.save()

    #recupera o último id de jogo
    id_jogo = Jogos.objects.latest('pk').pk

    #grava o tabuleiro do jogo
    for n in range(1, 10):
        tabuleiro = Tabuleiro(id_jogo=id_jogo, campos=n)
        tabuleiro.save()

    #criar uma matriz para contextualizar no template
    context['tabuleiro'] = [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]]

    #guarda o jogo e simbolo para contexto
    context['jogo'] = jogo
    context['simbolo'] = simbolo

    return render(request, template, context)


def reiniciar(request, jogo):

    template = 'tabuleiro.html'

    context = {}

    context = montar_tabuleiro(jogo)

    return render(request, template, context)

def jogada(request, btn, jogo, simbolo):

    template = 'tabuleiro.html'

    context = {}

    modalidade = Jogos.objects.filter(id=int(jogo)).values('modalidade')[0]['modalidade']

    if modalidade == 'IA':
        
        is_robot = True

        try:
            if int(btn):
                tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=btn)
                tabuleiro.update(campos=simbolo)
        except:
            is_robot = False

        if is_robot:
            vencedor = verifica_vencedor(request, jogo)
            if not vencedor:
                jogada_robot(jogo, simbolo)
            vencedor = verifica_vencedor(request, jogo)

        context = montar_tabuleiro(jogo)
        context['simbolo'] = simbolo
        if vencedor:
            context['vencedor'] = True

    else:
        tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=btn)
        tabuleiro.update(campos=simbolo)

        verifica_vencedor(request, jogo)

        context = montar_tabuleiro(jogo)

        if simbolo == 'X':
            context['simbolo'] = 'O'
        else:
            context['simbolo'] = 'X'

    return render(request, template, context)

def montar_tabuleiro(jogo):

    context = {}

    tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo).values('campos')

    matriz = []
    matriz.append([tabuleiro[n]['campos'] for n in range(3)])
    matriz.append([tabuleiro[n]['campos'] for n in range(3,6)])
    matriz.append([tabuleiro[n]['campos'] for n in range(6,9)])

    context['tabuleiro'] = matriz
    context['jogo'] = jogo

    return context

def jogada_robot(jogo, simbolo):

    if simbolo == 'X':
        simbolo_robot = 'O'
    else:
        simbolo_robot = 'X'

    campos = registrar_campos(jogo)

    if simbolo_robot == 'O':
        if campos[4] == 0:
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=5)
            tabuleiro.update(campos=simbolo_robot)
        elif campos.count(-1) == 1:
            campo = random.choice([1, 3, 7, 9])
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=campo)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[:3]) == 2:
            i = campos[:3].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[3:6]) == 2:
            i = campos[3:6].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+4)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[6:9]) == 2:
            i = campos[6:9].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+7)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::3]) == 2:
            i = campos[::3].index(0)
            if i == 0: i = 1
            elif i == 1: i = 4
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[1::3]) == 2:
            i = campos[1::3].index(0)
            if i == 0: i = 2
            elif i == 1: i = 5
            else: i = 8
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::3]) == 2:
            i = campos[2::3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 6
            else: i = 9
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::2][:3]) == 2:
            i = campos[2::2][:3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 5
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::-4]) == 2:
            i = campos[::-4].index(0)
            if i == 0: i = 9
            elif i == 1: i = 5
            else: i = 1
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[:3]) == -2:
            i = campos[:3].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[3:6]) == -2:
            i = campos[3:6].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+4)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[6:9]) == -2:
            i = campos[6:9].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+7)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::3]) == -2:
            i = campos[::3].index(0)
            if i == 0: i = 1
            elif i == 1: i = 4
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[1::3]) == -2:
            i = campos[1::3].index(0)
            if i == 0: i = 2
            elif i == 1: i = 5
            else: i = 8
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::3]) == -2:
            i = campos[2::3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 6
            else: i = 9
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::2][:3]) == -2:
            i = campos[2::2][:3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 5
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::-4]) == -2:
            i = campos[::-4].index(0)
            if i == 0: i = 9
            elif i == 1: i = 5
            else: i = 1
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        else:
            while True:
                if 0 not in campos:
                    break
                campo = random.choice(campos)
                if campo == 0:
                    i = campos.index(campo)
                    tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
                    tabuleiro.update(campos=simbolo_robot)
                    break
    else:
        if campos[4] == 0:
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=5)
            tabuleiro.update(campos=simbolo_robot)
        elif campos.count(1) == 1:
            campo = random.choice([1, 3, 7, 9])
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=campo)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[:3]) == -2:
            i = campos[:3].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[3:6]) == -2:
            i = campos[3:6].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+4)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[6:9]) == -2:
            i = campos[6:9].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+7)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::3]) == -2:
            i = campos[::3].index(0)
            if i == 0: i = 1
            elif i == 1: i = 4
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[1::3]) == -2:
            i = campos[1::3].index(0)
            if i == 0: i = 2
            elif i == 1: i = 5
            else: i = 8
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::3]) == -2:
            i = campos[2::3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 6
            else: i = 9
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::2][:3]) == -2:
            i = campos[2::2][:3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 5
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::-4]) == -2:
            i = campos[::-4].index(0)
            if i == 0: i = 9
            elif i == 1: i = 5
            else: i = 1
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[:3]) == 2:
            i = campos[:3].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[3:6]) == 2:
            i = campos[3:6].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+4)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[6:9]) == 2:
            i = campos[6:9].index(0)
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+7)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::3]) == 2:
            i = campos[::3].index(0)
            if i == 0: i = 1
            elif i == 1: i = 4
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[1::3]) == 2:
            i = campos[1::3].index(0)
            if i == 0: i = 2
            elif i == 1: i = 5
            else: i = 8
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::3]) == 2:
            i = campos[2::3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 6
            else: i = 9
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[2::2][:3]) == 2:
            i = campos[2::2][:3].index(0)
            if i == 0: i = 3
            elif i == 1: i = 5
            else: i = 7
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        elif sum(campos[::-4]) == 2:
            i = campos[::-4].index(0)
            if i == 0: i = 9
            elif i == 1: i = 5
            else: i = 1
            tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i)
            tabuleiro.update(campos=simbolo_robot)
        else:
            while True:
                if 0 not in campos:
                    break
                campo = random.choice(campos)
                if campo == 0:
                    i = campos.index(campo)
                    tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo, campos=i+1)
                    tabuleiro.update(campos=simbolo_robot)
                    break

def verifica_vencedor(request, jogo):

    campos = registrar_campos(jogo)

    if sum(campos[:3]) == -3 or sum(campos[:3]) == 3:
        if sum(campos[:3]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[3:6]) == -3 or sum(campos[3:6]) == 3:
        if sum(campos[3:6]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[6:9]) == -3 or sum(campos[6:9]) == 3:
        if sum(campos[6:9]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[::3]) == -3 or sum(campos[::3]) == 3:
        if sum(campos[::3]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[1::3]) == -3 or sum(campos[1::3]) == 3:
        if sum(campos[1::3]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[2::3]) == -3 or sum(campos[2::3]) == 3:
        if sum(campos[2::3]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[2::2][:3]) == -3 or sum(campos[2::2][:3]) == 3:
        if sum(campos[2::2][:3]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    elif sum(campos[::-4]) == -3 or sum(campos[::-4]) == 3:
        if sum(campos[::-4]) == -3:
            messages.success(request,'Vencedor é o X')
        else:
            messages.success(request,'Vencedor é o O')

        return True

    else:
        if 0 not in campos:
            messages.error(request,'Que pena deu Velha!')

        return False

def registrar_campos(jogo):

    tabuleiro = Tabuleiro.objects.filter(id_jogo=jogo).values('campos')

    campos = [0 for _ in range(9)]
    for i, valor in enumerate(tabuleiro):
        if valor['campos'] == 'X':
            campos[i] = -1
        if valor['campos'] == 'O':
            campos[i] = 1

    return campos

        

    
 




