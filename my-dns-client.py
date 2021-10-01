import sys
import time
import socket

cli_hostname = sys.argv[1] # hostname argument given by command line
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

# DNS Responses
answer_name = None
answer_type = None
answer_class = None
answer_ttl = None
answer_rdlength = None
answer_rdata = None

print("Contacting DNS server..")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initializing socket as UDP (DGRAM)
udp_host = socket.gethostname() # client hostname
udp_server = cli_hostname # server socket will attempt to connect to
udp_port = 53 # DNS Server port is 53
print("client hostname:",udp_host)
print("socket server hostname:",udp_server)
print("socket port:",udp_port)
start_time = time.time() # setting start time
while (attempts <= 3 and time.time() < start_time+5): # within 3 attempts AND less than 5 seconds elapsed
    attempts += 1
    print("Sending DNS query..:",attempts)
    try:
        udp_socket.sendto(message, (udp_server, udp_port))
    except socket.error as err:
        print("Remote host rejected connection:",err)
    try:
        data, udp_server = udp_socket.recvfrom(53)
        print("DNS response received (attempt",attempts,"of 3)")
        print("Processing DNS resopnse..")
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

    except socket.timeout as err:
        print("DNS query timed out",err)
    except socket.error as err:
        print("Socket receive error:",err)
