import sys
import time
import socket

cli_hostname = sys.argv[1] # hostname argument given by command line
message = [] # the message to send through socket
data = 0 # the message to receive from socket
start_time = 0.0 # start time from beginning of socket send attempts
attempts = 0 # number of times attempted to send message through socket


print("Preparing DNS query..")

# Header Fields
header_id = 1 # start with id 1: 16 bits
message.append(0x0)
message.append(0x1)
header_qr = 0 # 1 bit: 0 = query; 1 = response
header_opcode = 0 # 0 for standard: 4 bit
header_aa = 0 # authoritative answer: 1 bit
header_tc = 0 # truncation due to long message: 1 bit
header_rd = 0 # recursion desired: 1 bit
message.append(0x0)
header_ra = 0 # recursion available: 1 bit
header_z = 0 # 3 bit nothing
header_rcode = 0 # response code: 4 bit
message.append(0x0)
header_qdcount = 1 # number of question entries
message.append(0x0)
message.append(0x1)
header_ancount = 0 # number of RR in answer section
message.append(0x0)
message.append(0x0)
header_nscount = 0 # number of NS RR in authority records section
message.append(0x0)
message.append(0x0)
header_arcount = 0 # number of RR in additional records section
message.append(0x0)
message.append(0x0)

# Question Fields
# QNAME tokenizing + parsing
hostname_split = cli_hostname.split(".")
for i in hostname_split:
    message.append(len(i))
    
    for j in i:
        message.append(ord(j)) # ascii value of character
            
message.append(0x0) # a 0 byte shows that message reached the end of QNAME

question_qtype = 1
message.append(0x0)
message.append(0x1)
question_qclass = 1 # 0x0001 for Internet Address (IN)
message.append(0x0)
message.append(0x1)

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
# print("client hostname:",udp_host)
# print("socket server hostname:",udp_server)
# print("socket port:",udp_port)
start_time = time.time() # setting start time
while (attempts < 3 and time.time() < start_time+5): # within 3 attempts AND less than 5 seconds elapsed
    attempts += 1
    print("Sending DNS query..")
    try:
        udp_socket.sendto(bytes(message), (udp_server, udp_port)) # sends a message to specified server hostname and port
    except socket.error as err:
        print("Remote host rejected connection:",err)
    

    try:
        data, udp_server = udp_socket.recvfrom(udp_port) # receive message from port
        print("DNS response received (attempt",attempts,"of 3)")
        print("Processing DNS response..")
        header_id = int.from_bytes(data[0:2],'big')
        header_qr = int.from_bytes(data[2:3],'big') >> 7
        header_opcode = (int.from_bytes(data[2:3],'big') >> 3) & 15
        header_aa = (int.from_bytes(data[2:3],'big') >> 2) & 1
        header_tc = (int.from_bytes(data[2:3],'big') >> 1) & 1
        header_rd = int.from_bytes(data[3:4],'big') & 1
        header_ra = int.from_bytes(data[3:4],'big') >> 7
        header_z = (int.from_bytes(data[3:4],'big') >> 4) & 7
        header_rcode = int.from_bytes(data[3:4],'big') & 15
        header_qdcount = int.from_bytes(data[4:6],'big')
        header_ancount = int.from_bytes(data[6:8],'big')
        header_nscount = int.from_bytes(data[8:10],'big')
        header_arcount = int.from_bytes(data[10:12],'big')

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

        offset = 12
        for i in range(header_qdcount):
            qname_response = ""
            while(data[offset] != 0x0):
                letter_count = data[offset]
                offset += 1
                for j in range(letter_count):
                    qname_response += chr(data[offset])
                    offset += 1
                qname_response += '.'
            print("question.QNAME=",qname_response[:-1])
            offset += 1

        question_qtype = int.from_bytes(data[offset:offset+2],'big')
        print("question.QTYPE =",question_qtype)
        offset += 2
        question_qclass = int.from_bytes(data[offset:offset+2],'big')
        print("question.QCLASS =",question_qclass)
        offset += 2


        for i in range(header_ancount):
            # while (offset >= len(data) or data[offset] != 0x0):
            #     answer_name += data[offset]
            #     offset += 2
            # print("answer.NAME =",answer_name)
            # offset += 2
            print (data[offset:])
            print (offset)
            answer_name = ""
            while(data[offset] != 0x0):
                letter_count = data[offset]
                print("LETTER COUNT:",letter_count)
                offset += 1
                for j in range(letter_count):
                    answer_name += chr(data[offset])
                    offset += 1
                answer_name += '.'
            print("answer.NAME =",answer_name[:-1])
            offset += 1

            answer_type = int.from_bytes(data[offset:offset+2],'big')
            print("answer.TYPE =",answer_type)
            offset += 2

            answer_class = int.from_bytes(data[offset:offset+2],'big')
            print("answer.CLASS =",answer_class)
            offset += 2

            answer_ttl = int.from_bytes(data[offset:offset+4],'big')
            print("answer.TTL =",answer_ttl)
            offset += 4

            answer_rdlength = int.from_bytes(data[offset:offset+2],'big')
            print("answer.RDLENGTH =",answer_rdlength)
            offset += 2
            
            answer_rdata = ""
            answer_rdata += data[offset] + "."
            answer_rdata += data[offset+1] + "."
            answer_rdata += data[offset+2] + "."
            answer_rdata += data[offset+3] + "."
            print("answer.RDATA =",answer_rdata)
            offset += 4

        # for i in range(header_nscount):
        #     while (data[offset] != bytes([0x0])):
        #         answer_name += data[offset].decode('ascii')
        #         offset += 2
        #     print("answer.NAME =",answer_name)
        #     offset += 2

        #     answer_type = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.TYPE =",answer_type)
        #     offset += 2

        #     answer_class = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.CLASS =",answer_class)
        #     offset += 2

        #     answer_ttl = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.TTL =",answer_ttl)
        #     offset += 2

        #     answer_rdlength = int.from_bytes(data[offset:offset+4],'big')
        #     print("answer.RDLENGTH =",answer_rdlength)
        #     offset += 4
            
        #     answer_rdata = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.RDATA =",answer_rdata)
        #     offset += 2

        # for i in range(header_arcount):
        #     while (data[offset] != bytes([0x0])):
        #         answer_name += data[offset].decode('ascii')
        #         offset += 2
        #     print("answer.NAME =",answer_name)
        #     offset += 2

        #     answer_type = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.TYPE =",answer_type)
        #     offset += 2

        #     answer_class = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.CLASS =",answer_class)
        #     offset += 2

        #     answer_ttl = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.TTL =",answer_ttl)
        #     offset += 2

        #     answer_rdlength = int.from_bytes(data[offset:offset+4],'big')
        #     print("answer.RDLENGTH =",answer_rdlength)
        #     offset += 4
            
        #     answer_rdata = int.from_bytes(data[offset:offset+2],'big')
        #     print("answer.RDATA =",answer_rdata)
        #     offset += 2

        print("----------------------------------------------------------------------------")

        # TODO include authority and additional RRs received

        break

    except socket.timeout as err:
        print("DNS query timed out")
    except socket.error as err:
        print("Socket receive error")
