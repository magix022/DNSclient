from DnsHeader import DnsHeader
from DnsQuestion import DnsQuestion
from DnsAnswer import DnsAnswer

class DnsResponse:

    def __init__(self, dataBuffer):
        self.dataBuffer = dataBuffer
        self.lenght = len(dataBuffer)
        self.header = DnsHeader(dataBuffer[0:12])
        self.question = DnsQuestion(dataBuffer[12:])
        index = 12 + self.question.get_length()
        self.answer = []
        self.additional = []
        self.authority = []
        for i in range(self.header.get_ancount()):
            self.answer.append(DnsAnswer(dataBuffer[index:], dataBuffer, self.header.get_aa()))
            index += self.answer[i].get_length()
        if(self.header.get_nscount() != 0):
            for i in range(self.header.get_nscount()):
                self.authority.append(DnsAnswer(dataBuffer[index:], dataBuffer, self.header.get_aa()))
                index += self.authority[i].get_length()
            if(self.header.get_arcount() != 0):
                for i in range(self.header.get_arcount()):
                    self.authority.append(DnsAnswer(dataBuffer[index:], dataBuffer, self.header.get_aa()))
                    index += self.authority[i].get_length()
        else:
            if(self.header.get_arcount() != 0):
                for i in range(self.header.get_arcount()):
                    self.authority.append(DnsAnswer(dataBuffer[index:], dataBuffer, self.header.get_aa()))
                    index += self.authority[i].get_length()

    def get_bit(byte, position):
        return (byte >> position) & 1

    def output(self):
        ##ANSWER
        if self.header.get_ancount() == 0:
            print("NOTFOUND")
        else:
            print("***Answer Section ("+str(int.from_bytes(self.header.ancount, byteorder='big'))+" records)***\n")
            # print(self.answer.get_resource(self.header.get_ancount()))
            for i in range(self.header.get_ancount()):
                print(self.answer[i].get_resource())

        ##ADDITONAL
        if self.header.get_arcount() != 0:
            print("***Additional Section ("+str(int.from_bytes(self.header.arcount, byteorder='big'))+" records)***\n")
            print(self.additional.get_resource(self.header.get_arcount()))
        
        

