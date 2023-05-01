# import socket module
from socket import *
import threading
import datetime as dt
import random
import time

# In order to terminate the program
import sys

def UDP_server():
     # We will need the following module to generate randomized lost packets
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.settimeout(30)

    # Assign IP address and port number to socket
    serverSocket.bind(('149.125.168.212', 8000))


    sequence_number = 0
    packets_lost = 0
    total = 0


    while True:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)

        try:
            # Receive the client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            total += 1

            # If rand is less is than 4, we consider the packet lost and do not respond
            if rand < 4:
                # print('packet lost')
                packets_lost += 1
                continue
            else:
                response = f'echo, {sequence_number}, {time.time()}'
                sequence_number += 1
                serverSocket.sendto(response.encode(), address)
        except timeout:
            if total != 0:
                print(f'packet loss rate: {(packets_lost / total) * 100}%')
            print('Server echo timed out.')
            break

def server(connectionSocket):
    thread_id = threading.get_ident()
    try:
        message = connectionSocket.recv(1024).decode()
        # get the filename from request msg, need to parse it
        # prints http request, need to parse the filename out of the 'GET /home.html HTTP/1.1'

        filename = message.split()[1]


        # Send one HTTP header line into socket

        # HTTP/1.1 200 OK
        if '.pdf' in filename:
            f = open(filename[1:], 'rb')
            outputdata = f.read()
            application = "application/pdf"
            msg = f'HTTP/1.1 200 OK\r\nContent-Type: {application}\r\nContent-Length: {len(outputdata)}\r\n\r\n'
            connectionSocket.send(msg.encode())
            connectionSocket.sendall(outputdata)
        # Send the content of the requested file into socket
        else:
            f = open(filename[1:])
            outputdata = f.readlines()
            connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            

        time = dt.datetime.now()
        print(f'server-response, 200 OK, {thread_id}, {time}')
        # Send the content of the requested file into socket
        # Close client socket 
        connectionSocket.close()
    except IOError:
        msg = b'HTTP/1.1 404 NOT FOUND\r\n'
        connectionSocket.send(msg)
        time = dt.datetime.now()
        print(f'server-response, 404 NOT FOUND, {thread_id}, {time}')
        # Send response message for file not found
        ### YOUR CODE HERE ###
        # create out own sequence with format of http response msg
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM) # local host = 127.0.0.1, eduroam IP = 149.125.90.115
    host = '149.125.168.212'
    print(host) # local host = 127.0.0.1, eduroam IP = 149.125.90.115
    port = 8000
    serverSocket.bind((host, port))
    serverSocket.listen(10)

    UDP_thread = threading.Thread(target=UDP_server)
    UDP_thread.start()

    while True:
        print("Ready to serve...")

        connectionSocket, addr = serverSocket.accept() 

        thr = threading.Thread(target=server, args=(connectionSocket,))
        thr.start()

main()
