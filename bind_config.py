#!/usr/bin/env python

import os
import socket
from IPy import IP
# Following Environment Variables are expected or will be populated with default values

server  = os.environ.get('DNS_IP', socket.gethostbyname(os.environ.get('HOSTNAME')))
subnet  = IP(os.environ.get('DNS_SUBNET', '192.168.0.0/24'))
domain  = os.environ.get('DNS_DOMAIN', 'my.ip')

subnetblock = '.'.join(str(subnet).split('.')[:-1])

def subnetiter(subnet):
    while [ 1 ]:
        try:    subnet = IP(subnet.ip + 256)
        except: raise StopIteration()
        yield subnet

template = """$ORIGIN .
$TTL 600    ; 10 minutes
%s       IN SOA  self.%s. hostmaster.%s. (
                1 ; serial
                3600       ; refresh (1 hour)
                300        ; retry (5 minutes)
                3600000    ; expire (5 weeks 6 days 16 hours)
                3600       ; minimum (1 hour)
                )
            NS  self.%s.
$ORIGIN %s
self    A  %s""" % (domain, domain, domain, domain, domain, server) 
print template

subnetblock = '.'.join(str(subnet).split('.')[:-1])
subiter     = subnetiter(subnet)
currentblock = IP(subnet.ip)

while subnet.overlaps(currentblock):
    print "$GENERATE %s *.%s.$ A %s.$" % ('0-255', subnetblock, subnetblock)
    currentblock = subiter.next()
    subnetblock = '.'.join(str(currentblock).split('.')[:-1])
