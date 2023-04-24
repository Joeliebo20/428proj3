# We will need the following module to generate randomized lost packets
import random
import time

# Import socket module
from socket import *

# Prepare a sever socket
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets


def ping(client, host, port, sequence_number):
    try:
        server_info = (host, port)
        sent = time.time()
        msg = f'ping, {sequence_number}, {time.time()}'.encode()
        client.sendto(msg, server_info)
        print(f'message: {msg.decode()}')
        # packets_sent += 1

        resp, addr = client.recvfrom(1024)
        received = time.time()
        print(f'response: {resp.decode()}')
        # packets_received += 1
        rtt = received - sent
        print(f'Round Trip Time (RTT): {rtt}')
        print()
    except:
        print("Client ping timed out")

    time.sleep(3) # wait 3 seconds until next send


def main():
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Assign IP address and port number to socket
    port = 8000
    host = gethostbyname(gethostname())
    print(f'host: {host}')
    serverSocket.bind((host, port))



    client = socket(AF_INET, SOCK_DGRAM)
    client.settimeout(1) # wait up to one second


    total_time = 180 # 3 minutes in seconds

    # no need for host, port since this is only a pinger

    start = time.time()

    sequence_number = 1
    seq_number = 0

    while True:
        if time.time() - start > total_time:
            break
        
        ping(client, host, port, seq_number)
        seq_number += 1
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)

        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)

        # If rand is less is than 4, we consider the packet lost and do not respond
        if rand < 4:
            print("packet lost")
            response = 'packet lost' 
            serverSocket.sendto(response.encode(), address)
        else:
            # Otherwise, prepare the server response
            response = f'echo, {sequence_number}, {time.time()}'
            sequence_number += 1
            serverSocket.sendto(response.encode(), address)

main()
