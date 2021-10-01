import sys
import time
import socket

cli_hostname = sys.argv[1] # hostname argument given by command line
message = b"" # the message to send through socket
data = b"" # the message to receive from socket
static_id = 1;
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket


print("Preparing DNS query..")

class Header:
    def __init__(self, header_id, header_qr, header_opcode, header_aa, header_tc, header_rd, header_ra, header_z, header_rcode, header_qdcount, header_ancount, header_nscount, header_arcount):
        # Header Fields
        self.header_id = header_id
        self.header_qr = header_qr
        self.header_opcode = header_opcode
        self.header_aa = header_aa
        self.header_tc = header_tc
        self.header_rd = header_rd
        self.header_ra = header_ra
        self.header_z = header_z
        self.header_rcode = header_rcode
        self.header_qdcount = header_qdcount
        self.header_ancount = header_ancount
        self.header_nscount = header_nscount
        self.header_arcount = header_arcount

class Question:
    def __init__(self, question_qname, question_qtype, question_qclass):
        # Question Fields
        self.question_qname = question_qname
        self.question_qtype = question_qtype
        self.question_qclass = question_qclass

class Record:
    def __init__(self, answer_name, answer_type, answer_class, answer_ttl, answer_rdlength, answer_rdata):
        # DNS Responses
        self.answer_name = answer_name
        self.answer_type = answer_type
        self.answer_class = answer_class
        self.answer_ttl = answer_ttl
        self.answer_rdlength = answer_rdlength
        self.answer_rdata = answer_rdata


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
