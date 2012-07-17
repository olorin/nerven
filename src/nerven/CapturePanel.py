import os, os.path, datetime

import wx
from wx import calendar

import writer
from util import *
from consts import *

class CapturePanel(wx.Panel):
    def __init__(self, parent, epoc_mgr):
        wx.Panel.__init__(self, parent)
        self.epoc_mgr = epoc_mgr
        self.capture_path = None
        self.cur_dir = os.path.expanduser("~")
        self.capture_on = False
        self.init_controls()
        self.Show(True)
        self.Layout()
        # hidden after callling Layout so the formatting works
        if self.fmt_select.GetValue() != 'edf':
            self.show_edf_ctrls(False)

    def do_update(self):
        pass

    def init_controls(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer0 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.fname_ctrl = wx.TextCtrl(self)
        browse_button = wx.Button(self, label='Choose file')
        self.fmt_select = wx.ComboBox(self, choices=writer.backends.keys(), style=wx.CB_READONLY)
        self.fmt_select.SetValue(writer.backends.keys()[0])
        self.cap_button = wx.ToggleButton(self, label='Capture')
        self.edf_ctrls = {}
        self.edf_ctrls['patient'] = (wx.TextCtrl(self),
                                     wx.StaticText(self, label="Name:"))
        self.edf_ctrls['gender'] = (wx.ComboBox(self, choices=('male', 'female'), style=wx.CB_READONLY), 
                                    wx.StaticText(self, label="Sex:"))
        self.edf_ctrls['patient_additional'] = (wx.TextCtrl(self), 
                                                wx.StaticText(self, label="Additional info"))
        self.edf_ctrls['birthdate'] = (calendar.CalendarCtrl(self), 
                                       wx.StaticText(self, label="Birthdate"))
        self.Bind(wx.EVT_BUTTON, self.on_browse, browse_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_capture_btn, self.cap_button)
        self.Bind(wx.EVT_COMBOBOX, self.on_fmt_select, self.fmt_select)
        hsizer0.Add(self.fname_ctrl, 1)
        hsizer0.Add(browse_button, 0)
        hsizer0.Add(self.fmt_select, 0)
        hsizer0.Add(self.cap_button, 0, wx.ALIGN_RIGHT)
        vsizer.Add(hsizer0, 0, wx.EXPAND)
        gsizer = wx.GridSizer(len(self.edf_ctrls.keys()))
        for k in self.edf_ctrls:
            ec, lbl = self.edf_ctrls[k]
            gsizer.Add(lbl, 0)
            gsizer.Add(ec, 2, wx.ALIGN_RIGHT)
        vsizer.Add(gsizer)
        self.SetSizer(vsizer)

    def start_capture(self):
        backend = self.fmt_select.GetValue()
        if not self.capture_path:
            dlg = wx.MessageDialog(self, "You must select a file to write to.", "Error", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        writer_cls = writer.backends[backend]
        if backend != 'edf':
            self.writer = writer_cls(self.capture_path, self.epoc_mgr.device)
        else:
            edf_extra = self.get_edf_extra()
            self.writer = writer_cls(self.capture_path, self.epoc_mgr.device, edf_extra)
        self.npackets = 0
        for k in self.edf_ctrls:
            ec, lbl = self.edf_ctrls[k]
            ec.Enable(False)
        self.capture_on = True

    def stop_capture(self):
        self.writer.close()
        self.capture_path = ""
        self.fname_ctrl.SetValue('')
        for k in self.edf_ctrls:
            ec, lbl = self.edf_ctrls[k]
            ec.Enable(True)
        self.capture_on = False

    def write_packet(self):
        pkt = self.epoc_mgr.device.cur_pkt
        self.writer.write_packet(pkt)
        self.npackets += 1

    def show_edf_ctrls(self, visible):
        for k in self.edf_ctrls:
            ec, lbl = self.edf_ctrls[k]
            ec.Show(visible)
            lbl.Show(visible)

    def on_capture_btn(self, e):
        val = self.cap_button.GetValue()
        if val == self.capture_on:
            return
        if val:
            self.start_capture()
        else:
            self.stop_capture()

    def on_fmt_select(self, e):
        edf = self.fmt_select.GetValue() == 'edf'
        self.show_edf_ctrls(edf)

    def on_browse(self, e):
        ext = self.fmt_select.GetValue()
        if ext == 'raw':
            ext = 'epoc'
        wildcard = "*.%s" % ext
        dlg = wx.FileDialog(self, "Select output file", self.cur_dir, "", wildcard, wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.cur_dir = dlg.GetDirectory()
            self.capture_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
            self.fname_ctrl.SetValue(self.capture_path)
        dlg.Destroy()

    def get_edf_extra(self):
        extra = {}
        for k in ('patient','patient_additional'):
            ec, lbl = self.edf_ctrls[k]
            if ec.GetValue():
                extra[k] = ec.GetValue()
        gender, lbl = self.edf_ctrls['gender']
        gender = gender.GetValue()
        if gender in GENDERS:
            extra['gender'] = 1 if gender == 'male' else 0
        cal, lbl = self.edf_ctrls['birthdate']
        today = date_to_wxdate(datetime.date.today())
        if cal.GetDate() != today:
            extra['birthdate'] = wxdate_to_date(cal.GetDate())
        return extra
