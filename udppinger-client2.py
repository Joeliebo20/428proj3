# Import socket module
from socket import *
import time

server_info = ('', 8000)

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