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

# Get the ADS type and port number and input file name from the command line
type = str(sys.argv[1])
PortNum = int(sys.argv[2])
file = str(sys.argv[3])

# Read the input file and store the IP addresses of the ADS servers
fd = open(file, 'r')
lines = fd.readlines()
fd.close()

#ADS IP addresses are stored in ADS_IP
counter = -1
ADS_IP = []
for line in lines:
    counter += 1
    if(counter >= 5 and counter <= 10):
        ADS_IP.append(line.split()[1])
    if(counter > 10):
        break

#IP_INADS stores the IP addresses of the Domain Name (eg:www.bank.com) and the ADS server type (eg:1,2,3,4,5,6)
#IP_INADS is a list of tuples of the form (Domain Name ,(IP_Address,ADS_Type))
flag = False 
startString = "List_of_ADS"+type
nextString = "List_of_ADS"+str(int(type)+1)
IP_INADS = []
for line in lines:
    if(line[0:12] == startString):
        flag = True
        continue
    if(line[0:12] == nextString or line[0:8] == "END_DATA"):
        break
    if(flag == True and line[0:12] != nextString and line[0:8] != "END_DATA"):
        IP_str = line.split()
        IP_INADS.append((IP_str[0],(IP_str[1],int(type))))

#GetIPPort function returns the IP address of the Domain Name and the ADS server type
#If the Domain Name is not found, it returns ("Not_Found",0)
def GetIPPort(ADS_Type,IP_INADS):
    for i in range(len(IP_INADS)):
        if(IP_INADS[i][0].strip() == ADS_Type.strip()):
            return (IP_INADS[i][1][0],IP_INADS[i][1][1])
    return ("Not_Found",0)

#Create a UDP socket and bind it to the port number given in the command line argument 
#The socket is used to receive the query from the NR server
#The socket is used to send the response to the NR server
#The response is IP Address of Requested Domain Name 
socket_NR = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_NR.bind((ADS_IP[int(type)-1],PortNum))

#Open the ADS.output.txt file in write mode and truncate the file to 0 bytes, this is done to clear the file contents if the file already exists 
#The file is used to store the ADS query and response
#The query is the Domain Name and the response is the IP address of the requested Domain Name
fdw = open("ADS.output.txt", 'w')
fdw.truncate(0)
fdw.close()
while True:
    #Open the ADS.output.txt file in append mode
    fdw = open("ADS.output.txt", 'a')
    #Receive the query from the NR server and decode it to get the Domain Name 
    input_encoded, NR_Address = socket_NR.recvfrom(1024)
    input_str = input_encoded.decode()
    ADS_Type_Add = input_str
    #If the query is "bye", break the loop and close the socket and file 
    if(ADS_Type_Add[0:3] == "bye"):
        break
    #Input Domain Name and NR Port Number is what we got from NR server as message
    #Split the message to get the Domain Name and NR Port Number 
    ADS_Type = ADS_Type_Add.split()[0]
    NR_PortNum = ADS_Type_Add.split()[1]

    #Get the IP address of the Domain Name and the ADS server type 
    value = GetIPPort(ADS_Type,IP_INADS)
    #If the Domain Name is not found, send the response as "Not_Found" to the NR server
    #Else, send the response as the IP address of the Domain Name to the NR server

    #ADS_PortNum is the port number of the ADS server to which the NR server has to send the query 
    ADS_PortNum = value[1] + 3 + int(NR_PortNum)

    #send the response to the NR server 
    socket_NR.sendto(value[0].encode(),NR_Address)

    #Write the query and response to the ADS.output.txt file
    fdw.write(f"ADS{type} (Query and response (IP_address)): ({ADS_Type}, {value[0]}) \n")
    #Close the ADS.output.txt file
    #we are opening and closing the file for every query and response to avoid the file being locked by the program since many programs will be writing to same file 
    fdw.close()
#Close the socket
socket_NR.close()

