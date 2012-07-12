import wx, scipy, scipy.fftpack
import numpy as np
from numpy import fft

from nerven_panels import *
from consts import *
from epoc.epoc_bits import TAIL_LEN

class FourierSumPanel(NervenPlotPanel):
    def do_update(self):
        draw = True
        if self.draw_counter < PLOT_UPDATE_FREQ:
            self.draw_counter += 1
            draw = False
        if draw:
            fig = self.plot.get_figure()
            axes = fig.gca()
            acc_fft = np.array([0.0]*(SAMPLE_FREQ*TAIL_LEN/2+1), dtype='float')
            for i, sensor in enumerate(self.epoc.sensors):
                self.draw_counter = 0
                vals = np.array(self.epoc.sensor_tail[sensor], dtype='float')
                sensor_fft = abs(fft.rfft(vals))
                acc_fft = np.add(acc_fft, sensor_fft)
            freqs = scipy.fftpack.fftfreq(vals.size/2+1, d=(1.0/SAMPLE_FREQ))
            axes.plot(freqs, acc_fft)
            axes.set_xlabel('Hz')
            #axes.set_autoscale_on(True)
            self.plot.draw()
            fig.delaxes(axes)
        
