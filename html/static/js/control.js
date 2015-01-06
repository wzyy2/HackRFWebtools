// LCD style info
var lcdOn = "rgb(9,9,9)"
var lcdOff = "rgb(180,210,180)"
var lcdBg = "rgb(196,226,196)"
var current_status = 0
	//canvas resize
lcdcanvas = document.getElementById("lcdFrequency");
if ($("#tunerlcd").width() < 500 && $("#tunerlcd").width() > 300) {
	lcdcanvas.width = $("#tunerlcd").width() - 180;
} else if ($("#tunerlcd").width() < 350) {
	lcdcanvas.width = $("#tunerlcd").width() - 35;
	$("#lcdbg").css("width", lcdcanvas.width)
}

// LCD for receiver frequency
// var rx0lcdFrequency = new SegmentDisplay("rx0lcdFrequency");
// rx0lcdFrequency.pattern = "####.#####";
// rx0lcdFrequency.intMin = 0;
// rx0lcdFrequency.intMax = 0;
// rx0lcdFrequency.colorOn = lcdOn;
// rx0lcdFrequency.colorOff = lcdOff;

// LCD for frequency display
var lcdFrequency = new SegmentDisplay("lcdFrequency");
lcdFrequency.pattern = "####.#####";
lcdFrequency.intMin = 10000;
lcdFrequency.intMax = 170000000;
lcdFrequency.colorOn = lcdOn;
lcdFrequency.colorOff = lcdOff;

lcdFrequency.onValueChanged = function(value) {
	var hz = value * 10;

	console.debug("new frequency = " + hz + "Hz");

	// rx0lcdFrequency.setIntValue(value);

	$.ajax({
		url: '/do',
		type: 'GET',
		contentType: 'application/json',
		data: {
			"centre_frequency": hz,
			"method": "set_centre_frequency"
		}
	});
};

// LCD for memory display (not currently used)
var lcdMemory = new SegmentDisplay("lcdMemory");
lcdMemory.pattern = "##";
lcdMemory.intMin = 0;
lcdMemory.intMax = 99;
lcdMemory.zeroPad = true;
lcdMemory.colorOn = lcdOn;
lcdMemory.colorOff = lcdOff;

$(function() {
	$("#rfgain").slider({
		min: 0,
		max: 14,
		step: 14,
		animate: true,
		orientation: "horizontal",
		stop: function() {
			var gain = $("#rfgain").slider("value");
			console.debug("new gain" + gain + " dB");
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": gain,
					'method': 'set_rf_gain'
				}
			});
		}
	});
	$("#ifgain").slider({
		min: 0,
		max: 40,
		step: 8,
		animate: true,
		orientation: "horizontal",
		stop: function() {
			var gain = $("#ifgain").slider("value");
			console.debug("new gain" + gain + " dB");
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": gain,
					'method': 'set_if_gain'
				}
			});
		}
	});
	$("#bbgain").slider({
		min: 0,
		max: 62,
		step: 2,
		animate: true,
		orientation: "horizontal",
		stop: function() {
			var gain = $("#bbgain").slider("value");
			console.debug("new gain" + gain + " dB");
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": gain,
					'method': 'set_bb_gain'
				}
			});
		}
	});

	$("#bbbandwidth").slider({
		min: 0,
		max: 28000000,
		step: 200,
		animate: true,
		orientation: "horizontal",
		stop: function() {
			var bandwidth = $("#bbbandwidth").slider("value");
			console.debug("new bandwidth" + bandwidth + " Hz");

			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": bandwidth,
					'method': 'set_bb_bandwidth'
				}
			});
		}
	});
	$("#rx0squelch").slider({
		min: -100,
		max: 0,
		step: 10,
		animate: true,
		orientation: "horizontal",
	});

	$("input[name='rx0modulation']").change(function(obj) {
		var mod = obj.target.value; // FIXME: Is this ok?
		console.debug("new modulation: " + mod);

		function onDataReceived(wf) {}

		$.ajax({
			url: '/do',
			type: 'GET',
			dataType: 'json',
			data: {
				"demodulator": mod,
				'method': 'demodulator'
			},
			success: onDataReceived
		});
	});

	$("#fftrate").change(
		function() {
			var rate = $("#fftrate").val();
			console.debug("new fft rate" + rate + " hz");
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": rate,
					'method': 'set_fft_rate'
				}
			});
		});
	$("#fftsize").change(
		function() {
			var size = $("#fftsize").val();
			console.debug("new fft size" + size);
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": size,
					'method': 'set_fft_size'
				}
			});
		});
	$("#reset").click(
		function() {
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					'method': 'reset'
				},
				success: function(info) {
					if (info['ret'] == "ok")
						location.reload();
				}
			});
		});

	$("#control-right-btn").click(
		function() {
			$('#control-right').css("display", "block");
			$('#control-left').css("display", "none");
		});

	$("#control-left-btn").click(
		function() {
			$('#control-right').css("display", "none");
			$('#control-left').css("display", "block");
		});

	$("#samplerate").change(
		function() {
			var rate = $("#samplerate").val();
			console.debug("new sample rate" + rate + " hz");
			$.ajax({
				url: '/do',
				type: 'GET',
				dataType: 'json',
				data: {
					"value": rate,
					'method': 'set_sample_rate'
				}
			});
		});
});

$(document).ready(function() {
	// Apply LCD styles and initial 7 seg values
	$(".lcd").css("background-color", lcdBg);
	$(".lcd").css("color", lcdOn);
	lcdFrequency.setIntValue(10000000);
	lcdMemory.setIntValue(0);

	lcdFrequency.enableMouse();
	lcdMemory.enableMouse();
	//rx0lcdFrequency.enableMouse();

	// Waterfall
	var w = new Waterfall("waterfall-canvas", "waterfall-scale-canvas");
	var s = new Spectrum("spectrum-canvas", "spectrum-scale-canvas");
	var scrollinterval = null;
	var fetchinterval = null;

	function startStreaming() {
		scrollinterval = window.setInterval(function() {
			w.scroll();
		}, 80);
		fetchinterval = window.setInterval(function() {
			var url = '/do';

			function onDataReceived(wf) {
				if(wf['exit'] == 1)
					onConnectionFailed();
				
				w.setCentreFrequency(wf['centre_frequency']);
				w.setSampleRate(wf['sample_rate']);
				w.update(wf['data']);

				s.setCentreFrequency(wf['centre_frequency']);
				s.setSampleRate(wf['sample_rate']);
				s.update(wf['data']);
			}

			function onConnectionFailed() {
				$("#dialog").html("Server connection could not be established");
				$("#dialog").dialog({
					modal: true,
					buttons: {
						Ok: function() {
							$(this).dialog("close");
						}
					}
				});
				clearInterval(scrollinterval);
				clearInterval(fetchinterval);
			}

			$.ajax({
				url: url,
				type: 'GET',
				data: {
					'method': 'waterfall'
				},
				dataType: 'json',
				success: onDataReceived,
				error: onConnectionFailed,
			});
		}, 200);
	}

	function stopStreaming() {
		clearInterval(scrollinterval);
		clearInterval(fetchinterval);
	}

	// Get board data
	$.ajax({
		url: '/do',
		type: 'GET',
		async: true,
		data: {
			'method': 'get_board_data'
		},
		dataType: "json",
		crossDomain: true,
		success: function(info) {
			$("#tunerinfotext").html(
				"Board Name: " + info['board_name'] + "<br/>" +
				"Version: " + info['version'] + "<br/>"
				// + "Serial Number: " + info['serial_nr'] + "<br/>" 
			);
		}
	});

	// Get board settings
	$.ajax({
		url: '/do',
		type: 'GET',
		data: {
			'method': 'get_control_options'
		},
		dataType: 'json',
		success: function(control) {
			lcdFrequency.setIntValue(control['centre_frequency'] / 10);
			//rx0lcdFrequency.setIntValue(control['centre_frequency'] / 10);

			$("#rfgain").slider("value", control['rf_gain']);
			$("#ifgain").slider("value", control['if_gain']);
			$("#bbgain").slider("value", control['bb_gain']);
			$("#fftrate").val(control['fft_rate']);
			$("#fftsize").val(control['fft_size']);
			$("#samplerate").val(control['sample_rate']);
			$('.selectpicker').selectpicker('refresh');
			//				
			if (control['current_status'] == 0) {
				stopStreaming();
				current_status = 0
				$("#STOP").addClass("active");
			} else if (control['current_status'] == 1) {
				current_status = 1
				startStreaming();
				$("#STARTRX").addClass("active");
			} else if (control['current_status'] == 2) {
				startStreaming();
				current_status = 2
				$("#STARTTX").addClass("active");
			}
			// $( "#status_control" ).buttonset("refresh");

			var demod = control['demodulator'];
			if (demod == "AM") {
				$("#rx0modulationAM").addClass("active");
			} else if (demod == "WFM") {
				$("#rx0modulationFM").addClass("active");
			} else if (demod == "USB") {
				$("#rx0modulationUSB").addClass("active");
			} else if (demod == "LSB") {
				$("#rx0modulationLSB").addClass("active");
			} else if (demod == "NFM") {
				$("#rx0modulationNFM").addClass("active");
			}
			// $("#rx0modulation").btn("refresh");

			$("#bbbandwidth").slider("value", control['bb_bandwidth']);
			$("#rx0squelch").slider("value", control['squelch_threshold']);
		}
	});


	$("#STARTRX").click(function(event) {
		if (current_status == 0) {
			startStreaming();
		}
		$.ajax({
			url: '/do',
			type: 'GET',
			dataType: 'json',
			data: {
				'method': 'start_rx'
			}
		});
		current_status = 1;
	});
	$("#STOP").click(function(event) {
		current_status = 0;
		stopStreaming();
		$.ajax({
			url: '/do',
			type: 'GET',
			dataType: 'json',
			data: {
				'method': 'stop'
			}
		});
	});
	$("#STARTTX").click(function(event) {
		if (current_status == 0) {
			startStreaming();
		}
		$.ajax({
			url: '/do',
			type: 'GET',
			dataType: 'json',
			data: {
				'method': 'start_tx'
			}
		});
		current_status = 2;
	});

});