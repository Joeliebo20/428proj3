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

# Assign IP address and port number to socket
port = 8000
host = gethostbyname(gethostname())
print(f'host: {host}')
serverSocket.bind((host, port))



client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(1) # wait up to one second
sequence_number = 1
packets_sent = 0
packets_received = 0

total_time = 180 # 3 minutes in seconds

# no need for host, port since this is only a pinger

start = time.time()

while time.time() - start < 180:
    msg = f'ping {sequence_number} sent successfully at {time.time()}'

    try:
        server_info = (host, port)
        client.sendto(msg, server_info)
        packets_sent += 1
        sequence_number += 1

        resp, addr = client.recvfrom(1024)
        packets_received += 1
    except:
        


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
