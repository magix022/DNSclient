class DnsHeader:
    def __init__(self, data):
        self.id = data[0:2]
        self.flags = data[2:4]
        self.qdcount = data[4:6]
        self.ancount = data[6:8]
        self.nscount = data[8:10]
        self.arcount = data[10:12]

        # ##manually set ra to 0
        # self.flags = self.flags[0:1] + b'\x00' + self.flags[2:4]


        # print ("***Header Section***")
        # print ("ID: 0x" + self.id.hex())
        # print ("Flags: 0x" + self.flags.hex())
        # print ("QDCOUNT: " + str(self.get_qdcount()))
        # print ("ANCOUNT: " + str(self.get_ancount()))
        # print ("NSCOUNT: " + str(self.get_nscount()))
        # print ("ARCOUNT: " + str(self.get_arcount()))



        if self.get_qr() != 1:
            raise Exception("ERROR    Not a response packet")
        if self.get_opcode() != 0:
            raise Exception("ERROR    Not a standard query")
        if self.get_rcode() != 0:
            if self.get_rcode() == 1:
                raise Exception("ERROR    Format error: the name server was unable to interpret the query")
            if self.get_rcode() == 2:
                raise Exception("ERROR    Server failure: the name server was unable to process this query due to a problem with the name server")
            if self.get_rcode() == 3:
                if self.get_aa() == 1:
                    raise Exception("ERROR    Name error: meaningful only for responses from an authoritative name server, this code signifies that the domain name referenced in the query does not exist")
            if self.get_rcode() == 4:
                raise Exception("ERROR    Not implemented: the name server does not support the requested kind of query")
            if self.get_rcode() == 5:
                raise Exception("ERROR    Refused: the name server refuses to perform the requested operation for policy reasons")

        if self.get_ra() != 1:
            print("ERROR    Recursion not available")
            

        

    ## GETTERS
    def get_id(self):
        return self.id

    def get_flags(self):
        return self.flags

    def get_qdcount(self):
        return int.from_bytes(self.qdcount, byteorder='big')

    def get_ancount(self):
        return int.from_bytes(self.ancount, byteorder='big')

    def get_nscount(self):
        return int.from_bytes(self.nscount, byteorder='big')

    def get_arcount(self):
        return int.from_bytes(self.arcount, byteorder='big')

    def get_qr(self):
        return (self.flags[0] & 0x80) >> 7

    def get_opcode(self):
        return (self.flags[0] & 0x78) >> 3

    def get_aa(self):
        return (self.flags[0] & 0x04) >> 2

    def get_tc(self):
        return (self.flags[0] & 0x02) >> 1

    def get_rd(self):
        return self.flags[0] & 0x01

    def get_ra(self):
        return (self.flags[1] & 0x80) >> 7

    def get_z(self):
        return (self.flags[1] & 0x70) >> 4

    def get_rcode(self):
        return self.flags[1] & 0x0F
