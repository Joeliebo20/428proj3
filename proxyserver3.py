# import socket module
from socket import *
import threading
import datetime as dt

# In order to terminate the program
import sys

proxySocket = socket(AF_INET, SOCK_STREAM)
host = '149.125.28.177'
# local host = 127.0.0.1, eduroam IP = 149.125.90.115
port = 8080
proxySocket.bind((host, port))
proxySocket.listen(10)

def parse_port(msg):
    start_index = msg.find("/") + 1
    end_index = msg.find("/", start_index)
    port = msg[start_index:end_index]
    return port

def parse_host(msg):
    host_start = msg.find('Host: ') + len('Host: ')
    host_end = msg.find('\r\n', host_start)
    host = msg[host_start:host_end]
    if ':' in host:
        host, port = host.split(':')
    print('host: ', host)
    return host

def server(connectionSocket, addr):

    msg = connectionSocket.recv(4096)
    print(msg)
    filename = msg.decode().split()[1]
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server_port = 8000
    server_host = '149.125.171.215'
    print(server_host)
    thread_id = threading.get_ident()
    
    serverSocket.connect((server_host, server_port))
    time = dt.datetime.now()
    print(f'proxy-forward, server, {thread_id}, {time}')
    serverSocket.sendall(msg)

    res = serverSocket.recv(4096)
    
    if '.pdf' in filename:
        f = open(filename[1:], 'rb')
        data = f.read()
        msg = f'HTTP/1.1 200 OK\r\nContent-Type: application/pdf\r\nContent-Length: {len(data)}\r\n\r\n'
        if msg.encode() is res:
            connectionSocket.send(f'HTTP/1.1 200 OK\r\nContent-Type: application/pdf\r\nContent-Length: {len(data)}\r\n\r\n')
    else:
        connectionSocket.send(res)

    serverSocket.close()
    connectionSocket.close()

def main():
    while True:
        # Establish the connection
        print('Ready to serve...')

        connectionSocket, addr = proxySocket.accept() 

        thr = threading.Thread(target=server, args=(connectionSocket, addr))
        thr.start()

main()