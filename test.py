from pyhackrf import pylibhackrf 
import sys,time,threading,random
from func import *
import numpy as np
import pylab as pl
from ctypes import *
from dsp import common
import Queue,copy
# time1= time.time()
# cnt = 0
# def callback_fun(hackrf_transfer):
#     global time1,cnt
#     time2= time.time()
#     if time2 - time1 >= 1:
#         time1 = time.time()
#         print cnt
#         cnt = 0
#     cnt += hackrf_transfer.contents.valid_length
#     return 0
time1= time.time()
have_recv = False
lock = threading.Lock()
all_cnt = 0
buf = list()
buf2 = list()
cnt = 0
dataQueue = Queue.Queue([1]);

def callback_fun(hackrf_transfer):
    global  buf,buf2,cnt,time1,all_cnt 
    length = hackrf_transfer.contents.valid_length
    array_type = (c_ubyte*length)
    
    all_cnt += length
    if time.time() - time1 > 1:
        time1 = time.time()
        print all_cnt
        all_cnt = 0
    # iq = hackrf.packed_bytes_to_iq(values)

    values = cast(hackrf_transfer.contents.buffer, POINTER(array_type)).contents
    buf = copy.deepcopy(values)
    dataQueue.put(buf)

    return 0

if hackrf.is_open == False:
    hackrf.setup()
    hackrf.set_freq(hackrf_settings.centre_frequency)
    hackrf.set_sample_rate(hackrf_settings.sample_rate)
    hackrf.set_amp_enable(False)
    hackrf.set_lna_gain(hackrf_settings.if_gain)
    hackrf.set_vga_gain(hackrf_settings.bb_gain)    
    hackrf.set_baseband_filter_bandwidth(hackrf_settings.bb_bandwidth)  

# hackrf.start_rx_mode(callback_fun)


# Define the FIR filter taps used to extract the audio channels
# (90 taps, equiripple, fc = 19KHz, +/-0.4dB ripple in pass band, -47dB stop-band)
audioFilt = np.array([-0.00287983581133987,-0.000926407885047457,-0.000635251149646470,1.62845117817972e-05,0.00101916904478077,0.00229943112316492,0.00371371303782623,0.00506045151836540,0.00610736757778672,0.00662771338675820,0.00644014551958777,0.00544825751160880,0.00367332418708154,0.00127145849802163,-0.00147184344296973,-0.00417153634486715,-0.00639395493204246,-0.00772265459702439,-0.00783097318267360,-0.00655054644922716,-0.00392290604321896,-0.000222050906968737,0.00405977873813144,0.00826470411817517,0.0116557586699066,0.0135276814247624,0.0133274609455304,0.0107664845536791,0.00590519748125791,-0.000806134283814829,-0.00854123766576385,-0.0161694590376135,-0.0223801909792768,-0.0258466830262674,-0.0254085058655117,-0.0202474878245569,-0.0100315190547527,0.00499593742645088,0.0239963553790494,0.0455936584130458,0.0680052492125116,0.0892321839791224,0.107284945330503,0.120415688114799,0.127326567918114,0.127326567918114,0.120415688114799,0.107284945330503,0.0892321839791224,0.0680052492125116,0.0455936584130458,0.0239963553790494,0.00499593742645088,-0.0100315190547527,-0.0202474878245569,-0.0254085058655117,-0.0258466830262674,-0.0223801909792768,-0.0161694590376135,-0.00854123766576385,-0.000806134283814829,0.00590519748125791,0.0107664845536791,0.0133274609455304,0.0135276814247624,0.0116557586699066,0.00826470411817517,0.00405977873813144,-0.000222050906968737,-0.00392290604321896,-0.00655054644922716,-0.00783097318267360,-0.00772265459702439,-0.00639395493204246,-0.00417153634486715,-0.00147184344296973,0.00127145849802163,0.00367332418708154,0.00544825751160880,0.00644014551958777,0.00662771338675820,0.00610736757778672,0.00506045151836540,0.00371371303782623,0.00229943112316492,0.00101916904478077,1.62845117817972e-05,-0.000635251149646470,-0.000926407885047457,-0.00287983581133987]);
# Define the decimation rate to convert from the sampling rate to the audio rate        
audioDec = 6;
# Create the audio filter states, initially filled w/zeros
audioFiltStateLplusR = np.zeros((audioDec,np.size(audioFilt)/audioDec-1),dtype=np.complex64);
audioFiltStateLminusR = np.zeros((audioDec,np.size(audioFilt)/audioDec-1),dtype=np.complex64);

audioQueue = Queue.Queue([1]);
audio = common.AudioPlay()
audio.audioQueue = audioQueue
audioData = np.empty(40000, dtype=np.int16);
audio.start()
# audioData= []
for i in range(40000):
    audioData[i] = random.randint(1, 65533)     
    # print audioData[i]
    # audioData.append(random.randint(1, 255))     
while True:
    # data = dataQueue.get();     
    # iq =  hackrf.packed_bytes_to_iq(data);
    # fm = common.FmDemodulate(iq);
    # # Add an element to keep a proper size for the polyphase filtering
    # fm = np.concatenate(([0],fm));
    time.sleep(0.5)
    audioQueue.put(audioData)
    audioQueue.join()
    # (audioDataLplusR,audioFiltStateLplusR) = common.PolyphaseDecimate(audioFilt,fm,[],audioFiltStateLplusR,audioDec);
    # audioDataLplusR = np.real(audioDataLplusR);
    # print len(audioDataLplusR)

    # print  len(fm)
# while True:
#     lock.acquire()  
#     if have_recv == True:
#         iq = hackrf.packed_bytes_to_iq_withsize(buf2, 8192)
#         # buf3 = [-2, -1, 1, 6, 8, 9, 8, 6, 1, -1, -2, -1, 1, 6, 8, 9, 8, 6, 1, -1, -2, -1, 1, 6, 8, 9, 8, 6, 1, -1]
#         # iq = hackrf.packed_bytes_to_iq(buf3)
#         # iq2 = common.freqShiftIQ(iq, 100)
#         # # iq = hackrf.packed_bytes_to_iq_withsize(buf2, 2048)
#         # pl.figure()
#         lock.release()  
#         # fy = np.fft.fft(iq) / iq.size
#         # fx = np.fft.fft(iq2) / iq2.size        
#         # # pl.plot(iq)
#         # pl.plot(iq2)
#         # fy = np.fft.fftshift( fy )

#         # pl.xlabel("frequency bin")
#         # pl.ylabel("power(dB)")
#         # pl.title("FFT result of triangle wave")
#         # pl.show()

#         have_recv = False    
#     else:
#         lock.release()  


# print hackrf.hackrf_open()