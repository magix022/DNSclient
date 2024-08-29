class DnsQuestion:
    def __init__(self, data):
        self.qname = bytearray()
        while(True):
            if(data[0] == 0):
                break
            self.qname.append(data[0])
            data = data[1:]
        self.qtype = data[0:2]
        self.qclass = data[2:4]
        self.length = len(self.qname) + 4

    ## GETTERS
    def get_qname(self):
        return self.qname

    def get_qtype(self):
        return self.qtype

    def get_qclass(self):
        return self.qclass

    def get_length(self):
        return self.length