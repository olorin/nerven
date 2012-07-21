import wx
import numpy as np
from numpy import fft

from nerven_panels import *
from consts import *
from epoc.epoc_bits import TAIL_LEN

class FourierPanel(NervenPlotPanel):
    def do_update(self):
        draw = True
        if self.draw_counter < PLOT_UPDATE_FREQ:
            self.draw_counter += 1
            draw = False
        if draw:
            fig = self.plot.get_figure()
            axes = fig.gca()
            acc_fft = np.array([0.0]*(SAMPLE_FREQ*TAIL_LEN/2+1), dtype='float')
            for i, sensor in enumerate(self.epoc_mgr.device.sensors):
                if self.cfg['only_use_good_sensors']:
                    if self.epoc_mgr.device.sensor_q[sensor] < self.cfg['contact_qual_threshold']:
                        continue
                self.draw_counter = 0
                vals = np.array(self.epoc_mgr.device.sensor_tail[sensor], dtype='float')
                sensor_fft = abs(fft.rfft(vals))
                acc_fft = np.add(acc_fft, sensor_fft)
            freqs = fft.fftfreq(vals.size/2+1, d=(1.0/SAMPLE_FREQ))
            axes.plot(freqs, acc_fft, 'x')
            axes.set_xlabel('Hz')
            #axes.set_autoscale_on(True)
            self.plot.draw()
            fig.delaxes(axes)
        
