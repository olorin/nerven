import wx

from config import NervenConfig
from callbacks import nerven_callbacks as callbacks

class PrefsPanel(wx.Panel):
    def __init__(self, parent, delete_callback=None):
        wx.Panel.__init__(self, parent)
        self.delete_callback = delete_callback
        self.cfg = NervenConfig()
        self.init_ctrls()

    def init_ctrls(self):
        self.opt_ctrls = {}
        sizer = wx.BoxSizer(wx.VERTICAL)
        for key in self.cfg.options:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            op = self.cfg.options[key]
            if op.type == 'bool':
                self.opt_ctrls[key] = wx.CheckBox(self, -1, op.description)
                self.opt_ctrls[key].SetValue(self.cfg[key])
                hsizer.Add(self.opt_ctrls[key])
            else:
                self.opt_ctrls[key] = wx.TextCtrl(self, value=str(self.cfg[key]))
                lbl = wx.StaticText(self, label=op.description)
                hsizer.Add(self.opt_ctrls[key], 1, wx.EXPAND)
                hsizer.AddSpacer((10,0))
                hsizer.Add(lbl, 1, wx.ALIGN_RIGHT, wx.EXPAND)
            sizer.Add(hsizer)
        self.save_btn = wx.Button(self, label='Save')
        self.close_btn = wx.Button(self, label='Close')
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_btn)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.close_btn)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.save_btn)
        hsizer.Add(self.close_btn)
        sizer.AddSpacer((0,10))
        sizer.Add(hsizer)
        sizer.AddSpacer((0,10))
        self.SetSizer(sizer)

    def do_update(self):
        pass
    
    def close(self):
        if self.delete_callback is not None:
            self.delete_callback()
        self.Destroy()

    def on_close(self, e):
        self.close()

    def on_save(self, e):
        for key in self.cfg.options:
            self.cfg[key] = self.opt_ctrls[key].GetValue()
        self.cfg.write()
        for cb in callbacks['update_config']:
            cb()
        self.close()


