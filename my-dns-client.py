import sys
import time
import socket

cli_hostname = sys.argv[1] # hostname argument given by command line
message = 0 # the message to send through socket
message_size = 0 # size of message in bits
data = 0 # the message to receive from socket
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket


print("Preparing DNS query..")

# Header Fields
header_id = 170 # start with id 0: 16 bits
message |= header_id
message_size += 16
header_qr = 0 # 1 bit: 0 = query; 1 = response
message = message << 1
message_size += 1
message |= header_qr
header_opcode = 0 # 0 for standard: 4 bit
message = message << 4
message_size += 4
message |= header_opcode
header_aa = 0 # authoritative answer: 1 bit
message = message << 1
message_size += 1
message |= header_aa
header_tc = 0 # truncation due to long message: 1 bit
message = message << 1
message_size += 1
message |= header_tc
header_rd = 0 # recursion desired: 1 bit
message = message << 1
message_size += 1
message |= header_rd
header_ra = 0 # recursion available: 1 bit
message = message << 1
message_size += 1
message |= header_ra
header_z = 0 # 3 bit nothing
message = message << 3
message_size += 3
message |= header_qr
header_rcode = 0 # response code: 4 bit
message = message << 4
message_size += 4
message |= header_rcode
header_qdcount = 1 # number of question entries
message = message << 16
message_size += 16
message |= header_qdcount
header_ancount = 0 # number of RR in answer section
message = message << 16
message_size += 16
message |= header_ancount
header_nscount = 0 # number of NS RR in authority records section
message = message << 16
message_size += 16
message |= header_nscount
header_arcount = 0 # number of RR in additional records section
message = message << 16
message_size += 16
message |= header_arcount

# Question Fields
# QNAME tokenizing + parsing
hostname_split = cli_hostname.split(".")
for i in hostname_split:
    message = message << 8
    message_size += 8
    message |= len(i)
    
    for j in i:
        message = message << 8
        message_size += 8
        message |= ord(j) # ascii value of character
            
    message << 8 # a 0 byte shows that message reached the end of QNAME
    message_size += 8

question_qtype = 1
message = message << 16
message_size += 16
message |= question_qtype
question_qclass = 0
message = message << 16
message_size += 16
message |= question_qclass

print(message)


# DNS Responses
answer_name = 0
answer_type = 0
answer_class = 0
answer_ttl = 0
answer_rdlength = 0
answer_rdata = 0

print("Contacting DNS server..")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_socket.settimeout(2)
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
        udp_socket.sendto(message.to_bytes(message_size, byteorder='big'), (udp_server, udp_port)) # sends a message to specified server hostname and port
    except socket.error as err:
        print("Remote host rejected connection:",err)
    

    try:
        data, udp_server = udp_socket.recvfrom(udp_port) # receive message from port
        print("DNS response received (attempt",attempts,"of 3)")
        print("Processing DNS response..")
        header_id = int.from_bytes(data[0:2],'big')
        header_qr = int.from_bytes(data[2:3],'big')
        header_opcode = int.from_bytes(data[3:7],'big')
        header_aa = int.from_bytes(data[7:8],'big')
        header_tc = int.from_bytes(data[8:9],'big')
        header_rd = int.from_bytes(data[9:10],'big')
        header_ra = int.from_bytes(data[10:11],'big')
        header_z = int.from_bytes(data[11:14],'big')
        header_rcode = int.from_bytes(data[14:18],'big')
        header_qdcount = int.from_bytes(data[18:24],'big')
        header_ancount = int.from_bytes(data[24:40],'big')
        header_nscount = int.from_bytes(data[40:56],'big')
        header_arcount = int.from_bytes(data[56:72],'big')

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

        print("question.QNAME =")
        print("question.QTYPE =",question_qtype)
        print("question.QCLASS =",question_qclass)

        print("answer.NAME =",answer_name)
        print("answer.TYPE =",answer_type)
        print("answer.CLASS =",answer_class)
        print("answer.TTL =",answer_ttl)
        print("answer.RDLENGTH =",answer_rdlength)
        print("answer.RDATA =",answer_rdata)
        print("----------------------------------------------------------------------------")

        # TODO include authority and additional RRs received

        break

    except socket.timeout as err:
        print("DNS query timed out")
    except socket.error as err:
        print("Socket receive error")
