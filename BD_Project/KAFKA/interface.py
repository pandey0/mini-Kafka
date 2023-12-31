import socket
import threading
import random
from multiprocessing import Process

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


# Lists For Clients and Their Nicknames

producer = []
consumer =[]
broker1_topic = []
broker2_topic = []
broker3_topic = []

#running in parallel

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()


#get from broker
def getfrombroker(client):
    x=client.recv(1024).decode('ascii')
    x=x.split()
    if x[1] in broker1_topic:
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect(('127.0.0.2', 55556))#enter the broker credentials
        client1.send(x.encode('ascii'))
        recived_data = client1.recv(1024).decode('ascii')
        client1.close()
        client.send(recived_data.encode('ascii'))
    elif x[1] in broker2_topic:
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect(('127.0.0.2', 55557))#enter the broker credentials
        client2.send(x.encode('ascii'))
        recived_data = client2.recv(1024).decode('ascii')
        client2.close()
        client.send(recived_data.encode('ascii'))

    else:
        client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client3.connect(('127.0.0.2', 55558))#enter the broker credentials
        client3.send(x.encode('ascii'))
        recived_data = client3.recv(1024).decode('ascii')
        client3.close()
        client.send(recived_data.encode('ascii'))

    

    

#connecting to brokers
def sendbroker1(client):
    x=client.recv(1024).decode('ascii')
    y=x.split(",",1)
    broker1_topic.append(y[0])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 55556))#enter the broker credentials
    print(x)
    client.send(x.encode('ascii'))
    client.close()
    return

def sendbroker2(client):
    x=client.recv(1024).decode('ascii')
    y=x.split(",",1)
    broker2_topic.append(y[0])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 55557))#enter the broker credentials
    print(x)
    client.send(x.encode('ascii'))
    client.close()
    return
    
def sendbroker3(client):
    x=client.recv(1024).decode('ascii')
    y=x.split(",",1)
    broker3_topic.append(y[0])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 55558))#enter the broker credentials
    print(x)
    client.send(x.encode('ascii'))
    client.close()
    return

#handling the producer 
def sendtobroker(client):
    runInParallel(sendbroker1(client),sendbroker2(client),sendbroker3(client))
    

    
# Handling Messages From consumer and producer 
def handle(client):
    if client in producer:
        sendtobroker(client)
    elif client in consumer:
        getfrombroker(client)
                #sendfile(client)
       
#send file for consumer



# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if nickname == 'producer':
            producer.append(client)
        elif nickname == 'consumer':
            consumer.append(client)

        

        # Print And Broadcast Nickname
        print("user is {}".format(nickname))
        
        

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()