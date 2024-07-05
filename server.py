import socket
import threading

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8000
BUFFER = 1024

# Dicionários para armazenar todos os clientes conectados e seus nomes e a tupla que contem o ip e a porta
# clients names Socket: <socket.socket fd=1168, family=2, type=1, proto=0, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 65172)>, Nome: fe
# clients addresses Socket: <socket.socket fd=1168, family=2, type=1, proto=0, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 65172)>, Endereço: ('127.0.0.1', 65172)
names = {}
addresses = {}

def handle_client(client_socket, client_address):  
    """ 
    Função para lidar com cada cliente
    
    Args:
        client_socket (socket): objeto socket que representa a conexão com o cliente
        client_address (tupla): tupla que contém o endereço IP e porta do cliente
    """
        
    name = client_socket.recv(BUFFER).decode('utf-8')           # O servidor recebe uma mensagem com o nome de usuário do cliente e armazena-o no dicionario usando como chave o socket
    names[client_socket] = name    
    broadcast(f"{name} está conectado.", client_socket, 2)
    addresses[client_socket] = client_address                   # A função recebe o endereço do cliente e armazena em um dicionário
    client_socket.send(f'Bem vindo(a) {name}!\nDigite "exit" para encerrar a conexão\n'.encode('utf-8')) # Envia uma mensagem de bem vindo para o cliente 
    while True:                                                 
        try:
            message = client_socket.recv(BUFFER).decode('utf-8') 
            if message.lower() == 'exit':                       # Caso o usuário envie um 'exit' o laço é encerrado e é chamada a função para remover o cliente
                remove(client_socket)
                break
            else:
                broadcast(message, client_socket, 1)
        except:
            continue

def broadcast(message, client_socket, filter):
    """
    Função para transmitir mensagens para todos os clientes conectados, exceto para o cliente que enviou a mensagem original (client_socket).

    Args:
        message (string): mensagem que será enviada para os demais clientes
        client_socket (socket): objeto socket que representa a conexão com o cliente
    """
    for client in names:                                        # Percorre todos os nomes no dicionario
        if client != client_socket:
            if filter == 1:
                client.send(f"{names[client_socket]}: {message}".encode('utf-8'))   # Envia a mensagem no estilo Nome: mensagem
            elif filter == 2:
                client.send(message.encode('utf-8'))
                
def remove(client_socket):
    """
    Função para remover clientes desconectados. Remove dos dicionários e fecha o socket.
    
    Args:
        client_socket (socket): objeto socket que representa a conexão com o cliente
    """
    
    if client_socket in names:
        name = names[client_socket]
        print(f"Conexão com {name} ({addresses[client_socket]}) está fechada.")
        broadcast(f"{name} foi desconectado.", client_socket, 2)   # Notificar os outros clientes que o cliente foi desconectado
        del names[client_socket]
        del addresses[client_socket]
        client_socket.close()
    
def main():    
    """
    Função principal do servidor.
    Cria um objeto socket, faz o bind do socket com o endereço e porta 
    Executa 5 conexões simultâneas
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print("O servidor está aberto para a conexão...")

    while True:
        client_socket, client_address = server.accept()          # Aceitando conexões
        print(f"Conexão estabelecida com {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()    # Inicia uma nova thread que lida com esse cliente específico
           
if __name__ == "__main__":
    main()