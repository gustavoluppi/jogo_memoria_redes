import os
import sys
import time
import random

##
# Funções úteis
##

# Limpa a tela.
def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

##
# Funções de manipulação do tabuleiro
##

# Imprime estado atual do tabuleiro
def imprimeTabuleiro(tabuleiro):
    # Limpa a tela
    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    sys.stdout.write("     ")
    for i in range(dim):
        sys.stdout.write("{0:2d} ".format(i))

    sys.stdout.write("\n")

    # Imprime separador horizontal
    sys.stdout.write("-----")
    for i in range(dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for i in range(dim):
        # Imprime coordenadas verticais
        sys.stdout.write("{0:2d} | ".format(i))

        # Imprime conteúdo da linha 'i'
        for j in range(dim):
            # Peça já foi removida?
            if tabuleiro[i][j] == '-':
                sys.stdout.write(" - ")
            # Peça está levantada?
            elif tabuleiro[i][j] >= 0:
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))
            else:
                # Não, imprime '?'
                sys.stdout.write(" ? ")

        sys.stdout.write("\n")

# Cria um novo tabuleiro com peças aleatórias. 
# 'dim' é a dimensão do tabuleiro, necessariamente par.
def novoTabuleiro(dim):
    # Cria um tabuleiro vazio.
    tabuleiro = []
    for i in range(dim):
        linha = []
        for j in range(dim):
            linha.append(0)
        tabuleiro.append(linha)

    # Cria uma lista de todas as posições do tabuleiro. Util para
    # sortearmos posições aleatoriamente para as peças.
    posicoesDisponiveis = []
    for i in range(dim):
        for j in range(dim):
            posicoesDisponiveis.append((i, j))

    # Varre todas as peças que serão colocadas no tabuleiro e
    # posiciona cada par de peças iguais em posições aleatórias.
    for j in range(dim // 2):
        for i in range(1, dim + 1):
            # Sorteio da posição da segunda peça com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posição da segunda peça com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

    return tabuleiro

# Abre (revela) peça na posição (i, j). Se posição já está
# aberta ou se já foi removida, retorna False. Retorna True
# caso contrário.
def abrePeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True
    return False

# Fecha peça na posição (i, j). Se posição já está
# fechada ou se já foi removida, retorna False. Retorna True
# caso contrário.
def fechaPeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True
    return False

# Remove peça na posição (i, j). Se posição já está
# removida, retorna False. Retorna True
# caso contrário.
def removePeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = "-"
        return True

## 
# Funções de manipulação do placar
##

# Cria um novo placar zerado.
def novoPlacar(nJogadores):
    return [0] * nJogadores

# Adiciona um ponto no placar para o jogador especificado.
def incrementaPlacar(placar, jogador):
    placar[jogador] += 1

# Imprime o placar atual.
def imprimePlacar(placar):
    nJogadores = len(placar)
    print("Placar:")
    print("---------------------")
    for i in range(nJogadores):
        print("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

##
# Funções de interação com o usuário
#

# Imprime informações básicas sobre o estado atual da partida.
def imprimeStatus(tabuleiro, placar, vez):
    imprimeTabuleiro(tabuleiro)
    sys.stdout.write('\n')
    imprimePlacar(placar)
    sys.stdout.write('\n')
    sys.stdout.write('\n')
    print("Vez do Jogador {0}.\n".format(vez + 1))

# Lê as coordenadas de uma peça. Retorna uma tupla do tipo (i, j)
# em caso de sucesso, ou False em caso de erro.
def leCoordenada(dim):
    entrada = input("Especifique uma peça: ")

    try:
        i = int(entrada.split(' ')[0])
        j = int(entrada.split(' ')[1])
    except ValueError:
        print("Coordenadas inválidas! Use o formato \"i j\" (sem aspas),")
        print("onde i e j são inteiros maiores ou iguais a 0 e menores que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if i < 0 or i >= dim:
        print("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if j < 0 or j >= dim:
        print("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    return (i, j)

##
# Parâmetros da partida
##

# Tamanho (da lateral) do tabuleiro. NECESSARIAMENTE PAR E MENOR QUE 10!
dim = 4

# Número de jogadores
nJogadores = 2

# Número total de pares de peças
totalDePares = dim**2 // 2

##
# Programa principal
##

# Cria um novo tabuleiro para a partida
tabuleiro = novoTabuleiro(dim)

# Cria um novo placar zerado
placar = novoPlacar(nJogadores)

# Partida continua enquanto ainda há pares de peças a casar.
paresEncontrados = 0
vez = 0
while paresEncontrados < totalDePares:
    # Requisita primeira peça do próximo jogador
    while True:
        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        # Solicita coordenadas da primeira peça.
        coordenadas = leCoordenada(dim)
        if coordenadas == False:
            continue

        i1, j1 = coordenadas

        # Testa se peça já está aberta (ou removida)
        if abrePeca(tabuleiro, i1, j1) == False:
            print("Escolha uma peça ainda fechada!")
            input("Pressione <enter> para continuar...")
            continue

        break 

    # Requisita segunda peça do próximo jogador
    while True:
        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        # Solicita coordenadas da segunda peça.
        coordenadas = leCoordenada(dim)
        if coordenadas == False:
            continue

        i2, j2 = coordenadas

        # Testa se peça já está aberta (ou removida)
        if abrePeca(tabuleiro, i2, j2) == False:
            print("Escolha uma peça ainda fechada!")
            input("Pressione <enter> para continuar...")
            continue

        break 

    # Imprime status do jogo
    imprimeStatus(tabuleiro, placar, vez)

    print("Peças escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))

    # Peças escolhidas são iguais?
    if tabuleiro[i1][j1] == tabuleiro[i2][j2]:
        print("Peças casam! Ponto para o jogador {0}.".format(vez + 1))
        incrementaPlacar(placar, vez)
        paresEncontrados += 1
        removePeca(tabuleiro, i1, j1)
        removePeca(tabuleiro, i2, j2)

        time.sleep(5)
    else:
        print("Peças não casam!")
        time.sleep(3)

        fechaPeca(tabuleiro, i1, j1)
        fechaPeca(tabuleiro, i2, j2)
