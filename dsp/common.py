import numpy
import math,types,threading
import scipy.signal

def get_exp(num):
    """
    Get the exponent of the number in base 10.

    Args:
        num: the floating point number

    Returns:
        the exponent as an integer
    """
    if num == 0: return 0
    return int(math.floor(math.log10(abs(num))))

def get_clean_num(num):
    """
    Get the closest clean number match to num with bases 1, 2, 5.

    Args:
        num: the number

    Returns:
        the closest number
    """
    if num == 0: return 0
    sign = num > 0 and 1 or -1
    exp = get_exp(num)
    nums = numpy.array((1, 2, 5, 10))*(10**exp)
    return sign*nums[numpy.argmin(numpy.abs(nums - abs(num)))]

def get_clean_incr(num):
    """
    Get the next higher clean number with bases 1, 2, 5.

    Args:
        num: the number

    Returns:
        the next higher number
    """
    num = get_clean_num(num)
    exp = get_exp(num)
    coeff = int(round(num/10**exp))
    return {
        -5: -2,
        -2: -1,
        -1: -.5,
        1: 2,
        2: 5,
        5: 10,
    }[coeff]*(10**exp)

def get_clean_decr(num):
    """
    Get the next lower clean number with bases 1, 2, 5.

    Args:
        num: the number

    Returns:
        the next lower number
    """
    num = get_clean_num(num)
    exp = get_exp(num)
    coeff = int(round(num/10**exp))
    return {
        -5: -10,
        -2: -5,
        -1: -2,
        1: .5,
        2: 1,
        5: 2,
    }[coeff]*(10**exp)

def get_min_max(samples):
    """
    Get the minimum and maximum bounds for an array of samples.

    Args:
        samples: the array of real values

    Returns:
        a tuple of min, max
    """
    factor = 2.0
    mean = numpy.average(samples)
    std = numpy.std(samples)
    fft = numpy.abs(numpy.fft.fft(samples - mean))
    envelope = 2*numpy.max(fft)/len(samples)
    ampl = max(std, envelope) or 0.1
    return mean - factor*ampl, mean + factor*ampl

def get_min_max_fft(fft_samps):
    """
    Get the minimum and maximum bounds for an array of fft samples.

    Args:
        samples: the array of real values

    Returns:
        a tuple of min, max
    """
    #get the peak level (max of the samples)
    peak_level = numpy.max(fft_samps)
    #separate noise samples
    noise_samps = numpy.sort(fft_samps)[:len(fft_samps)/2]
    #get the noise floor
    noise_floor = numpy.average(noise_samps)
    #get the noise deviation
    noise_dev = numpy.std(noise_samps)
    #determine the maximum and minimum levels
    max_level = peak_level
    min_level = noise_floor - abs(2*noise_dev)
    return min_level, max_level

def freqShiftIQ(d, freqshift):
    """Shift frequency by multiplication with complex phasor."""

    def g(d, freqshift):
        p = 0
        for b in d:
            n = len(b)
            w = numpy.exp((numpy.arange(n) + p) * (2j * numpy.pi * freqshift))
            p += n
            yield b * w

    if isinstance(d, types.GeneratorType):
        return g(d, freqshift)
    else:
        n = len(d)
        w = numpy.exp(numpy.arange(n) * (2j * numpy.pi * freqshift))
        return d * w

def FmDemodulate(data):
    # Calculate the complex vector between two adjacent data points
    tmp = data[1::1] * numpy.conjugate(data[0:-1:1]);
    # Record the angle of the complex difference vectors
    return numpy.angle(tmp);

from scipy.signal import lfilter

def PolyphaseDecimate(filt,inputData,mixValues,filtState,decRate):
    
  # Decompose the input and the filter
  polyFilt = numpy.reshape(filt,[decRate, -1],order='F');
  print polyFilt
  polyFilt = numpy.flipud(polyFilt);
  polyInput = numpy.reshape(inputData,[decRate,-1],order='F');
  # Pre-allocate the array
  tmp = numpy.zeros(shape=(decRate,len(inputData)/decRate), dtype=numpy.complex64);

  # Perform the mixing (only if necessary)
  if len(mixValues) > 0:
    polyMix = numpy.reshape(mixValues,[decRate,-1],order='F');
    polyInput = polyInput * polyMix;
  
  # Perform the filtering - there are two ways out of the function
  if numpy.size(filtState) == 0:
    # A filter state was not passed in, ignore tracking states
    for ndx in range(decRate):
      tmp[ndx,:] = lfilter(polyFilt[ndx,:],1,polyInput[ndx,:]);
    return numpy.sum(tmp,axis=0);
  else:
    # A filter state was passed in. Supply it to the filter routine and pass back the updated state
    for ndx in range(decRate):
      (tmp[ndx,:],filtState[ndx,:]) = lfilter(polyFilt[ndx,:],1,polyInput[ndx,:],zi=filtState[ndx,:]);
    return (numpy.sum(tmp,axis=0),filtState);

import pyaudio
import wave,time,random



class AudioPlay(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.running = True
    self.audioQueue = None

  def run(self):
    # Grab initial data off of the queue
    # wf =  wave.open("/home/chen/test.wav", 'rb');
    # chunk = 1024
    # Create the audio device
    # audioData = numpy.empty(82666 , 'int')
    audioData = self.audioQueue.get()
    self.audioQueue.task_done()

    audioObject = pyaudio.PyAudio()
    # Create stream object associated with the audio device
    # If mono is desired, change the number of channels to '1' here
    pcmStream = audioObject.open(format=pyaudio.paInt16,channels=1,rate=40000,output=True,frames_per_buffer=numpy.size(audioData)*2)
    # pcmStream = audioObject.open(format = audioObject.get_format_from_width(wf.getsampwidth()),
    #                 channels = wf.getnchannels(),
    #                 rate = wf.getframerate(),
    #                 output = True)  
    # time1 = time.time()
    # audioData = []
    while self.running:  
        # audioData = wf.readframes(chunk)
        # if audioData == "": break
        # Play the audio - the Python wrapper assumes a string of bytes. . . 
        # It doesn't have to be this way but that is pyaudio's assumption
        # time2 = time.time()
        # if(time2 - time1 >1):
        #     for i in range(82666):
        #         audioData.append( random.randint(1, 255))     
        pcmStream.write(str(bytearray(audioData)))
        audioData = self.audioQueue.get()

        print len(bytearray(audioData))
        self.audioQueue.task_done()

    pcmStream.close()
    audioObject.terminate()