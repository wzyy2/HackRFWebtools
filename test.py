from pyhackrf.core import HackRf 

def timer(buf, size):  
    print 1

hackrf = HackRf()
hackrf.set_rx_mode(timer)