# import socket module
from socket import *
import threading
import datetime as dt
import time

# In order to terminate the program
import sys

proxySocket = socket(AF_INET, SOCK_STREAM)
host = '149.125.168.212'
print(host)
port = 8080
proxySocket.bind((host, port))
proxySocket.listen(10)

cache = {}

def send_messages(filename, thread_id, connectionSocket, msg):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = 8000
    server_host = '149.125.30.245'
    print(server_host)
    serverSocket.connect((server_host, server_port))
    time = dt.datetime.now()
    print(f'proxy-forward, server, {thread_id}, {time}')
    serverSocket.sendall(msg.encode())

    resp = serverSocket.recv(4096)
    try:
        cache[filename] = (resp, dt.datetime.now())
        time = dt.datetime.now()
        print(f'proxy-cache, client, {thread_id}, {time}')
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
        connectionSocket.send(resp)
        connectionSocket.send('\r\n'.encode())
    except:
        time = dt.datetime.now()
        print(f'proxy-cache, client, {thread_id}, {time}')
        connectionSocket.send(b'HTTP/1.1 404 NOT FOUND\r\n')
    return serverSocket

def server(connectionSocket, addr):

    msg = connectionSocket.recv(4096).decode()
    thread_id = threading.get_ident()
    time =  dt.datetime.now()
    filename = msg.split()[1]

    if filename in cache:
        if time.second - cache[filename][1].second < 30:
            time = dt.datetime.now()
            print(f'proxy-cache, client, {thread_id}, {time}')
            resp = b'HTTP/1.1 200 OK\r\n'
            connectionSocket.send(resp)
            connectionSocket.send(cache[filename][0])
            connectionSocket.send('\r\n'.encode())
            connectionSocket.close()
        else:
            del cache[filename]
            serverSocket = send_messages(filename, thread_id, connectionSocket, msg)
            res = serverSocket.recv(4096)
            connectionSocket.send(res)
            serverSocket.close()
    else:
        serverSocket = send_messages(filename, thread_id, connectionSocket, msg)
        res = serverSocket.recv(4096)
        connectionSocket.send(res)
        serverSocket.close()
    connectionSocket.close()


def ping():
    server_info = ('149.125.30.245', 8000)

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)

    ping_seq_num = 0
    success = 0

    rtts = []

    start = time.time()
    while time.time() - start < 180:

        message = f'ping {ping_seq_num}, {time.time()}'

        clientSocket.sendto(message.encode(), server_info)
        print(f'Message sent: {message}')
        ping_seq_num += 1

        sent = time.time()

        try:

            response, server = clientSocket.recvfrom(1024)
            success += 1

            received = time.time()

            rtt = received - sent
            rtts.append(rtt)

            print(f'Response: {response.decode()}')
            print(f'RTT (Rount Trip Time): {rtt}')
            


        except timeout:
            print('Client ping timed out')
        time.sleep(3)

    print('-'*30)
    print('Stats:')
    print()

    print(f'minimum RTT: {min(rtts)}s')
    print(f'maximum RTT: {max(rtts)}s')
    print(f'successful RTTs: {success}')
    sum = 0 
    for rtt in rtts:
        sum += rtt
    print(f'average RTT: {sum / len(rtts)}s')

    

def main():
    ping_thread = threading.Thread(target=ping)
    ping_thread.start()

    while True:
        # Establish the connection
        print('Ready to serve...')

        connectionSocket, addr = proxySocket.accept() 

        thr = threading.Thread(target=server, args=(connectionSocket, addr))
        thr.start()

       

main()
