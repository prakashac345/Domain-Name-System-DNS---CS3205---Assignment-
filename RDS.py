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

#reading the file and storing the IP addresses of RDS 
fd = open(file, 'r')
lines = fd.readlines()
fd.close()

#storing the IP address of RDS
counter = -1
RDS_IP = ""
for line in lines:
    counter += 1
    if(counter == 2 or line.split()[0].strip() == "RDS"):
        RDS_IP = line.split()[1]
    if(counter > 2):
        break

#RDS_List contains the TDL_Domain and the TDS_IP and TDS_Port Number
RDS_List = []
cnt = 0
for line in lines:
    if(line[0:3] == "TDS"):
        TDS_str = line.split()
        TDL_Domain = TDS_str[0].split("_")
        if(cnt == 0 or TDL_Domain[1] == "com"):
            RDS_List.append((TDL_Domain[1],(TDS_str[1],PortNum + 1)))
        else :
            RDS_List.append((TDL_Domain[1],(TDS_str[1],PortNum + 2)))
        cnt += 1
    if(cnt > 1):
        break

#function to get the TDS_IP and TDS_Port Number from the RDS_List for a given TDL_Domain(input_domain) 
#returns the TDS_IP and TDS_Port Number if found else returns "Not_Found" and 0
def GetIPPort(input_domain,RDS_List):
    TDL_Domain = input_domain
    for i in range(len(RDS_List)):
        if(RDS_List[i][0].strip() == TDL_Domain.strip()):
            return (RDS_List[i][1][0],RDS_List[i][1][1])
    return ("Not_Found",0)

#opening the file to write the queries and responses 
fdw = open("RDS.output.txt", 'w')

#creating the socket and binding it to the RDS_IP and PortNum 
socket_NR = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_NR.bind((RDS_IP,PortNum))
while True:
    #receiving the query from the NR 
    input_domain_T_encoded,NR_Address = socket_NR.recvfrom(1024)
    input_domain_T = input_domain_T_encoded.decode()

    #if the query is bye then break the loop and close the socket and file
    if(input_domain_T[0:3] == "bye"):
        break

    #getting the TDL_Domain from the query since the query will be of form, eg: "www.google.com" and what we want is "com" to search in the RDS_List 
    # and then getting the TDS_IP and TDS_Port Number from the RDS_List
    input_domain = input_domain_T.split(".")[2]
    value = GetIPPort(input_domain,RDS_List)

    #sending the response to the NR (TDS_IP and TDS_Port Number) 
    socket_NR.sendto((value[0] + " " + str(value[1])).encode(),NR_Address)

    #writing the query and response to the file 
    fdw.write(f"RDS (Query , Response(TDS_IP_Adress, TDS_Port Number)) : ({input_domain} , ({value[0]} {value[1]})) \n")

#closing the socket and file
socket_NR.close()
fdw.close()

