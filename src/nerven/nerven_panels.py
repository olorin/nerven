import wx, wxmpl
from consts import *

class SensorPlot(wxmpl.PlotPanel):
    pass

class NervenPanel(wx.Panel):
    '''Abstract base class for every panel in the nerven Notebook.'''
    def do_update(self):
        pass

class NervenPlotPanel(NervenPanel):
    def __init__(self, parent, epoc):
        wx.Panel.__init__(self, parent)
        self.epoc = epoc
        self.init_plot()

    def init_plot(self):
        self.draw_counter = 1001
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot = SensorPlot(self, SENSOR_PLOT_ID)
        sizer.Add(self.plot, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.plotted_axes = {}
