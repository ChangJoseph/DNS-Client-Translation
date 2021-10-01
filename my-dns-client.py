import sys
import time
import socket

hostname = sys.argv[1] # hostname argument given by command line
message = b"" # the message to send through socket
start_time = 0 # start time of socket send attempts
time = 0 # time elapsed in seconds
attempts = 0 # number of times attempted to send message through socket

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


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_host = socket.gethostname() # client hostname
udp_port = 53 # DNS Server port is 53
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
