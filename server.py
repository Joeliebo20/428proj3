 # We will need the following module to generate randomized lost packets
import random
import time
import threading

# Import socket module
from socket import *

# Prepare a sever socket
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.settimeout(30)

# Assign IP address and port number to socket
serverSocket.bind(('', 8000))


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

