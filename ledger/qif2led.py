import sys
import parseqif


xpayee = {
    "American Express" : "amex",
    "BofA Merchant Services": "bofa ms",
    "Rackspace": "rackspace",
    "Merchant Account" : "bofa ms",
    "Service Charge": "monthly maintenance fee",
}

xpayee = {
    "American Express" : "amex",
    "BofA Merchant Services": "bofa ms",
    "Rackspace": "rackspace",
    "Merchant Account" : "bofa ms",
    "Service Charge": "monthly maintenance fee",
}


if __name__=="__main__":

    
    try:
        f = file(sys.argv[1])
    except Exception, e:
        print e
        print "usage: qif2led.py filename"
        sys.exit()
        
    data = parseqif.parseQif(f)

    for item in data:
        print item.date,
        if item.num:
            print "(%s)" % item.num,
        print xpayee.get(item.payee, item.payee.lower())
        print "    asset:checking %33s" % item.amount
        print "    other:account"
        print

        
        
