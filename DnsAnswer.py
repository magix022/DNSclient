class DnsAnswer:
    def __init__(self, answer, data, aa):
        self.data = data
        self.name = bytearray()
        while(True):
            if(answer[0] == 0):
                break
            self.name.append(answer[0])
            answer = answer[1:]
        self.type = answer[0:2]
       # if self.type != b'\x00\x01' and self.type != b'\x00\x02' and self.type != b'\x00\x05' and self.type != b'\x00\x0f':
            ##raise Exception("ERROR    Unknown response type")
        self.class_ = answer[2:4]
        self.ttl = answer[4:8]
        self.rdlength = answer[8:10]
        self.rdata = answer[10:10 + int.from_bytes(self.rdlength, byteorder='big')]
        self.length = len(self.name) + 10 + int.from_bytes(self.rdlength, byteorder='big')
        self.aa = aa
    ## GETTERS
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_class(self):
        return self.class_

    def get_ttl(self):
        return self.ttl

    def get_rdlength(self):
        return self.rdlength

    def get_rdata(self):
        return self.rdata

    def get_length(self):
        return self.length

    def get_resource(self):
        if self.type == b'\x00\x01':
            string = ""
            index = 0
            while index < len(self.rdata):
                string += "IP\t" + str(self.rdata[index]) + '.' + str(self.rdata[index+1]) + '.' + str(self.rdata[index+2]) + '.' + str(self.rdata[index+3]) + "\t" + str(int.from_bytes(self.ttl, byteorder='big')) + "\t" + {True:"auth", False:"nonauth"}[self.aa]
                index += 4
            return string
        if self.type == b'\x00\x02':
            index = 0
            string = ""
            temp = ""
            while True:
                if self.rdata[index] == 0:
                    break
                if get_bit(self.rdata[index],7) & 1 and get_bit(self.rdata[index],6) & 1:
                    temp_index = self.rdata[index+1]
                    index += 1
                    while True:
                        if self.data[temp_index] == 0:
                            break
                        length = self.data[temp_index]
                        temp_index += 1
                        for j in range(length):
                            temp += chr(self.data[temp_index])
                            temp_index += 1
                        temp += '.'
                    break
                length = self.rdata[index]

                index += 1
                for j in range(length):
                    temp += chr(self.rdata[index])
                    index += 1
                temp += '.'
            return "NS\t" + temp[:-1] + "\t" + str(int.from_bytes(self.ttl, byteorder='big')) + "\t" + {True:"auth", False:"nonauth"}[self.aa]
        if self.type == b'\x00\x05':
            index = 0
            string = ""
            temp = ""
            while True:
                if self.rdata[index] == 0:
                    break
                if get_bit(self.rdata[index],7) & 1 and get_bit(self.rdata[index],6) & 1:
                    temp_index = self.rdata[index+1]
                    index += 1
                    while True:
                        if self.data[temp_index] == 0:
                            break
                        length = self.data[temp_index]
                        temp_index += 1
                        for j in range(length):
                            temp += chr(self.data[temp_index])
                            temp_index += 1
                        temp += '.'
                    break
                length = self.rdata[index]

                index += 1
                for j in range(length):
                    temp += chr(self.rdata[index])
                    index += 1
                temp += '.'
            return "CNAME\t" + temp[:-1] + "\t" + str(int.from_bytes(self.ttl, byteorder='big')) + "\t" + {True:"auth", False:"nonauth"}[self.aa]
        if self.type == b'\x00\x0f':
            pref = self.rdata[0:2]
            index = 2
            string = ""
            temp = ""
            while True:
                if self.rdata[index] == 0:
                    break
                if get_bit(self.rdata[index],7) & 1 and get_bit(self.rdata[index],6) & 1:
                    temp_index = self.rdata[index+1]
                    index += 1
                    while True:
                        if self.data[temp_index] == 0:
                            break
                        length = self.data[temp_index]
                        temp_index += 1
                        for j in range(length):
                            temp += chr(self.data[temp_index])
                            temp_index += 1
                        temp += '.'
                    break
                length = self.rdata[index]

                index += 1
                for j in range(length):
                    temp += chr(self.rdata[index])
                    index += 1
                temp += '.'
            return "MX\t" + temp[:-1] + "\t" + str(int.from_bytes(self.ttl, byteorder='big')) + "\t" + {True:"auth", False:"nonauth"}[self.aa]

def get_bit(byte, position):
        return (byte >> position) & 1
