// LCD style info
var lcdOn = "rgb(9,9,9)"
var lcdOff = "rgb(180,210,180)"
var lcdBg = "rgb(196,226,196)"


// LCD for receiver frequency
var rx0lcdFrequency = new SegmentDisplay("rx0lcdFrequency");
rx0lcdFrequency.pattern = "####.#####";
rx0lcdFrequency.intMin = 0;
rx0lcdFrequency.intMax = 0;
rx0lcdFrequency.colorOn = lcdOn;
rx0lcdFrequency.colorOff = lcdOff;

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
	
	rx0lcdFrequency.setIntValue(value);
	
	$.ajax({
		url: '/do',
		type: 'GET',
		contentType: 'application/json',
		data: { "centre_frequency":  hz  , "method":"set_centre_frequency" }		
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
		min: -20, 
		max: 50, 
		step: 5,
		animate: true,
		orientation: "horizontal",
		slide: function() {
			var gain = $("#rfgain").slider("value");
			console.debug("new gain" + gain + " dB");
		}
		});
	$("#ifgain").slider({
		min: -20,
		max: 50,
		step: 5,
		animate: true,
		orientation: "horizontal"
		});
	$("#AGC").button();
//		$("#rxtabs").tabs();

	$("#rx0ifbandwidth").slider({
		min: 200,
		max: 200000,
		step: 200,
		animate: true,
		orientation: "horizontal",
		slide: function() {
			var bandwidth = $("#rx0ifbandwidth").slider("value");
			console.debug("new bandwidth" + bandwidth + " Hz");
			
			$.ajax({
				url: '../receivers/0000',
				type: 'PUT',
				contentType: 'application/json',
				data: ' { "if_bandwidth": ' + bandwidth + ' }'		
			});
		}
		});
	$("#rx0afbandwidth").slider({
		min: 1000,
		max: 20000,
		step: 1000,
		animate: true,
		orientation: "horizontal",
		});
	$("#rx0squelch").slider({
		min: -100,
		max: 0,
		step: 10,
		animate: true,
		orientation: "horizontal",
		});

	$("#rx0modulation").buttonset();
	$("input[name='rx0modulation']").change(function(obj) {
		var mod = obj.target.value; // FIXME: Is this ok?
		console.debug("new modulation: " + mod);
		
		$.ajax({
			url: '../receivers/0000',
			type: 'PUT',
			contentType: 'application/json',
			data: ' { "demodulator": "' + mod + '" }'		
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

//		var tabs = $("#rxtabs").tabs();
//		var ul = tabs.find("ul");
//		$("<li><a href=\"#rx1\">blah</a></li>").appendTo(ul);
//		$("<div id=\"rx1\"><p>Blah</p></div>").appendTo(tabs);
//		$("<li><a href=\"#rx2\">blah</a></li>").appendTo(ul);
//		$("<div id=\"rx2\"><p>Blah</p></div>").appendTo(tabs);
//		$("<li><a href=\"#rx3\">blah</a></li>").appendTo(ul);
//		$("<div id=\"rx3\"><p>Blah</p></div>").appendTo(tabs);
//		tabs.tabs("refresh");
	
	// Waterfall
	var w = new Waterfall("waterfall-canvas", "waterfall-scale-canvas");
	var scrollinterval = window.setInterval(function () { w.scroll(); }, 50);
	var fetchinterval = window.setInterval(function() {
		var url = '../tuners/0000/waterfall';

		function onDataReceived(wf) {
			w.setCentreFrequency(wf['centre_frequency']);
			w.setSampleRate(wf['sample_rate']);
			w.update(wf['data']);
		}
		
		function onConnectionFailed() {
			$("#dialog").html("Server connection could not be established");
			$("#dialog").dialog({
				modal: true,
				buttons: {
					Ok: function() { $(this).dialog("close"); }
					}
				});
			clearInterval(scrollinterval);
			clearInterval(fetchinterval);
		}

		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			success: onDataReceived,
			error: onConnectionFailed,
		});
	}, 200);
	
	// Get board data
	$.ajax({
		url: '/do',
		type: 'GET',
		async   : true,
		data    : {'method':'get_board_data'},
		dataType :"json",
		crossDomain: true,
		success: function(info) {
			$("#tunerinfotext").html(
				"Board id: " + info['board_id'] + "<br/>" +
				"Version: " + info['version'] + "<br/>" +
				"Serial Number: " + info['serial_nr'] + "<br/>" 
				);
		}
		});
	
	// Get tuned frequency
	$.ajax({
		url: '../tuners/0000/control',
		type: 'GET',
		dataType: 'json',
		success: function(control) {
			lcdFrequency.setIntValue(control['centre_frequency'] / 10);
			rx0lcdFrequency.setIntValue(control['centre_frequency'] / 10);
			
			$("#rfgain").slider("value", control['rf_gain']);
			$("#ifgain").slider("value", control['if_gain']);
			$("#AGC").attr("checked", control['agc']).button("refresh");
		}
		});
		
	// Get receiver data
	$.ajax({
		url: '../receivers/0000',
		type: 'GET',
		dataType: 'json',
		success: function(info) {
			var demod = info['demodulator'];
			if (demod == "AM") {
				$("#rx0modulationAM").click();
			} else if (demod == "FM") {
				$("#rx0modulationFM").click();
			} else if (demod == "USB") {
				$("#rx0modulationUSB").click();
			} else if (demod == "LSB") {
				$("#rx0modulationLSB").click();
			}
			$("#rx0ifbandwidth").slider("value", info['if_bandwidth']);
			$("#rx0afbandwidth").slider("value", info['af_bandwidth']);
			$("#rx0squelch").slider("value", info['squelch_threshold']);
		}
		});			
});