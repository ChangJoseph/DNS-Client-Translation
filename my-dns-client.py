import sys
import time
import socket

cli_hostname = sys.argv[1] # hostname argument given by command line
message = 0 # the message to send through socket
data = 0 # the message to receive from socket
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket


print("Preparing DNS query..")

# Header Fields
header_id = 1 # start with id 0: 16 bits
message |= header_id
header_qr = 0 # 1 bit: 0 = query; 1 = response
message << 1
message |= header_qr
header_opcode = 0 # 0 for standard: 4 bit
message << 4
message |= header_opcode
header_aa = 0 # authoritative answer: 1 bit
message << 1
message |= header_aa
header_tc = 0 # truncation due to long message: 1 bit
message << 1
message |= header_tc
header_rd = 0 # recursion desired: 1 bit
message << 1
message |= header_rd
header_ra = 0 # recursion available: 1 bit
message << 1
message |= header_ra
header_z = 0 # 3 bit nothing
message << 3
message |= header_qr
header_rcode = 0 # response code: 4 bit
message << 4
message |= header_rcode
header_qdcount = 1 # number of question entries
message << 16
message |= header_qdcount
header_ancount = 0 # number of RR in answer section
message << 16
message |= header_ancount
header_nscount = 0 # number of NS RR in authority records section
message << 16
message |= header_nscount
header_arcount = 0 # number of RR in additional records section
message << 16
message |= header_arcount

# Question Fields
# QNAME tokenizing + parsing
hostname_split = cli_hostname.split(".")
for i in len(hostname_split):
    message << 8
    message |= len(hostname_split[i])
    
    for j in len(hostname_split[i]):
        message << 8
        message |= ord(hostname_split[i][j]) # ascii value of character
            
    message << 8 # a 0 byte shows that message reached the end of QNAME

question_qtype = 1
message << 16
message |= question_qtype
question_qclass = 0
message << 16
message |= question_qclass


# DNS Responses
answer_name = 0
answer_type = 0
answer_class = 0
answer_ttl = 0
answer_rdlength = 0
answer_rdata = 0

print("Contacting DNS server..")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_socket.settimeout(1)
udp_host = socket.gethostname() # client hostname
udp_server = "8.8.8.8" # server socket will attempt to connect to
udp_port = 53 # DNS Server port is 53
print("client hostname:",udp_host)
print("socket server hostname:",udp_server)
print("socket port:",udp_port)
start_time = time.time() # setting start time
while (attempts < 3 and time.time() < start_time+5): # within 3 attempts AND less than 5 seconds elapsed
    attempts += 1
    print("Sending DNS query..:",attempts)
    try:
        udp_socket.sendto(message, (udp_server, udp_port)) # sends a message to specified server hostname and port
    except socket.error as err:
        print("Remote host rejected connection:",err)
    

    try:
        data, udp_server = udp_socket.recvfrom(udp_port) # receive message from port
        print("DNS response received (attempt",attempts,"of 3)")
        print("Processing DNS response..")
        header_id = data # TODO bitwise every header field
        print("----------------------------------------------------------------------------")
        print("header.ID =",header_id)
        print("header.QR =",header_qr)
        print("header.OPCODE =",header_opcode)
        print("header.AA =",header_aa)
        print("header.TC =",header_tc)
        print("header.RD =",header_rd)
        print("header.RA =",header_ra)
        print("header.Z =",header_z)
        print("header.RCODE =",header_rcode)
        print("header.QDCOUNT =",header_qdcount)
        print("header.ANCOUNT =",header_ancount)
        print("header.NSCOUNT =",header_nscount)
        print("header.ARCOUNT =",header_arcount)

        print("question.QNAME =",question_qname)
        print("question.QTYPE =",question_qtype)
        print("question.QCLASS =",question_qclass)

        print("answer.NAME =",answer_name)
        print("answer.TYPE =",answer_type)
        print("answer.CLASS =",answer_class)
        print("answer.TTL =",answer_ttl)
        print("answer.RDLENGTH =",answer_rdlength)
        print("answer.RDATA =",answer_rdata)

        # TODO include authority and additional RRs received

    except socket.timeout as err:
        print("DNS query timed out",err)
    except socket.error as err:
        print("Socket receive error:",err)
