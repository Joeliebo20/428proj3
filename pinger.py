# Import socket module
from socket import *
import time

# Set the server address and port number
server_info = ('', 8000)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

ping_seq_num = 0
success = 0

rtts = []

# Send the pings and receive the responses
start = time.time()
while time.time() - start < 180:
    # Prepare the message to send
    message = f'ping {ping_seq_num}, {time.time()}'

    # Send the message to the server
    clientSocket.sendto(message.encode(), server_info)
    print(f'Message sent: {message}')
    ping_seq_num += 1

    # Record the time the ping was sent
    sent = time.time()

    try:
        # Receive the server response
        response, server = clientSocket.recvfrom(1024)
        success += 1

        # Record the time the ping was received
        received = time.time()

        # Calculate the round trip time
        rtt = received - sent
        rtts.append(rtt)

        # Print the response message and round trip time
        print(f'Response: {response.decode()}')
        print(f'RTT (Rount Trip Time): {rtt}')
        


    except timeout:
        # If a response isn't received within the timeout period, print a message
        print('Client ping timed out')
    time.sleep(3)

print(f'minimum RTT: {min(rtts)}s')
print(f'maximum RTT: {max(rtts)}s')
print(f'successful RTTs: {success}')
sum = 0 
for rtt in rtts:
    sum += rtt
print(f'average RTT: {sum / len(rtts)}s')