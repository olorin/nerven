import os, os.path, datetime

import wx
from wx import calendar

from epoc import EpocDevice
import writer
from util import *
from consts import *
from nerven_panels import *

class PlaybackPanel(NervenPanel):
    def __init__(self, parent, epoc_mgr):
        wx.Panel.__init__(self, parent)
        self.epoc_mgr = epoc_mgr
        self.current_device = self.epoc_mgr.device
        self.playback_path = None
        self.cur_dir = os.path.expanduser("~")
        self.init_controls()
        self.Show(True)

    def init_controls(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.fname_ctrl = wx.TextCtrl(self)
        browse_button = wx.Button(self, label='Choose file')
        self.load_button = wx.Button(self, label='Start')
        self.stop_button = wx.Button(self, label='Stop')
        self.stop_button.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.on_browse, browse_button)
        self.Bind(wx.EVT_BUTTON, self.on_load_btn, self.load_button)
        self.Bind(wx.EVT_BUTTON, self.on_stop_btn, self.stop_button)
        hsizer0.Add(self.fname_ctrl, 1)
        hsizer0.Add(browse_button, 0)
        hsizer0.Add(self.load_button, 0, wx.ALIGN_RIGHT)
        hsizer0.Add(self.stop_button, 0, wx.ALIGN_RIGHT)
        vsizer.Add(hsizer0, 0, wx.EXPAND)
        self.SetSizer(vsizer)

    def start_playback(self):
        self.current_device = self.epoc_mgr.device
        self.epoc_mgr.device = EpocDevice(self.playback_path)
        self.load_button.Enable(False)
        self.stop_button.Enable(True)

    def stop_playback(self):
        self.epoc_mgr.device = self.current_device
        self.load_button.Enable(True)
        self.stop_button.Enable(False)

    def on_load_btn(self, e):
        self.start_playback()

    def on_stop_btn(self, e):
        self.stop_playback()

    def on_browse(self, e):
        ext = 'epoc'
        wildcard = "*.%s" % ext
        dlg = wx.FileDialog(self, "Select data file", self.cur_dir, "", wildcard, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.cur_dir = dlg.GetDirectory()
            self.playback_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
            self.fname_ctrl.SetValue(self.playback_path)
        dlg.Destroy()

