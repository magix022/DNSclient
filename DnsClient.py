import sys
import socket
import time
import re
from DnsRequest import createHeader, createQuestion, buildReq
from DnsResponse import DnsResponse

queryT = "A"
port = 53
maxEntr =3
timeoutTime = 5
target = bytearray()
targetName = ""
addr = ""
currentAttempts=1

def send():
    global queryT, port, maxEntr, timeoutTime, target, targetName, addr, currentAttempts
    try:
        if(currentAttempts>maxEntr):
            print("ERROR    Maximum number of retries ["+str(maxEntr)+"] exceeded")
            return
        if(currentAttempts==1):
            if(queryT=="A"):
                print("DnsClient sending request for " + targetName +
                    "\n"+ "Server: ["+addr+"]\n"+"Request type: [A]")
            if(queryT=="MX"):
                print("DnsClient sending request for " + targetName +
                    "\n"+ "Server: ["+addr+"]\n"+"Request type: [MX]")
            if(queryT=="NS"):
                print("DnsClient sending request for " + targetName +
                    "\n"+ "Server: ["+addr+"]\n"+"Request type: [NS]")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeoutTime)
        s.connect((addr, port))
        req = buildReq(targetName, queryT)
        #print(req)
        ## calculate time for receiving response
        response_time = time.time()
        sent = s.send(req)
        answer = s.recv(4096)
        #print(answer)
        response_time = time.time() - response_time
        response = DnsResponse(answer)
        print("Response received after "+str(response_time)+" seconds ("+str(currentAttempts-1)+" retries)\n")
        response.output()




        s.settimeout(None)

        
    except socket.herror:
        print("ERROR    An error occured with the entered address.")
    except socket.timeout:
        print("ERROR    The connection timed out. Retrying.")
        currentAttempts+=1
        send()
    except socket.error:
        print("ERROR    A socket error occured.")
     

def parseArgs():
    global queryT, port, maxEntr, timeoutTime, target, targetName, addr, currentAttempts
    expecting_int = False
    for i in range(len(sys.argv)):
        match sys.argv[i]:
            case "-ns": 
                queryT = "NS"
            case "-mx":
                queryT = "MX"
            case "-p":
                port = int(sys.argv[i+1])
                expecting_int = True
            case "-r":
                maxEntr = int(sys.argv[i+1])
                expecting_int = True
            case "-t":
                timeoutTime=int(sys.argv[i+1])
                expecting_int = True
            case default:
                if expecting_int:
                    expecting_int = False
                    continue
                pattern = r'-.*'
                if re.match(pattern, sys.argv[i]) and i != 0:
                    raise Exception("ERROR  Unknown flag ["+sys.argv[i]+"]")
                if "@" in sys.argv[i]:
                    addr = sys.argv[i].split("@")[1]
                    numbers = addr.split(".")
                    for index in range(len(numbers)):
                        num = int(numbers[index])
                        if num < 0 or num >255:
                            raise Exception("ERROR  Incorrect IP address syntax [numbers must be between 0 and 255]")
                        target.append(num.to_bytes(1, byteorder='big')[0])
                    targetName = sys.argv[i+1]

if __name__ == "__main__":
    try:
        parseArgs()
        #print(createQuestion(targetName, queryT))
        ##print(buildReq(targetName, queryT))
        send()
    except Exception as e:
        print(e)
        exit(1)
    


                






