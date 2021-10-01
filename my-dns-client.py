import sys
import time
import socket

hostname = sys.argv[1] # hostname argument given by command line
message = b"" # the message to send through socket
data = b"" # the message to receive from socket
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket

# Header Fields
id = None
qr = None
opcode = None
aa = None
tc = None
rd = None
ra = None
z = None
rcode = None
qdcount = None
ancount = None
nscount = None
arcount = None

# Question Fields
qname = None
qtype = None
qclass = None


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_host = socket.gethostname() # client hostname
print (udp_host)
server = "8.8.8.8" 
udp_port = 53 # DNS Server port is 53
print('socket hostname:',udp_host)
print('socket port:',udp_port)
start_time = time.time() # setting start time
while (attempts <= 3 and time.time() < start_time+5): # within 3 attempts AND less than 5 seconds elapsed
    attempts += 1
    print('socket send attempt number:',attempts)
    udp_socket.sendto(message, (udp_host, udp_port))
    try:
        data, server = udp_socket.recvfrom(53)
    except socket.timeout:
        print('Retrying message send')
