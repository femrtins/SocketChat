import socket
import threading
import os

SERVER_IP = '127.0.0.1' # IP do servidor 
SERVER_PORT = 8000
BUFFER = 1024

def receive_messages(client_socket):
    """
    Função recebe mensagens do servidor e exibe no terminal

    Args:
        client_socket (socket): objeto socket que representa a conexão com o cliente
    """

    while True:
        try:
            message = client_socket.recv(BUFFER).decode('utf-8')        # Recebe mensagens do servidor 
            if message:                
                print(message)                                          # Se houver mensagens, imprime 
        except:                            
            client_socket.close()                                       # Encerrar o programa do cliente (dá erro se não tiver isso)
            os._exit(0)  
            

def main():
    """
    Função que inicializa o cliente.
    Cria um objeto socket e o conecta ao servidor 
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((SERVER_IP, SERVER_PORT))    
    
    name = input("Nome do usuário: ")                               
    client.send(name.encode('utf-8'))                                   # Enviar nome de usuário para o servidor
    threading.Thread(target=receive_messages, args=(client,)).start()   # Inicia uma thread para receber mensagens do servidor enquanto realiza também o loop 

    while True:
        message = input("")
        client.send(message.encode('utf-8'))                            # Enviar a mensagem para o servidor
        if message.lower() == 'exit':                                   # Se a mensagem for exit o cliente será desconectado
            print("Você foi desconectado.")
            client.close()
            os._exit(0)                                                 # Encerrar o programa do cliente

if __name__ == "__main__":
    main()
