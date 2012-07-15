from collections import deque
from numpy import arange
import wx, wxmpl
from matplotlib.ticker import MaxNLocator

from nerven_panels import *
from consts import *
from epoc.epoc_bits import TAIL_LEN

class SensorPlotPanel(NervenPlotPanel):
    def __init__(self, parent, epoc_mgr):
        NervenPlotPanel.__init__(self, parent, epoc_mgr)

    def do_update(self):
        self.update_plot()

    def update_plot(self):
        nplots = len(self.epoc_mgr.device.sensors)
        fig = self.plot.get_figure()
        draw = True
        if self.draw_counter < PLOT_UPDATE_FREQ:
            self.draw_counter += 1
            draw = False
        if draw:
            for i, sensor in enumerate(self.epoc_mgr.device.sensors):
                self.draw_counter = 0
                x = arange(0.0, TAIL_LEN, (1.0/SAMPLE_FREQ))
                axes = fig.add_subplot(nplots/2, 2, i+1)
                axes.plot(x, self.epoc_mgr.device.sensor_tail[sensor])
                axes.set_ylabel(sensor)
                axes.yaxis.set_major_locator(MaxNLocator(4))
                self.plotted_axes[sensor] = axes
            self.plot.draw()
            for sensor in self.epoc_mgr.device.sensors:
                fig.delaxes(self.plotted_axes[sensor])

    
    
