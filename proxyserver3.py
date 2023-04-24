# import socket module
from socket import *
import threading
import datetime as dt

# In order to terminate the program
import sys

proxySocket = socket(AF_INET, SOCK_STREAM)
host = '149.125.28.177'
print(host)
# local host = 127.0.0.1, eduroam IP = 149.125.90.115
port = 8070
proxySocket.bind((host, port))
proxySocket.listen(5)

cache = {}

def send_messages(filename, thread_id, connectionSocket, msg):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = 8000
    server_host = '149.125.171.215'
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
        if time.second - cache[filename][1].second < 5:
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
