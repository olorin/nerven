import wx, wxmpl
from consts import *
from config import NervenConfig

class SensorPlot(wxmpl.PlotPanel):
    pass

class NervenPanel(wx.Panel):
    '''Abstract base class for every panel in the nerven Notebook.'''
    def do_update(self):
        pass

class NervenPlotPanel(NervenPanel):
    def __init__(self, parent, epoc_mgr):
        wx.Panel.__init__(self, parent)
        self.epoc_mgr = epoc_mgr
        self.cfg = NervenConfig()
        self.init_plot()

    def init_plot(self):
        self.draw_counter = 1001
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot = SensorPlot(self, SENSOR_PLOT_ID)
        self.sizer.Add(self.plot, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.plotted_axes = {}
