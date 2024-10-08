import socket
import threading
from jogo import jogo
# Define o endereço do servidor e a porta
HOST = '127.0.0.1'  # Endereço local
PORT = 8000          # Porta

player_id = 0
players = []  # Lista para armazenar as conexões dos jogadores

def handle_connections(conn, addr):
    conn.settimeout(10)
    global player_id
   
    conn.sendall(str(player_id).encode())  # Envia o ID do jogador ao cliente
    print(f'Conectado por {addr} com ID: {player_id}')
    players.append(conn)
    
    if len(players) == num_connections:
        for player in players:
            player.sendall('Todos os jogadores estão conectados. Você pode começar a jogar!'.encode())
        # while(ninguem vencer)  #Todo
        jogo(players) 
    else:
        conn.sendall(f'Aguardando outros jogadores... (Você é jogador {player_id})'.encode())
    player_id += 1  # Incrementa o ID do jogador
    while True:
    # Recebe dados do cliente
        data = conn.recv(2048)
        
        print(f'Recebido: {data.decode()}')
        if (data.decode() == "sair"):
            break
    # Envia uma resposta
        # conn.sendall(data)  # Ecoa de volta
    print(f'Conexão encerrada com {addr}')

# Cria um socket TCP(STREAM) -> AF_INET (IPV4 ou IPV6)
socket_tcp =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Liga o socket ao endereço e porta
socket_tcp.bind((HOST, PORT))
# Escuta por conexões
socket_tcp.listen()
print(f'Servidor ouvindo em {HOST}:{PORT}')
    
# Aceita uma conexão
num_connections = int(input("Quantas conexões o servidor deve aceitar? "))

for _ in range(num_connections):

    conn, addr = socket_tcp.accept()
    client_thread = threading.Thread(target=handle_connections, args=(conn, addr))
    client_thread.start()
   

    
print("Número máximo de conexões aceitas. O jogo irá começar")
