class LowPass():
    FIR_LENGTH = 64

    def __init__(self):
        self._passband = 0
        self._reqDecimation = 0
        self._reqOutputRate = 48 * 1000 
        pass

    def setPassband(self, hz):
        self._passband = hz
        pass

    def setDecimation(self, n):
        self._reqDecimation = n
        self._reqOutputRate = 0 
        pass

    def setOutputSampleRate(self, hz):
        self._reqDecimation = 0
        self._reqOutputRate = hz 
        pass

    def working(self):
        pass

    def recalculate(self):
        pass