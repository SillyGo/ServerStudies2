import socket
import threading #threads in python

#we are going to put client stuff
#in different threads, avoiding
#the occurance of bottlenecks
#(engarrafamento)

HEADER = 64 #header de 64 bytes. A primeira mensagem para o servidor. Nos informa o comprimento da próxima mensagem.
PORT = 5050 #precisamos encontrar ports que não estão sendo usados
#SERVER = "192.168.5.59" #meu endereço ipv4. Eu quero rodar localmente
#outra forma de fazer isso é fazer:
SERVER = socket.gethostbyname(socket.gethostname()) #esse código pega o ipv4 automaticamente
#print(socket.gethostname()) #pega o nome da máquina
#print(SERVER) #no caso do código acima, printaria o endereço ipv4, no qual o servidor está hosteado
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = "192.168.5.171"
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#now we need to connect to the server
client.connect(ADDR) #conectamos

def send(msg):
    message = msg.encode(FORMAT) #encodes into a byte-like object
    #first message must always be the len
    msg_len = len(message) 
    send_len = str(msg_len).encode(FORMAT) #encode as string
    #we need to make sure send_len is 64
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

    msg_len = client.recv(HEADER).decode(FORMAT)
    if msg_len: #caso a mensagem faça sentido, ou seja, não seja um NULL ou sla
        msg_len = int(msg_len)   #assumindo que estamos transmitindo inteiros
        msg = client.recv(msg_len).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            conectado = False
            print(f'client {ADDR} has disconnected')
        else:
            print(f'[{ADDR}] {msg}')

#send("hello, world!")
send("Hello, Friend!")
send("!DISCONNECT")
