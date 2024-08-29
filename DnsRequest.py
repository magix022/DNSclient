from random import randbytes
from DnsHeader import DnsHeader

def createHeader():
    head = bytearray(12)

    #ID
    head[0] = randbytes(1)[0]
    head[1] = randbytes(1)[0]

    oneInHex = '0x01'
    zeroInHex = '0x00'

    #QR to RD
    head[2] = bytes.fromhex(oneInHex[2:])[0]
    #RA to RCODE
    head[3] = bytes.fromhex(zeroInHex[2:])[0]

    #QDCOUNT
    head[4] = bytes.fromhex(zeroInHex[2:])[0]
    head[5] = bytes.fromhex(oneInHex[2:])[0]

    #ANCOUNT
    head[6] = bytes.fromhex(zeroInHex[2:])[0]
    head[7] = bytes.fromhex(zeroInHex[2:])[0]

    #NSCOUNT
    head[8] = bytes.fromhex(zeroInHex[2:])[0]
    head[9] = bytes.fromhex(zeroInHex[2:])[0]

    #ARCOUNT
    head[10] = bytes.fromhex(zeroInHex[2:])[0]
    head[11] = bytes.fromhex(zeroInHex[2:])[0]

    return head

def createQuestion(target, queryT):
    length =0
    oneInHex = '0x01'
    zeroInHex = '0x00'
    twoInHex = '0x02'
    fHex = '0x0f'

    strs = target.split(".")

    for stri in strs:
        length+=len(stri) + 1

    question = bytearray(length + 5)

    index=0
    for stri in strs:
        question[index]=len(stri)
        index+=1
        for char in stri:
            question[index]=char.encode('ascii')[0]
            index+=1

    #zero octect after domain name
    question[index]=0

    #QNAME
    match queryT:
        case "A":
            question[index+1] = bytes.fromhex(zeroInHex[2:])[0]
            question[index+2] = bytes.fromhex(oneInHex[2:])[0]
        case "NS":
            question[index+1] = bytes.fromhex(zeroInHex[2:])[0]
            question[index+2] = bytes.fromhex(twoInHex[2:])[0]
        case "MX":
            question[index+1] = bytes.fromhex(zeroInHex[2:])[0]
            question[index+2] = bytes.fromhex(fHex[2:])[0]
    
    #QCLASS
    question[index+3] = bytes.fromhex(zeroInHex[2:])[0]
    question[index+4] = bytes.fromhex(oneInHex[2:])[0]

    return question


def buildReq(target, queryT):

    strs = target.split(".")
    length=0
    for stri in strs:
        length+=1+len(stri)
    
    #total lenght of request
    length += 12 +5

    req = bytearray(length)

    head = createHeader()
    ques = createQuestion(target,queryT)

    for i in range(len(head)):
        req[i]=head[i]
    for i in range(len(ques)):
        req[i+len(head)]=ques[i]
    
    return req
            








        



