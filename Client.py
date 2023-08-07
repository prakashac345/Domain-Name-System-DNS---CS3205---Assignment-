#  NAME: Prakash A
#  Roll Number: CS20B061
#  Course: CS3205 Jan. 2023 semester
#  Lab number: 2
#  Date of submission: 04/03/2023
#  I confirm that the source file is entirely written by me without
#  resorting to any dishonest means.

import os
import sys
import socket
import subprocess

localIP     = "127.0.0.1"
startPortNum = int(sys.argv[1])
file = str(sys.argv[2])

fd = open(file, 'r')
lines = fd.readlines()
fd.close()

#We are storing the IP addresses of all the servers in the following variables
counter = -1
NR_IP = ""
RDS_IP = ""
TDS_IP = []
ADS_IP = []
for line in lines:
    counter += 1
    if(counter == 1 or line.split()[0].strip() == "NR"):
        NR_IP = line.split()[1]
    if(counter == 2 or line.split()[0].strip() == "RDS"):
        RDS_IP = line.split()[1]
    if(counter == 3 or line[0:3] == "TDS"):
        TDS_IP.append(line.split()[1])
    if(counter == 4 or line[0:3] == "TDS"):
        TDS_IP.append(line.split()[1])
    if(counter >= 5 and counter <= 10):
        ADS_IP.append(line.split()[1])

#We are starting all the servers in the following lines
SP= subprocess.Popen(f"python NR.py {startPortNum + 53} inputfile.txt")
SP= subprocess.Popen(f"python RDS.py {startPortNum + 54} inputfile.txt")
SP= subprocess.Popen(f"python TDS.py 1 {startPortNum + 55} inputfile.txt")
SP= subprocess.Popen(f"python TDS.py 2 {startPortNum + 56} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 1 {startPortNum + 57} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 2 {startPortNum + 58} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 3 {startPortNum + 59} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 4 {startPortNum + 60} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 5 {startPortNum + 61} inputfile.txt")
SP= subprocess.Popen(f"python ADS.py 6 {startPortNum + 62} inputfile.txt")

#We are starting the client in the following lines
Socket_NR = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    input_server_name = input("Enter Server Name: ") #Input from the user
    #sending the input to the Name Resolver
    Socket_NR.sendto(input_server_name.encode(),(NR_IP,startPortNum + 53))

    #If the user enters bye, we are killing all the servers and exiting and breaking the loop 
    if input_server_name[0:3] == "bye": 
        print("All Server Processes are killed. Exiting.")
        Socket_NR.sendto(input_server_name.encode(),(RDS_IP,startPortNum + 54))
        Socket_NR.sendto(input_server_name.encode(),(TDS_IP[0],startPortNum + 55))
        Socket_NR.sendto(input_server_name.encode(),(TDS_IP[1],startPortNum + 56))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[0],startPortNum + 57))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[1],startPortNum + 58))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[2],startPortNum + 59))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[3],startPortNum + 60))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[4],startPortNum + 61))
        Socket_NR.sendto(input_server_name.encode(),(ADS_IP[5],startPortNum + 62))
        break

    #Receiving the IP address from the Name Resolver
    IP_encoded,NR_Address = Socket_NR.recvfrom(1024)
    IP = IP_encoded.decode()

    #Printing the IP address
    if(IP != "Not Found"):
        print(f"DNS Mapping: {IP}")
    else :
        print("No DNS Record Found")

#Closing the socket
Socket_NR.close()