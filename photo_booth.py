#!/usr/bin/python3

# This example is essentially the same as app_capture.py, however here
# we use the Qt signal/slot mechanism to get a callback (finish_picture_capture)
# when the capture, that is running asynchronously, is finished.
import os
import datetime
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

#
# config
#

pic_width = 1200
pic_height = 900
window_width = 1920
window_height = 1010
photo_dump = Path('/home/olmec/Desktop')

#
# picam
#

picam2 = Picamera2()
still_cfg = picam2.create_still_configuration()
preview_cfg = picam2.create_preview_configuration(main={'size': (pic_width, pic_height)})
picam2.configure(preview_cfg)


#
# init gui app
#

app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=pic_width, height=pic_height, keep_ar=True)
window = QWidget()

#
# input handlers
#

def start_picture_capture():
    # change this to change how the folders and names are created for saved pics
    photo_path = photo_dump / datetime.datetime.now().strftime('%Y-%b-%d-%a/%H-%M-%f.jpg')
    os.makedirs(photo_path.parent, exist_ok=True)

    picam2.switch_mode_and_capture_file(still_cfg, photo_path, signal_function=qpicamera2.signal_done, delay=30)

def finish_picture_capture(job):
    picam2.wait(job)
    
def keyboard_handler(e):
    if e.key() == Qt.Key_Q:
        qpicamera2.close()
        window.close()
    else:
        start_picture_capture()

#
# gui layout
#

qpicamera2.done_signal.connect(finish_picture_capture)
window.keyPressEvent = keyboard_handler

layout_h = QHBoxLayout()
layout_h.addWidget(qpicamera2, 80)

window.setWindowTitle('Legendary Selfie')
window.resize(window_width, window_height)
window.setLayout(layout_h)

picam2.start()
window.show()

app.exec()
