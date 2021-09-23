import sys
import time
import socket

hostname = sys.argv[1]
message = ""
start_time = 0
time = 0 # time in seconds
attempts = 0

# Header Fields
id
qr
opcode
aa
tc
rd
ra
z
rcode
qdcount
ancount
nscount
arcount

# Question Fields
qname
qtype
qclass


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_host = socket.gethostname()
udp_port = 53
print('socket hostname:',udp_host)
print('socket port:',udp_port)
start_time = time.time()
while (attempts <= 3 and time < start_time+5):
    attempts += 1
    print('socket send attempt number:',attempts)
    udp_socket.sendto(message, (udp_host, udp_port))
    try:
        data, server = udp_socket.recvfrom(53)
    except socket.timeout:
        print('Retrying message send')
        time = time.time()
