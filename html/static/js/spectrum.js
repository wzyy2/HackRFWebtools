function Spectrum(spectrum_target, scale_target) {
	this.canvas = document.getElementById(spectrum_target);
	this.context = this.canvas.getContext("2d");

	this.canvas.width = $('#spectrum').width();
	this.canvas.height = $('#spectrum').height();

	if (scale_target != null) {
		this.scale_canvas = document.getElementById(scale_target);
		this.scale_context = this.scale_canvas.getContext("2d");
	} else {
		this.scale_canvas = null;
		this.scale_context = null;
	}

	this.scale_canvas.width = this.canvas.width;
	this.scale_canvas.height = this.canvas.height;

	this.centreFrequency = 0;
	this.sampleRate = 0;
	this.nMarkers = 3; // number of markers either side of centre

	// Create waterfall colour scheme
	this.palette = new Array();
	for (var n = 0; n < 256; n++) {
		var r, g, b;
		if (n < 64) {
			r = 0;
			g = 0;
			b = n * 4;
		} else if (n < 128) {
			r = 0;
			g = (n - 64) * 4;
			b = 255;
		} else if (n < 192) {
			r = (n - 128) * 4;
			g = 255;
			b = 255 - (n - 128) * 4;
		} else {
			r = 255;
			g = 255 - (n - 192) * 4;
			b = 0;
		}
		//		r = 0; g = n; b = 0; //matrix!
		this.palette.push("rgba(" + r + "," + g + "," + b + ", 0.5)");
	}

	this.my_gradient = this.context.createLinearGradient(0, 0, 0, this.canvas.height);
	this.my_gradient.addColorStop(0, "black");
	this.my_gradient.addColorStop(1, "rgba(80,80,80,1.0)");

	// Pre-fill canvas
	this.context.fillStyle = this.my_gradient;
	this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);
}

Spectrum.prototype.setCentreFrequency = function(f) {
	this.centreFrequency = f;
	this.redrawScale();
}

Spectrum.prototype.setSampleRate = function(r) {
	this.sampleRate = r;
	this.redrawScale();
}

Spectrum.prototype.redrawScale = function() {
	if (this.scale_canvas == null)
		return;

	var ctx = this.scale_context;
	var w = this.scale_canvas.width;
	var h = this.scale_canvas.height;

	// Clear scale canvas
	ctx.fillStyle = "rgba(0,0,0,0)";
	ctx.fillRect(0, 0, w, h - 18);
	ctx.fillStyle = "rgba(0,0,0,1.0)";
	ctx.fillRect(0, h - 18, w, 18);

	// Redraw scale text
	ctx.font = "12px Arial";
	ctx.textAlign = "center";
	ctx.strokeStyle = "white";
	var freq = this.centreFrequency - this.sampleRate / 2;
	for (n = 0; n < this.nMarkers * 2 + 1; n++) {
		var xpos = n * w / this.nMarkers / 2;
		var label = (freq / 1000000.0).toFixed(3).toString();
		ctx.strokeText(label, xpos, h - 2);
		freq = freq + this.sampleRate / this.nMarkers / 2;
	}

	// // Redraw markers
	// var grad = ctx.createLinearGradient(0, 0, 0, h);
	// grad.addColorStop(0, "rgba(0,0,0,0)");
	// grad.addColorStop(0.5, "rgba(255,255,255,1)");
	// grad.addColorStop(1, "rgba(0,0,0,0)");
	// ctx.beginPath();
	// for (n = 1; n < this.nMarkers * 2; n++) {
	// 	var xpos = n * w / this.nMarkers / 2;

	// 	ctx.moveTo(xpos, 0);
	// 	ctx.lineTo(xpos, h - 15);
	// }
	// ctx.strokeStyle = grad;
	// ctx.stroke();

}

var iirFftData = new Array([1024]);
for(var i = 0; i < 1024; i++) {
	iirFftData[i] = 0.0;
}
	

Spectrum.prototype.update = function(series) {
	var ctx = this.context;
	var w = this.canvas.width / series.length;
	// Pre-fill canvas
	this.context.fillStyle = this.my_gradient;
	this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

	function colour(self, val) {
			val = val * 255.0;
			val = Math.floor(val);
			if (val < 0) val = 0;
			if (val > 255) val = 255;
			return self.palette[val];
		}
		// series[bin]  -50 10    0  60
		// Draw new series into first row
		// for (var bin = 0; bin < series.length; bin++) {
		// 	ctx.fillStyle = "white"; // x2 here for some reason?
		// 	y = ((series[bin] + 50) / 60) * this.canvas.height;
		// 	ctx.fillRect(Math.floor(bin * w), y, Math.ceil(w), 1);
		// }

	this.context.strokeStyle = "#fff";
	this.context.lineWidth = 1;
	this.context.beginPath();

	for (n = 1; n < series.length; n++) {
		iirFftData[n] = (1.0 - 0.4) * iirFftData[n] + 0.4 * series[n];
		
	}

	this.context.moveTo(0,  (-iirFftData[0] / 100) * this.canvas.height - 20);
	for (n = 1; n < series.length; n++) {
		this.context.lineTo(Math.floor(n * w), (-iirFftData[n] / 100) * this.canvas.height - 20);
	}
	this.context.stroke();

}