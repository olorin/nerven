import wx

from nerven_panels import *
from colours import *
from consts import *

class QualityPanel(NervenPanel):
    def __init__(self, parent, epoc_mgr):
        wx.Panel.__init__(self, parent)
        self.epoc_mgr = epoc_mgr
        self.pnl = wx.Panel(self)
        self.init_text()
        self.init_image()
        self.do_update()
        self.Show(True)

    def _get_qual_lbl(self, val):
        if val is None:
            return "N/A"
        return "%f" % val

    def _colour_text(self, txt, val):
        if val < 0.4:
            txt.SetForegroundColour(RED)
        elif val < 0.8:
            txt.SetForegroundColour(ORANGE)
        else:
            txt.SetForegroundColour(BLACK)

    def init_image(self):
        self.image = None
        try:
            self.image = wx.Bitmap(IMAGE_1020)
        except:
            pass
        wx.EVT_PAINT(self, self.on_paint)

    def on_paint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.image, IMAGE_1020_X, IMAGE_1020_Y)

    def init_text(self):
        self.qual_text = {}
        self.colour_counter = 101
        for i, s in enumerate(self.epoc_mgr.device.sensors):
            y_pos = QUAL_TEXT_POS[1] + i*LINE_SIZE
            lbl = "%s: " % s
            pos = (QUAL_TEXT_POS[0], y_pos)
            wx.StaticText(self, label=lbl, pos=pos)
            lbl = self._get_qual_lbl(self.epoc_mgr.device.sensor_q[s])
            pos = (QUAL_TEXT_POS[0] + 100, y_pos)
            self.qual_text[s] = wx.StaticText(self, label=lbl, pos=pos)
            self._colour_text(self.qual_text[s], self.epoc_mgr.device.sensor_q[s])

    def do_update(self):
        for sensor in self.qual_text:
            if self.colour_counter > 100:
                val = self.epoc_mgr.device.sensor_q[sensor]
                lbl = self._get_qual_lbl(val)
                self.qual_text[sensor].SetLabel(lbl)
                self._colour_text(self.qual_text[sensor], val)
                self.colour_counter = 0
            self.colour_counter += 1
        
