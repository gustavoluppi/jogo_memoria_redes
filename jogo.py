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
        sys.stdout.write("{:2d} ".format(i))

    sys.stdout.write("\n")

    # Imprime separador horizontal
    sys.stdout.write("-----")
    for i in range(dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for i in range(dim):
        # Imprime coordenadas verticais
        sys.stdout.write("{:2d} | ".format(i))

        # Imprime conteúdo da linha 'i'
        for j in range(dim):
            # Peça já foi removida?
            if tabuleiro[i][j] == '-':
                sys.stdout.write(" - ")
            # Peça está levantada?
            elif tabuleiro[i][j] >= 0:
                sys.stdout.write("{:2d} ".format(tabuleiro[i][j]))
            else:
                # Não, imprime '?'
                sys.stdout.write(" ? ")

        sys.stdout.write("\n")

# Cria um novo tabuleiro com peças aleatórias. 
# 'dim' é a dimensão do tabuleiro, necessariamente par.
def novoTabuleiro(dim):
    # Cria um tabuleiro vazio.
    tabuleiro = [[0] * dim for _ in range(dim)]

    # Cria uma lista de todas as posições do tabuleiro.
    posicoesDisponiveis = [(i, j) for i in range(dim) for j in range(dim)]

    # Varre todas as peças que serão colocadas no 
    # tabuleiro e posiciona cada par de peças iguais
    # em posições aleatórias.
    for j in range(dim // 2):
        for i in range(1, dim + 1):
            for _ in range(2):  # Para colocar o par de peças
                # Sorteio da posição da peça
                indiceAleatorio = random.randint(0, len(posicoesDisponiveis) - 1)
                rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)
                tabuleiro[rI][rJ] = -i

    return tabuleiro

# Abre (revela) peça na posição (i, j).
def abrePeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True
    return False

# Fecha peça na posição (i, j).
def fechaPeca(tabuleiro, i, j):
    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True
    return False

# Remove peça na posição (i, j).
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
        print("Jogador {:d}: {:2d}".format(i + 1, placar[i]))

##
# Funções de interação com o usuário
#

# Imprime informações básicas sobre o estado atual da partida.
def imprimeStatus(tabuleiro, placar, vez):
    imprimeTabuleiro(tabuleiro)
    sys.stdout.write('\n')
    imprimePlacar(placar)
    sys.stdout.write('\n\n')
    print("Vez do Jogador {:d}.\n".format(vez + 1))




def leCoordenada(dim, coordenadas, vez, players):
    print("ESTOU AQUI coord")
    try:
        i, j = map(int, coordenadas.split())
    except ValueError:
        conn = players[vez]
        conn.sendall("Coordenadas inválidas! Use o formato \"i j\" (sem aspas).\n".encode())
        return False  # Permite que o jogador tente novamente

    if i < 0 or i >= dim or j < 0 or j >= dim:
        conn = players[vez]
        conn.sendall("Coordenadas fora dos limites do tabuleiro.\n".encode())
        return False  # Permite que o jogador tente novamente

    return (i, j)

def enviaTabuleiro(players, tabuleiro):
    # Limpa a tela (opcional, mas pode ser deixado se você não quiser limpar a tela do servidor)
    # limpaTela()

    # Cria a representação do tabuleiro como uma string
    dim = len(tabuleiro)
    tabuleiro_str = "     "
    
    # Adiciona as coordenadas horizontais
    for i in range(dim):
        tabuleiro_str += "{:2d} ".format(i)
    
    tabuleiro_str += "\n"

    # Adiciona separador horizontal
    tabuleiro_str += "-----"
    for i in range(dim):
        tabuleiro_str += "---"
    
    tabuleiro_str += "\n"

    # Adiciona o conteúdo do tabuleiro
    for i in range(dim):
        # Adiciona as coordenadas verticais
        tabuleiro_str += "{:2d} | ".format(i)

        for j in range(dim):
            # Verifica se a peça já foi removida
            if tabuleiro[i][j] == '-':
                tabuleiro_str += " - "
            elif tabuleiro[i][j] >= 0:
                tabuleiro_str += "{:2d} ".format(tabuleiro[i][j])
            else:
                # Peça não levantada
                tabuleiro_str += " ? "

        tabuleiro_str += "\n"

    # Envia o tabuleiro formatado para todos os jogadores
    for conn in players:
        conn.sendall(f"Estado atual do tabuleiro:\n{tabuleiro_str}\n".encode())


##
# Parâmetros da partida
##

def jogo(players):

    
    
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

    # Partida continua enquanto ainda há pares de peças a 
    # casar.
    paresEncontrados = 0
    vez = 0
    while paresEncontrados < totalDePares:
        # Requisita primeira peça do próximo jogador
        while True:
            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            enviaTabuleiro(players, tabuleiro)

            conn = players[vez]
            conn.sendall(f"É a sua vez, Jogador {vez}. Escolha uma posição (linha,coluna):\n".encode())

            for j, other_conn in enumerate(players):
                if j != vez:
                    other_conn.sendall(f"Aguarde, é a vez do jogador {vez}.\n".encode())

            # Solicita coordenadas da primeira peça.
            data = conn.recv(2048)
            coordenadas = data.decode()  # Esperando entrada como "linha,coluna"
            coordenadas = leCoordenada(dim, coordenadas, vez, players)
            print("ATE AQUI 0")
            if coordenadas is False:
                conn.sendall("É a sua vez, Jogador. Escolha uma posição (linha,coluna):\n".encode())
                continue

            i1, j1 = coordenadas
            print("ATE AQUI")
            # Testa se peça já está aberta (ou removida)
            if not abrePeca(tabuleiro, i1, j1):
                conn.sendall("Escolha uma peça ainda fechada!\n".encode())
                # input("Pressione <enter> para continuar...")
                continue
            print("ATE AQUI 2")
            break 

        # Requisita segunda peça do próximo jogador
        while True:
            # Imprime status do jogo
            print("ATE AQUI 3")
            imprimeStatus(tabuleiro, placar, vez)

            enviaTabuleiro(players, tabuleiro)

            conn = players[vez]
            conn.sendall(f"É a sua vez, Jogador {vez}. Escolha uma posição (linha,coluna):\n".encode())
            data = conn.recv(2048)
            coordenadas = data.decode()  # Esperando entrada como "linha,coluna"
            # Solicita coordenadas da segunda peça.
            coordenadas = leCoordenada(dim, coordenadas,vez, players)
            if coordenadas is False:
                continue

            i2, j2 = coordenadas

            # Testa se peça já está aberta (ou removida)
            if not abrePeca(tabuleiro, i2, j2):
                conn.sendall("Escolha uma peça ainda fechada!\n".encode())
                # input("Pressione <enter> para continuar...")
                continue
            break 

        # Imprime status do jogo
        # imprimeStatus(tabuleiro, placar, vez)
        enviaTabuleiro(players, tabuleiro)
        

        print("Peças escolhidas --> ({:d}, {:d}) e ({:d}, {:d})\n".format(i1, j1, i2, j2))
        conn.sendall("Peças escolhidas --> ({:d}, {:d}) e ({:d}, {:d})\n".format(i1, j1, i2, j2).encode())

        # Peças escolhidas são iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:
            print("Peças casam! Ponto para o jogador {:d}.".format(vez + 1))
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
            vez = (vez + 1) % nJogadores

    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = [i for i in range(nJogadores) if placar[i] == pontuacaoMaxima]

    if len(vencedores) > 1:
        sys.stdout.write("Houve empate entre os jogadores ")
        sys.stdout.write(' '.join(str(i + 1) for i in vencedores))
        sys.stdout.write("\n")
    else:
        print("Jogador {:d} foi o vencedor!".format(vencedores[0] + 1))

