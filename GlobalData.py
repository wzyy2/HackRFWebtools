from pyhackrf import pylibhackrf 

#hackrf device
hackrf = pylibhackrf.HackRf()

#default setting
class HackrfSettings():
    def __init__(self):
        self.modulation = 'NO'
        self.centre_frequency = 100 * 1000 * 1000
        self.sample_rate = 8 * 1000 * 1000
        self.rf_gain = 0
        self.if_gain = 16
        self.bb_gain = 20
        self.bb_bandwidth = 7 * 1000 * 1000
        self.current_status = 0  #0 stop 1 rx 2 tx
        self.fft_size = 8192
        self.fft_rate = 20
        self.name = None
        self.version = None
        self.serial_num = None
        self.rx_thread = None
hackrf_settings = HackrfSettings()

