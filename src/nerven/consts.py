import os.path

MAIN_TITLE = "nerven"
ABOUT_TEXT = """nerven is a visualisation and capture utility for the Emotiv EPOC. Written by Sharif Olorin/fractalcat <sio@tesser.org>."""
ABOUT_TITLE = "about nerven"
MAIN_FRAME_ID = -1
SENSOR_PLOT_ID = -2
SENSOR_PLOT_FRAME_ID = -3
MENU_QUAL_ID = 201
MENU_PLOT_ID = 202

POLL_TIMER_ID = 101
PLOT_TIMER_ID = 102
PLOT_POLL_FREQ = 2
POLL_FREQ = 2 # milliseconds

STATUS_FIELDS = 4

PLOT_LEN = 10
SENSOR_MAX = 8192
SAMPLE_FREQ = 128
PLOT_UPDATE_FREQ = 100

QUAL_FRAME_SIZE = (300, 400)
QUAL_TEXT_POS = (25, 80)
LINE_SIZE = 20

IMAGE_1020_X = 220
IMAGE_1020_Y = 25
IMAGE_1020_H = 468
IMAGE_1020_W = 500

IMAGE_1020 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'img', '1020.png'))

GENDERS = ('male', 'female') # yes, I know gender is not binary - EDF only accepts two values.

BRAIN_WAVES = {
    'delta' : (0.5, 4.0),
    'theta' : (4.0, 7.0),
    'alpha' : (7.0, 12.0),
    'beta' : (12.0, 30.0),
}


