# Domain-Name-System-DNS---CS3205---Assignment-
DNS Implementation in Python 
LAB-2 : Simple DNS Server
Objective: Implement a simple hierarchical Domain Name Server (DNS) system, with a client and a set of relevant DNS servers.

This Assignment Submission has 5 Source files(.py files) , 
But only has to RUN Client.py for the complete execution of the program.
Make sure that all the 5 files are in the same directory.

To Run Client.py Code 
Open a terminal run :
(Only in Windows)
In Windows: python Client.py <Port_Number> <Inputfile_name> 
eg: py Client.py 1400 inputfile.txt

(It is assumed that the python3 or py command is added to the path variable of the system)
(Suggestion <Port_Number> should be greater than 1024)

----------------------------------------------------------------------------------------------------
After Running the above commands in terminal, 
A message will be displayed as "Enter Server Name: " where ,
we have enter the server name for which we want to find its IP address.

After entering the server name, 
"DNS Mapping: <IP_Address>" the IP address of the server will be displayed in the terminal,
if, the entered Server Name is present in DNS Severs.
else , "No DNS Record Found" will be displayed in the terminal.
To terminal the program, enter "bye" in the place of server name.
The message "All Server Processes are killed. Exiting." will be displayed in the terminal.
and the program will be terminated.

----------------------------------------------------------------------------------------------------
// Read The Following Instructions Carefully For Better Understanding Of The X.output.txt files. //
After finishing the execution of the program,
the output files will be generated in the same directory as Client.py file, which are:
1. NR.output.txt which containes queries and response made by NR Server to other Servers , as well as from Client to NR Server.
2. RDS.output.txt which containes queries and response made to RDS Server from NR Server.
3. TDS.output.txt which containes queries and response made to TDS Server from NR Server.
4. ADS.output.txt which containes queries and response made to ADS Server from NR Server.

Even Though we will send the whole input_server_name and NR_Port_Number as a query from NR Server to other Servers,
but the output files will contain only the required query for which the a particular server is responsible and the response made by that server.

eg :
The query made by NR Server to RDS Server is : "com" or "edu" response is <TDS_IP_Adress, TDS_Port Number>
The query made by NR Server to TDS Server is : "mynah.edu" or "bank.com" response is <ADS_IP_Adress, ADS_Port Number>
The query made by NR Server to ADS Server is : "ftp.mynah.edu" or "www.bank.com" response is <IP_Address of Requested Server Name>
The NR.output.txt file will contain the queries and responses made to other Servers from NR Server as well as from Client to NR Server.

eg:
In ADS.output.txt file , the queries and responses made to ADS Server from NR Server are displayed in the following format:
<ADS<i>> (Query and response (IP_address)): (<Query>, <IP Address of Requested Server NameResponse>)
eg: ADS4 (Query and response (IP_address): (ftp.mynah.edu, 198.167.5.3))


Since I wrote my code in windows , my code can be run in windows only. and so i can't provide the Script files 
