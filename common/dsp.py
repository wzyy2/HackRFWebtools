import numpy
import math

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
