import string
from ctypes import *

_libraries = {}
#linux
#_libraries['libhackrf.so'] = CDLL('libhackrf.so')

#mac
_libraries['libhackrf.so'] = CDLL('/opt/local/lib/libhackrf.0.3.0.dylib')



STRING = c_char_p
int8_t = c_int8
int16_t = c_int16
int32_t = c_int32
int64_t = c_int64
uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32
uint64_t = c_uint64
int_least8_t = c_byte
int_least16_t = c_short
int_least32_t = c_int
int_least64_t = c_long
uint_least8_t = c_ubyte
uint_least16_t = c_ushort
uint_least32_t = c_uint
uint_least64_t = c_ulong
int_fast8_t = c_byte
int_fast16_t = c_long
int_fast32_t = c_long
int_fast64_t = c_long
uint_fast8_t = c_ubyte
uint_fast16_t = c_ulong
uint_fast32_t = c_ulong
uint_fast64_t = c_ulong
intptr_t = c_long
uintptr_t = c_ulong
intmax_t = c_long
uintmax_t = c_ulong



class hackrf_dev(Structure):
    pass



hackrf_dev_t = hackrf_dev
hackrf_dev._fields_=[]

hackrf_init=_libraries['libhackrf.so'].hackrf_init
hackrf_init.restype = int_least32_t
hackrf_init.argtypes = []

hackrf_exit=_libraries['libhackrf.so'].hackrf_exit
hackrf_exit.restype = int_least32_t
hackrf_exit.argtypes = []

hackrf_open=_libraries['libhackrf.so'].hackrf_open
hackrf_open.restype = int_least32_t
hackrf_open.argtypes = [POINTER(POINTER(hackrf_dev_t))]

hackrf_close=_libraries['libhackrf.so'].hackrf_close
hackrf_close.restype = int_least32_t
hackrf_close.argtypes = [POINTER(hackrf_dev_t)]


###
hackrf_set_transceiver_mode=_libraries['libhackrf.so'].hackrf_set_transceiver_mode
hackrf_set_transceiver_mode.restype = int_least32_t
hackrf_set_transceiver_mode.argtypes = [POINTER(hackrf_dev_t),int_least32_t]


hackrf_max2837_read=_libraries['libhackrf.so'].hackrf_max2837_read
hackrf_max2837_read.restype = int_least32_t
hackrf_max2837_read.argtypes = [POINTER(hackrf_dev_t),uint8_t,POINTER(uint16_t)]

hackrf_max2837_write=_libraries['libhackrf.so'].hackrf_max2837_write
hackrf_max2837_write.restype = int_least32_t
hackrf_max2837_write.argtypes = [POINTER(hackrf_dev_t),uint8_t,uint16_t]

hackrf_si5351c_read=_libraries['libhackrf.so'].hackrf_si5351c_read
hackrf_si5351c_read.restype = int_least32_t
hackrf_si5351c_read.argtypes = [POINTER(hackrf_dev_t),uint16_t,POINTER(uint16_t)]

hackrf_si5351c_write=_libraries['libhackrf.so'].hackrf_si5351c_write
hackrf_si5351c_write.restype = int_least32_t
hackrf_si5351c_write.argtypes = [POINTER(hackrf_dev_t),uint16_t,uint16_t]

hackrf_set_baseband_filter_bandwidth=_libraries['libhackrf.so'].hackrf_set_baseband_filter_bandwidth
hackrf_set_baseband_filter_bandwidth.restype = int_least32_t
hackrf_set_baseband_filter_bandwidth.argtypes = [POINTER(hackrf_dev_t),uint32_t]


hackrf_rffc5071_read=_libraries['libhackrf.so'].hackrf_rffc5071_read
hackrf_rffc5071_read.restype = int_least32_t
hackrf_rffc5071_read.argtypes = [POINTER(hackrf_dev_t),uint8_t,POINTER(uint16_t)]

hackrf_rffc5071_write=_libraries['libhackrf.so'].hackrf_rffc5071_write
hackrf_rffc5071_write.restype = int_least32_t
hackrf_rffc5071_write.argtypes = [POINTER(hackrf_dev_t),uint8_t,uint16_t]

hackrf_spiflash_write=_libraries['libhackrf.so'].hackrf_spiflash_write
hackrf_spiflash_write.restype = int_least32_t
hackrf_spiflash_write.argtypes = [POINTER(hackrf_dev_t),uint32_t,uint16_t,STRING]

hackrf_spiflash_read=_libraries['libhackrf.so'].hackrf_spiflash_read
hackrf_spiflash_read.restype = int_least32_t
hackrf_spiflash_read.argtypes = [POINTER(hackrf_dev_t),uint32_t,uint16_t,STRING]

hackrf_cpld_write=_libraries['libhackrf.so'].hackrf_cpld_write
hackrf_cpld_write.restype = int_least32_t
hackrf_cpld_write.argtypes = [POINTER(hackrf_dev_t),STRING,uint_least32_t]

hackrf_board_id_read=_libraries['libhackrf.so'].hackrf_board_id_read
hackrf_board_id_read.restype = int_least32_t
hackrf_board_id_read.argtypes = [POINTER(hackrf_dev_t),POINTER(uint8_t)]


hackrf_version_string_read=_libraries['libhackrf.so'].hackrf_version_string_read
hackrf_version_string_read.restype = int_least32_t
hackrf_version_string_read.argtypes = [POINTER(hackrf_dev_t),STRING,uint8_t]

hackrf_set_freq=_libraries['libhackrf.so'].hackrf_set_freq
hackrf_set_freq.restype = int_least32_t
hackrf_set_freq.argtypes = [POINTER(hackrf_dev_t),uint64_t]


###
hackrf_set_freq_explicit=_libraries['libhackrf.so'].hackrf_set_freq_explicit
hackrf_set_freq_explicit.restype = int_least32_t
hackrf_set_freq_explicit.argtypes = [POINTER(hackrf_dev_t),uint64_t,uint64_t,uint32_t]


hackrf_set_sample_rate_manual=_libraries['libhackrf.so'].hackrf_set_sample_rate_manual
hackrf_set_sample_rate_manual.restype = int_least32_t
hackrf_set_sample_rate_manual.argtypes = [POINTER(hackrf_dev_t),uint32_t,uint32_t]

hackrf_set_sample_rate=_libraries['libhackrf.so'].hackrf_set_sample_rate
hackrf_set_sample_rate.restype = int_least32_t
hackrf_set_sample_rate.argtypes = [POINTER(hackrf_dev_t),c_double]

hackrf_set_amp_enable=_libraries['libhackrf.so'].hackrf_set_amp_enable
hackrf_set_amp_enable.restype = int_least32_t
hackrf_set_amp_enable.argtypes = [POINTER(hackrf_dev_t),uint8_t]


###
hackrf_board_partid_serialno_read=_libraries['libhackrf.so'].hackrf_board_partid_serialno_read
hackrf_board_partid_serialno_read.restype = int_least32_t
hackrf_board_partid_serialno_read.argtypes = [POINTER(hackrf_dev_t),POINTER()]

hackrf_set_lna_gain= _libraries['libhackrf.so'].hackrf_set_lna_gain
hackrf_set_lna_gain.restype = int_least32_t
hackrf_set_lna_gain.argtypes = [POINTER(hackrf_dev_t),uint32_t]

hackrf_set_vga_gain=_libraries['libhackrf.so'].hackrf_set_vga_gain
hackrf_set_vga_gain.restype = int_least32_t
hackrf_set_vga_gain.argtypes = [POINTER(hackrf_dev_t),uint32_t]

hackrf_set_txvga_gain=_libraries['libhackrf.so'].hackrf_set_txvga_gain
hackrf_set_txvga_gain.restype = int_least32_t
hackrf_set_txvga_gain.argtypes = [POINTER(hackrf_dev_t),uint32_t]

hackrf_set_antenna_enable=_libraries['libhackrf.so'].hackrf_set_antenna_enable
hackrf_set_antenna_enable.restype = int_least32_t
hackrf_set_antenna_enable.argtypes = [POINTER(hackrf_dev_t),uint32_t]

hackrf_is_streaming = _libraries['libhackrf.so'].hackrf_is_streaming
hackrf_is_streaming.restype = int_least32_t
hackrf_is_streaming.argtypes = [POINTER(hackrf_dev_t)]

#####
hackrf_start_rx = _libraries['libhackrf.so'].hackrf_start_rx
hackrf_start_rx.restype = int_least32_t
hackrf_start_rx.argtypes = [POINTER(hackrf_dev_t),callback,c_void]

hackrf_stop_rx = _libraries['libhackrf.so'].hackrf_stop_rx
hackrf_stop_rx.restype = int_least32_t
hackrf_stop_rx.argtypes = [POINTER(hackrf_dev_t)]

###
hackrf_start_tx = _libraries['libhackrf.so'].hackrf_start_tx
hackrf_start_tx.restype = int_least32_t
hackrf_start_tx.argtypes = [POINTER(hackrf_dev_t),callback,c_void]

hackrf_stop_tx = _libraries['libhackrf.so'].hackrf_stop_tx
hackrf_stop_tx.restype = int_least32_t
hackrf_stop_tx.argtypes = [POINTER(hackrf_dev_t)]


###
hackrf_error_name = _libraries['libhackrf.so'].hackrf_error_name
hackrf_error_name.restype = STRING
hackrf_error_name.argtypes = [uint32_t]

###
hackrf_board_id_name = _libraries['libhackrf.so'].hackrf_board_id_name
hackrf_board_id_name.restype = STRING
hackrf_board_id_name.argtypes = [uint32_t]
####
hackrf_filter_path_name = _libraries['libhackrf.so'].hackrf_filter_path_name
hackrf_filter_path_name.restype = STRING
hackrf_filter_path_name.argtypes = [uint32_t]

hackrf_compute_baseband_filter_bw_round_down_lt = _libraries['libhackrf.so'].hackrf_compute_baseband_filter_bw_round_down_lt
hackrf_compute_baseband_filter_bw_round_down_lt.restype = int_least32_t
hackrf_compute_baseband_filter_bw_round_down_lt.argtypes = [uint32_t]

hackrf_compute_baseband_filter_bw = _libraries['libhackrf.so'].hackrf_compute_baseband_filter_bw
hackrf_compute_baseband_filter_bw.restype = int_least32_t
hackrf_compute_baseband_filter_bw.argtypes = [uint32_t]

if __name__=="__main__":
	print hackrf_init()
	a=hackrf_dev_t()
	print hackrf_open(pointer(a))
	print a
	id=uint8_t()
	print hackrf_board_id_read(a,pointer(id))
	print id



