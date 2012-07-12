import wx, scipy, scipy.fftpack
import numpy as np
from numpy import fft

from nerven_panels import *
from consts import *


class FftPanel(NervenPlotPanel):
    def do_update(self):
        nplots = len(self.epoc.sensors)
        fig = self.plot.get_figure()
        draw = True
        if self.draw_counter < PLOT_UPDATE_FREQ:
            self.draw_counter += 1
            draw = False
        if draw:
            for i, sensor in enumerate(self.epoc.sensors):
                self.draw_counter = 0
                axes = fig.add_subplot(nplots/2, 2, i+1)
                vals = np.array(self.epoc.sensor_tail[sensor], dtype='float')
                trans = abs(fft.rfft(vals))
                freqs = scipy.fftpack.fftfreq(vals.size/2+1, d=(1.0/SAMPLE_FREQ))
                axes.plot(freqs, trans)
                axes.set_ylabel(sensor)
                self.plotted_axes[sensor] = axes
            self.plot.draw()
            for sensor in self.epoc.sensors:
                fig.delaxes(self.plotted_axes[sensor])
        
