import socket
import threading #threads in python
import pickle #i would use this if i wanted to send python objects, for example.

#we are going to put client stuff
#in different threads, avoiding
#the occurance of bottlenecks
#(engarrafamento)

HEADER = 64 #header de 64 bytes. A primeira mensagem para o servidor. Nos informa o comprimento da próxima mensagem
PORT = 5050 #precisamos encontrar ports que não estão sendo usados
#SERVER = "192.168.5.59" #meu endereço ipv4. Eu quero rodar localmente
#outra forma de fazer isso é fazer:
#SERVER = socket.gethostbyname(socket.gethostname()) #esse código pega o ipv4 automaticamente
SERVER = "192.168.5.186"
#print(socket.gethostname()) #pega o nome da máquina
#print(SERVER) #no caso do código acima, printaria o endereço ipv4, no qual o servidor está hosteado
ADDR = (SERVER, PORT)

print(ADDR)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #informa o tipo da conexão. Nesse caso, estaremos lidando com servidores ipvr
print(server)
#precisamos agora ligar o socket com o server
server.bind(ADDR) #nos ligamos o socket com esse o endereço, de modo que qualquer cliente acessando o endereço bate no socket.
#queremos configurar o socket para escuta, agora

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr}')
    conectado = True
    while conectado:
        msg_len = conn.recv(HEADER).decode(FORMAT) #how many bytes we wish to receive from the client.
        if msg_len: #caso a mensagem faça sentido, ou seja, não seja um NULL ou sla
            msg_len = int(msg_len)   #assumindo que estamos transmitindo inteiros
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conectado = False
                print(f'client {ADDR} has disconnected')
            else:
                print(f'[{ADDR}] {msg}')

                confirmation = "Msg Received".encode(FORMAT)
                msg_len = len(confirmation) 
                send_len = str(msg_len).encode(FORMAT) #encode as string
                #we need to make sure send_len is 64
                send_len += b' ' * (HEADER - len(send_len))
                conn.send(send_len)
                conn.send(confirmation)
        #this is very cool

    conn.close()
    pass 

def start(): #começa o socket server
    #o servidor deve começar a escutar e passar para o handle, que será executado em outra thread.
    server.listen()
    print(f'[LISTENING] Servidor escutando em {SERVER}')
    while (1):
        conn, addr = server.accept() #quando uma nova conexão ocorre, armazenamos o endereço e um objeto (conn), que nos possibilita enviar informação de volta para a conexão;
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start() #inicia a nova thread, configurada acima
        print(f'[CONEXÕES] {threading.active_count() - 1}')
    pass

print("[STARTING] servidor iniciando...")
start()