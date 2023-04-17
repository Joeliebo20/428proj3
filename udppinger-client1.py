# We will need the following module to generate randomized lost packets
import random
import time

# Import socket module
from socket import *

# Prepare a sever socket
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
port = 8000
host = gethostbyname(gethostname())
print(f'host: {host}')
serverSocket.bind((host, port))


client = socket(AF_INET, SOCK_DGRAM)
start = time.time()


while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue

    # Otherwise, prepare the server response
    print(message)

    # The server responds
    serverSocket.sendto(message, address)
