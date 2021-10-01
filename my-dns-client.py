import sys
import time
import socket

hostname = sys.argv[1] # hostname argument given by command line
message = b"" # the message to send through socket
data = b"" # the message to receive from socket
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket


print("Preparing DNS query..")

# Header Fields
header_id = None
header_qr = None
header_opcode = None
header_aa = None
header_tc = None
header_rd = None
header_ra = None
header_z = None
header_rcode = None
header_qdcount = None
header_ancount = None
header_nscount = None
header_arcount = None

# Question Fields
question_qname = None
question_qtype = None
question_qclass = None


print("Contacting DNS server..")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_host = socket.gethostname() # client hostname
server = "8.8.8.8" 
udp_port = 53 # DNS Server port is 53
print("socket hostname:",udp_host)
print("socket port:",udp_port)
start_time = time.time() # setting start time
while (attempts <= 3 and time.time() < start_time+5): # within 3 attempts AND less than 5 seconds elapsed
    attempts += 1
    print("Sending DNS query..:",attempts)
    udp_socket.sendto(message, (udp_host, udp_port))
    try:
        data, server = udp_socket.recvfrom(53)
        print("DNS response received (attempt",attempts,"of 3)")
        print("Processing DNS resopnse..")
        print("----------------------------------------------------------------------------")
        print("header.ID =",header_id)
        print("header.QR =",header_qr)


    except socket.timeout:
        print("DNS query failed")
