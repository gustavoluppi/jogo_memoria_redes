import socket

# Define o endereço do servidor e a porta
HOST = '127.0.0.1'  # Endereço local do servidor
PORT = 8000          # Porta

# Cria um socket TCP
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor
socket_tcp.connect((HOST, PORT))

player_id = socket_tcp.recv(2048).decode()
print(f'Seu ID de jogador é: {player_id}')


while True:
    data = socket_tcp.recv(4096)
    print(f'Resposta do servidor: {data.decode()}')

    if("Escolha uma posição (linha,coluna):" in data.decode()):
        mensagem = input()
        socket_tcp.sendall(mensagem.encode())
    
    elif ("Aguarde" in data.decode()):
        print("Aguarde a sua vez...")

        


    
    # # Envia uma mensagem
    # mensagem = input("Digite uma mensagem para enviar ao servidor (ou 'sair' para encerrar): ")
    # socket_tcp.sendall(mensagem.encode())
        
    # # Se o usuário digitar 'sair', encerra a conexão
    # if mensagem.lower() == 'sair':
    #     break
    # Recebe a resposta
    

