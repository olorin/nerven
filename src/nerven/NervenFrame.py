import wx

from epoc import *
from QualityPanel import QualityPanel
from SensorPlotPanel import SensorPlotPanel
from CapturePanel import CapturePanel
from PlaybackPanel import PlaybackPanel
from FourierPanel import FourierPanel
from BrainWavePanel import BrainWavePanel
from consts import *
from conf import *

class NervenFrame(wx.Frame):
    def __init__(self, parent, id, opts):
        wx.Frame.__init__(self, parent, MAIN_FRAME_ID, MAIN_TITLE)
        self.opts = opts
        self.status_bar = self.CreateStatusBar(STATUS_FIELDS)
        self._create_menu()
        self._set_poll_timer()
        self._init_epoc()
        self.init_notebook()
        self.init_capture_controls()
        self.draw_counter = 1001
        self.Show(True)
        self.Maximize(True)
        if not self.have_epoc:
            dlg = wx.MessageDialog(self, "Cannot open EEG data stream at %s." % self.opts.stream_path, "Error", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()


    def _init_epoc(self):
        self.epoc_mgr = EpocManager(ZeroDevice())
        try:
            self.epoc_mgr.device = EpocDevice(self.opts.stream_path)
            self.have_epoc = True
        except IOError:
            self.have_epoc = False

    def _set_poll_timer(self):
        self.timer = wx.Timer(self, POLL_TIMER_ID)
        self.timer.Start(POLL_FREQ)
        self.Bind(wx.EVT_TIMER, self.on_poll, self.timer)

    def init_capture_controls(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
    def init_notebook(self):
        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel)
        self.capture_panel = CapturePanel(self.nb, self.epoc_mgr)
        self.playback_panel = PlaybackPanel(self.nb, self.epoc_mgr)
        self.qual_panel = QualityPanel(self.nb, self.epoc_mgr)
        self.plot_panel = SensorPlotPanel(self.nb, self.epoc_mgr)
        self.fourier_panel = FourierPanel(self.nb, self.epoc_mgr)
        self.brain_wave_panel = BrainWavePanel(self.nb, self.epoc_mgr)
        self.nb.AddPage(self.capture_panel, "Capture")
        self.nb.AddPage(self.playback_panel, "Playback")
        self.nb.AddPage(self.qual_panel, "Sensor quality")
        self.nb.AddPage(self.plot_panel, "Plot")
#        self.nb.AddPage(self.fft_panel, "Fourier")
        self.nb.AddPage(self.fourier_panel, "Fourier")
        self.nb.AddPage(self.brain_wave_panel, "Brain waves")
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

    def _create_menu(self):
        bar = wx.MenuBar()
        bar.Append(self._create_menu_file(), "&File")
        self.SetMenuBar(bar)

    def _create_menu_file(self):
        menu = wx.Menu()
        about = menu.Append(wx.ID_ABOUT, "&About", "About nerven")
        exit_ = menu.Append(wx.ID_EXIT, "E&xit", "Exit nerven")
        self.Bind(wx.EVT_MENU, self.on_exit, exit_)
        self.Bind(wx.EVT_MENU, self.on_about, about)
        return menu

    def update_status_bar(self):
        if self.draw_counter < PLOT_UPDATE_FREQ:
            self.draw_counter += 1 
            return
        self.draw_counter = 0
        fields = [
            'capture: %s' % (('on (%s)' % self.capture_panel.writer.running()) if self.capture_panel.capture_on else 'off'),
            'x: %d' % self.epoc_mgr.device.cur_pkt.gyro.x,
            'y: %d' % self.epoc_mgr.device.cur_pkt.gyro.y,
            'battery: %d%%' % self.epoc_mgr.device.battery,
            ]
        self.status_bar.SetFields(fields)

    def on_exit(self, e):
        self.Close(True)

    def on_about(self, e):
        dialog = wx.MessageDialog(self, ABOUT_TEXT, ABOUT_TITLE, wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_poll(self, e):
        self.epoc_mgr.device.update()
        self.update_status_bar()
        if self.capture_panel.capture_on:
            self.capture_panel.write_packet()
        selection = self.nb.GetPage(self.nb.GetSelection())
        selection.do_update()

