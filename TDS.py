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

# Get the TDS type and port number and input filename from the command line arguments
type = int(sys.argv[1])
PortNum = int(sys.argv[2])
file = str(sys.argv[3])

# Open the input file and read the lines
fd = open(file, 'r')
lines = fd.readlines()
fd.close()

# Get the TDS IP addresses from the input file and store them in a list of strings (TDS_IP) 
# we are getting the TDS IP addresses so that we can bind the socket to the correct IP address based on the TDS type
counter = -1
TDS_IP = []
for line in lines:
    counter += 1
    if(counter == 3 or line[0:3] == "TDS"):
        TDS_IP.append(line.split()[1])
    if(counter == 4 or line[0:3] == "TDS"):
        TDS_IP.append(line.split()[1])
    if(counter > 4):
        break

# Get the ADS Domain Name (eg: bank.com) , ADS IP addresses and ADS_Server_No (eg:1,2,3,4,5,6) from the input file and store them in a list of tuples (ADS_IP)
# we are getting the ADS IP addresses and port numbers so that we can send the ADS name and port number to NR Server as Response to its request
counter = 0
ADS_IP = []
for line in lines:
    counter += 1
    if(counter >= 6 and counter <= 11):
        ADS_str = line.split()
        ADS_IP.append((ADS_str[0],(ADS_str[1],counter-5)))
    if(counter > 11):
        break

# Get the ADS_IP address and ADS_Server_No of the ADS based on the ADS DNS name 
def GetIPPort(ADS_Name,ADS_IP):
    for i in range(len(ADS_IP)):
        if(ADS_IP[i][0].strip() == ADS_Name.strip()):
            return (ADS_IP[i][1][0],ADS_IP[i][1][1])
    return ("Not_Found",0)

# Open the output file and truncate it to 0 bytes and close it , This is done so that the output file is empty before we write to it
fdw = open("TDS.output.txt", 'w')
fdw.truncate(0)
fdw.close()

# Create a UDP socket and bind it to the TDS IP address and port number
socket_NR = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_NR.bind((TDS_IP[type-1],PortNum))
while True:
    #Open the output file in append mode 
    # read the input from the NR Server
    fdw = open("TDS.output.txt", 'a')

    #input is of form (eg : www.bank.com NR_PortNum)
    input_encoded, NR_Address = socket_NR.recvfrom(1024) 
    input_value = input_encoded.decode()
    ADS_Name_Add = input_value

    # If the input is bye then break the loop and close the socket
    if(ADS_Name_Add[0:3] == "bye"):
        break

    #Get the ADS Domain Name (eg: bank.com) from input which is of form (eg : www.bank.com NR_PortNum)
    ADS_Name = ADS_Name_Add.split()[0].split(".")[1] +"."+ ADS_Name_Add.split()[0].split(".")[2]
    NR_PortNum = ADS_Name_Add.split()[1]

    #Get the ADS IP address and ADS_Server_No of the ADS based on the ADS DNS name
    value = GetIPPort(ADS_Name,ADS_IP)

    #ADS_PortNum is calculated as 3 + NR_PortNum + ADS_Server_No since the ADS Server port numbers are 3 more than the NR Server port numbers + ADS_Server_No (eg: 1,2,3,4,5,6)
    ADS_PortNum = value[1] + 3 + int(NR_PortNum)

    #Send the ADS IP address and ADS_PortNum to the NR Server as Response to its request 
    socket_NR.sendto((value[0] + " " + str(ADS_PortNum)).encode(),NR_Address)

    #write the query and response to the output file
    fdw.write(f"TDS{type} Server (Query , Respose (ADS_IP_Address, ADS_Port Number)) : ({ADS_Name} , ({value[0]} , {ADS_PortNum})) \n")
    #Close the ADS.output.txt file
    #we are opening and closing the file for every query and response to avoid the file being locked by the program since many programs will be writing to same file 
    fdw.close()

#Close the socket
socket_NR.close()

