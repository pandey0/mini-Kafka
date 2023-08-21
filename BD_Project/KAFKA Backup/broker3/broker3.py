import socket
import threading

# Connection Data
host = '127.0.0.2'
port = 55558

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


#send file for consumer
def sendfile(client):
    y = client.recv(1024).decode('ascii')
    data = open(f"{y}.txt", "r")
    for line in data:
        #print(line)
        topic = y.encode("ascii")
        content = line.encode("ascii")
        #client.send(topic)
        client.send(content)
        #client.send(line.encode('ascii'))
    

    
#topic creation txt

def write_file(x):
        with open(f"{x[0]}.txt", "a+") as text_file:
            text_file.write(x[1]+",")




# Handling Messages From Clients
def handle(client):
     x=client.recv(1024).decode('ascii')
     print(x)
     x=x.split(",",1)
     if x[0]== "get" :
        sendfile(client)
     else:
        write_file(x)

# Receiving / Listening Function
def receive():
    while True:
        print("Hello")
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()