from ctypes import *
#load libhackrf
libhackrf=cdll.LoadLibrary("/usr/local/lib/libhackrf.so")

def hackrf_init():
    pass
    return libhackrf.hackrf_init()

def hackrf_exit():
    pass
    return libhackrf.hackrf_init()

def hackrf_open(device):
    pass
    return libhackrf.hackrf_open(device)

def hackrf_close(device):
    pass
    return libhackrf.hackrf_close(device)

def hackrf_start_rx(device,callback,tx_ctx):
    pass
    return libhackrf.hackrf_start_rx(device,callback,tx_ctx)

def hackrf_stop_rx(device):
    pass
    return libhackrf.hackrf_stop_rx(device)

def hackrf_start_tx(device,callback,tx_ctx):
    pass
    return libhackrf.hackrf_start_tx(device,callback,tx_ctx)

def hackrf_stop_tx(device):
    pass
    return libhackrf.hackrf_stop_tx(device)

def hack_is_streaming(device):
    pass
    return libhackrf.hackrf_is_streaming(device)

def hackrf_max2837_read(device,register_number,value):
    pass
    return libhackrf.hackrf_max2837_read(device,register_number,value)

def hackrf_max2837_weite(device,register_number,value):
    pass
    return libhackrf.hackrf_max2837_weite(device,register_number,value)

def hackrf_si5351c_read(device,register_number,value):
    pass
    return libhackrf.hackrf_si5351c_read(device,register_number,value)

def hackrf_si5351c_write(device,register_number,value):
    pass
    return libhackrf.hackrf_si5351c_write(device,register_number,value)

def hackrf_set_baseband_filter_bandwidth(device,bandwidth_hz):
    pass
    return libhackrf.hackrf_set_baseband_filter_bandwidth(device,bandwidth_hz)

def hackrf_rffc5071_read(device,register_number,value):
    pass
    return libhackrf.hackrf_rffc5071_read(device,register_number,value)

def hackrf_rffc5071_write(device,register_number,value):
    pass
    return libhackrf.hackrf_rffc5071_write(device,register_number,value)

def hackrf_spiflash_erase(device):
    pass
    return libhackrf.hackrf_spiflash_erase(device)

def hackrf_spiflash_write(device,address,length,data):
    pass
    return libhackrf.hackrf_spiflash_write(device,address,length,data)

def hackrf_spiflash_read(device,address,length,data):
    pass
    return libhackrf.hackrf_spiflash_read(device,address,length,data)

def hackrf_cpld_write(device,data,total_length):
    pass
    return libhackrf.hackrf_cpld_write(device,data,total_length)

def hackrf_board_id_read(device,value):
    pass
    return libhackrf.hackrf_board_id_read(device,value)

def hackrf_version_string_read(device,version,lenth):
    pass
    return libhackrf.hackrf_version_string_read(device,version,lenth)

def hackrf_set_freq(device,freq_hz):
    pass
    return libhackrf.hackrf_set_freq(device,freq_hz)

def hackrf_set_freq_explicit(device,if_freq_hz,lo_freq_hz,path):
    pass
    return libhackrf.hackrf_set_freq_explicit(device,if_freq_hz,lo_freq_hz,path)

def hackrf_set_sample_rate_manual(device,freq_hz,divider):
    pass
    return libhackrf.hackrf_set_sample_rate_manual(device,freq_hz,divider)

def hackrf_set_sample_rate(device,freq_hz):
    pass
    return libhackrf.hackrf_set_sample_rate(device,freq_hz)

def hackrf_set_amp_enable(device,value):
    pass
    return libhackrf.hackrf_set_amp_enable(device,value)

def hackrf_board_partid_serialno_read(device,read_partid_serialno):
    pass
    return libhackrf.hackrf_board_partid_serialno_read(device,read_partid_serialno)

def hackrf_set_lna_gain(device,value):
    pass
    return libhackrf.hackrf_set_lna_gain(device,value)

def hackrf_set_vga_gain(device,value):
    pass
    return libhackrf.hackrf_set_vga_gain(device,value)

def hackrf_set_txvga_gain(device,value):
    pass
    return libhackrf.hackrf_set_txvga_gain(device,value)

def hackrf_set_antenna_enable(device,value):
    pass
    return libhackrf.hackrf_set_antenna_enable(device,value)

def hackrf_error_name(errcode):
    pass
    return libhackrf.hackrf_error_name(errcode)

def hackrf_board_id_name(board_id):
    pass
    return libhackrf.hackrf_board_id_name(board_id)

def hackrf_filter_path_name(path):
    pass
    return libhackrf.hackrf_filter_path_name(path)

def hackrf_compute_baseband_filter_bw_round_down_lt(bandwidth_hz):
    pass
    return libhackrf.hackrf_compute_baseband_filter_bw_round_down_lt(bandwidth_hz)

def hackrf_compute_baseband_filter_bw(bandwidth_hz):
    pass
    return libhackrf.hackrf_compute_baseband_filter_bw(bandwidth_hz)

    
    








