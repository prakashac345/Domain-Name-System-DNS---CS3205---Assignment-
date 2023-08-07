#  NAME: Prakash A
#  Roll Number: CS20B061
#  Course: CS3205 Jan. 2023 semester
#  Lab number: 2
#  Date of submission: 04/03/2023
#  I confirm that the source file is entirely written by me without
#  resorting to any dishonest means.

import sys
import socket
import os

#getting the port number and file name from the command line
PortNum = int(sys.argv[1])
file = str(sys.argv[2])

#reading the file and storing the IP addresses of NR and RDS
fd = open(file, 'r')
lines = fd.readlines()
fd.close()
#storing the IP addresses of NR and RDS
counter = -1
NR_IP = ""
RDS_IP = ""
for line in lines:
    counter += 1
    if(counter == 1 or line.split()[0].strip() == "NR"):
        NR_IP = line.split()[1]
    if(counter == 2 or line.split()[0].strip() == "RDS"):
        RDS_IP = line.split()[1]
    if(counter > 2):
        break

#opening the file to write the queries and responses
fdw = open("NR.output.txt", "w")

#creating the socket for communication with the client
socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_client.bind((NR_IP,PortNum))

#creating the socket for communication with the RDS and TDS and ADS servers
socket_Gen = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
while(True):
    #receiving the input from the client
    input_server ,Address = socket_client.recvfrom(1024)
    input_server_name = input_server.decode()
    
    #checking if the input is bye
    #if yes, then break the loop
    if input_server_name == "bye":
        break

    #splitting the input so that we can get the TDL domain name from it and send it to the RDS server 
    #and we can also get the TDS IP address and port number from the RDS server
    #and we can also get which ADS server to send the query to
    input_names = input_server_name.split(".")

    #sending the TDL domain name to the RDS server
    socket_Gen.sendto(input_server_name.encode(),(RDS_IP,PortNum + 1))
    #receiving the TDS IP address and port number from the RDS server
    RDS_Value_encoded,RDS_Address = socket_Gen.recvfrom(1024)
    RDS_Value = RDS_Value_encoded.decode()
    #splitting the TDS IP address and port number
    TDS_IP = RDS_Value.split()[0]

    #checking if the TDS IP address is not found
    #if yes, then send the not found message to the client and continue the loop
    if(TDS_IP == "Not_Found"):
        socket_client.sendto("Not Found".encode(),Address)
        continue

    #getting the TDS port number
    TDS_PortNum = int(RDS_Value.split()[1])
    
    #sending the ADS domain name (eg: bank.com etc) to the TDS server to get the ADS IP address and port number
    socket_Gen.sendto((input_server_name + " " + str(PortNum)).encode(),(TDS_IP,TDS_PortNum))
    #receiving the ADS IP address and port number from the TDS server
    ADS_Value_encoded,TDS_Address = socket_Gen.recvfrom(1024)
    ADS_Value = ADS_Value_encoded.decode()
    #splitting the ADS IP address and port number
    ADS_IP = ADS_Value.split()[0]

    #checking if the ADS IP address is not found
    #if yes, then send the not found message to the client and continue the loop
    if(ADS_IP == "Not_Found"):
        socket_client.sendto("Not Found".encode(),Address)
        continue

    #getting the ADS port number
    ADS_PortNum = int(ADS_Value.split()[1])
    
    #sending the ADS domain name (eg: bank.com etc) to the ADS server to get the IP address of the input domain name (eg: www.bank.com) 
    socket_Gen.sendto((input_server_name + " " + str(PortNum)).encode(),(ADS_IP,ADS_PortNum))
    #receiving the IP address of the input domain name (eg: www.bank.com) from the ADS server
    IP_Value_encoded,ADS_Address = socket_Gen.recvfrom(1024)
    IP_Value = IP_Value_encoded.decode()
    #splitting the IP address
    IP = IP_Value.split()[0]

    #checking if the IP address is not found
    #if yes, then send the not found message to the client and continue the loop
    if(IP == "Not_Found"):
        socket_client.sendto("Not Found".encode(),Address)
        continue

    #writing the query and response to the file
    fdw.write(f"Query From Client: {input_server_name} and Response : {IP} \n")
    
    #sending the IP address of the input domain name (eg: www.bank.com) to the client
    socket_client.sendto(IP.encode(),Address) 
#closing the sockets and the file
socket_client.close()
socket_Gen.close()
fdw.close()