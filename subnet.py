class Main:

    def __init__(self):

        self.cidr       = 0
        self.mask       = 0
        self.ipaddress  = 0
        self.hosts      = 0
        self.subnets    = 0
        self.subnethost = 0

        print """
                   _                _   _   _
                  | |              | | | | (_)
 _ __   ___   ___ | |__  _ __   ___| |_| |_ _ _ __   __ _
| '_ \ / _ \ / _ \| '_ \| '_ \ / _ \ __| __| | '_ \ / _` |
| | | | (_) | (_) | |_) | | | |  __/ |_| |_| | | | | (_| |
|_| |_|\___/ \___/|_.__/|_| |_|\___|\__|\__|_|_| |_|\__, |
                                                     __/ |
  # VERSION 2.1           NOW WITH EASTER EGG(S)!   |___/

Another shitty tool made by parkerp

The following prompt should interpret what you input pretty well, if not
then you probably shouldn't be subnetting in the first place.

Type "help" to see commands!
            """

    def display(self):

        print ""
        print "%-15s%-15s" % ('CIDR:', self.cidr), "\t\t", "%-15s%-15s" % ('IP ADDRESS:', self.ipaddress)
        print "%-15s%-15s" % ('MASK:', self.mask), "\t\t", "%-15s%-15s" % ('SUBNET HOST:', self.subnethost)

        print "%-15s%-15s" % ('# OF SUBNETS:', self.subnets)
        print "%-15s%-15s" % ('HOSTS/SUBNET:', self.hosts)
        print ""

        self.interpreter()

    def interpreter(self):

        raw = raw_input(" > ")

        if raw == 'help' or raw == 'h':

            print ""
            print " |Type an IP/CIDR, /CIDR, or subnet mask:"
            print " |\t> 172.20.179.64/26"
            print " |\t> /26 or 26"
            print " |\t> 255.255.255.192\n"
            print " |For this list:"
            print " |\t> help"
            print " |\t> h\n"
            print " |For subnetting tables:"
            print " |\t> table"
            print " |\t> t\n"
            print " |To reset user input:"
            print " |\t> reset"
            print " |\t> r\n"

            self.interpreter()

        elif raw == 'table' or raw == 't':

            self.tables()
            self.interpreter()

        elif raw == 'reset' or raw == 'r':

            self.cidr = 0
            self.mask = 0
            self.ipaddress = 0
            self.hosts = 0
            self.subnets = 0
            self.subnethost = 0

            print ""

            self.interpreter()

        ## IP WITH CIDR
        elif "/" in raw:

            self.cidr = raw.split('/')[1]
            self.ipaddress = raw.split('/')[0]

            self.qcidr = True
            self.qip = True
            self.qmask = False

            self.path()

        ## CIDR VALUES
        elif len(raw) <= 4:

            try:
                self.cidr = int(raw.lstrip("/"))
            except:
                self.cidr = int(raw)

            self.qcidr  = True
            self.qip    = False
            self.qmask   = False

            self.path()

        elif raw.count(".") > 3:

            self.ipaddress  = raw.split(" ")[0]
            self.mask       = raw.split(" ")[1]

            self.qcidr  = False
            self.qip    = True
            self.qmask  = True

            self.path()

        ## MASK
        else:
            self.mask = raw

            self.qcidr = False
            self.qip = False
            self.qmask = True

            self.path()

    def path(self):

        # Mask yet?
        if self.qmask == True:
            pass
        else:
            self.genmask()

        # CIDR yet?
        if self.qcidr == True:
            pass
        else:
            self.gencidr()

        # How many subs? Hosts?
        self.subandhosts()

        # Is there any IP? What sub contains it?
        if self.qip == True:
            self.subcontain()
        else:
            pass

        self.display()

    def genmask(self):

        self.cidr = int(self.cidr)

        # LAST OCTET
        if self.cidr > 24:

            multiplier = 7

            for number in range(24, self.cidr):
                self.mask += (2 ** multiplier)
                multiplier -= 1

            self.mask = "255.255.255.%r" % self.mask

        # 3RD OCTET
        elif 16 < self.cidr < 24:

            multiplier = 7

            for number in range(16, self.cidr):
                self.mask += (2 ** multiplier)
                multiplier -= 1

            self.mask = "255.255.%r.0" % self.mask

        # 2ND OCTET
        elif 8 < self.cidr < 16:

            multiplier = 7

            for number in range(8, self.cidr):
                self.mask += (2 ** multiplier)
                multiplier -= 1

            self.mask = "255.%r.0.0" % self.mask

        elif self.cidr == 24:
            self.mask = "255.255.255.0"

        elif self.cidr == 16:
            self.mask = "255.255.0.0"

    def gencidr(self):

        octets = self.mask.split(".")
        bits = [128, 64, 32, 16, 8, 4, 2, 1]

        for octet in octets:
            if octet == "255":
                self.cidr += 8
            elif octet == "0":
                pass
            else:
                borrower = int(octet)
                count = 0

                while borrower > 0:
                    borrower -= bits[count]
                    self.cidr += 1
                    count += 1

    def subandhosts(self):

        borrowedbits = self.cidr % 8
        self.subnets = 2 ** borrowedbits

        self.hosts = (256 / self.subnets) - 2

    def subcontain(self):

        octets = self.mask.split(".")
        octet = False
        count = 0

        while octet == False:
            if int(octets[count]) == 0:
                octet = count
            elif count == 3:
                octet = count
            else:
                count += 1
                pass

        octets = self.ipaddress.split(".")
        host = int(octets[octet])
        interval = (256/self.subnets)

        octets[octet] = (host / interval) * interval

        self.subnethost = "%s.%s.%s.%s" % (octets[0], octets[1], octets[2], octets[3])

    def tables(self):

        if self.ipaddress != 0:
            octets = str(self.ipaddress).split(".")
        else:
            octets = self.mask.split(".")

        interval = self.hosts + 2

        if self.cidr > 25:

            # GET THE UNTOUCHED OCTETS TO ADD ON
            mutable = 3
            ipbase = ""
            for i in range(0, mutable):
                ipbase += octets[i] + "."
            print ipbase
            # CREATE BASES FOR PRINTING, AKA SUB 1 VALUES
            smod = 1
            nmod = 0
            h1mod = 0 + 1
            h2mod = 0 + int(self.hosts)
            bmod = 0 + 1 + int(self.hosts)
            mods = [nmod, h1mod, h2mod, bmod]

            for i in range(0, (self.subnets / 4)):

                categories = ["Network:", "First Host:", "Last Host:", "Broadcast:"]

                print "%12s  %-15s  %-15s  %-15s  %-15s" % ("Subnet:", smod, smod + 1, smod + 2, smod + 3)
                smod += 4

                for mod in mods:
                    row1 = ipbase + str(mod)
                    row2 = ipbase + str(mod + interval)
                    row3 = ipbase + str(mod + 2 * (interval))
                    row4 = ipbase + str(mod + 3 * (interval))

                    print "%12s  %-15s  %-15s  %-15s  %-15s" % (categories[mods.index(mod)], row1, row2, row3, row4)

                    mods[mods.index(mod)] = (interval + mod + 3 * (interval))
                print ""

        elif self.cidr == 25:

            # GET THE UNTOUCHED OCTETS TO ADD ON
            mutable = 3
            ipbase = ""
            for i in range(0, mutable):
                ipbase += octets[i] + "."

            # CREATE BASES FOR PRINTING, AKA SUB 1 VALUES
            smod = 1
            nmod = 0
            h1mod = 0 + 1
            h2mod = 0 + int(self.hosts)
            bmod = 0 + 1 + int(self.hosts)
            mods = [nmod, h1mod, h2mod, bmod]

            categories = ["Network:", "First Host:", "Last Host:", "Broadcast:"]

            print "%12s  %-15s  %-15s" % ("Subnet:", smod, smod + 1)

            for mod in mods:
                row1 = ipbase + str(mod)
                row2 = ipbase + str(mod + interval)

                print "%12s  %-15s  %-15s" % (categories[mods.index(mod)], row1, row2)

                mods[mods.index(mod)] = (interval + mod + 3 * (interval))

            print ""

        elif self.cidr < 25:
            print "You can't do that with those /CIDR and mask values.\n"

m = Main()
m.interpreter()