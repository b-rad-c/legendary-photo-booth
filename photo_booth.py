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

# change this to change where photos are saved
photo_dump = Path('/home/olmec/Desktop')

#
# picam
#

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (1200, 900)}))

#
# init gui app
#

app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=1200, height=900, keep_ar=False)
window = QWidget()

#
# input handlers
#

n = 0
def start_picture_capture():
    global n
    button.setEnabled(False)
    cfg = picam2.create_still_configuration()

    # change this to change how the folders and names are created for saved pics
    photo_path = photo_dump / datetime.datetime.now().strftime('%Y-%b-%d-%a/%H-%M-%f.jpg')
    os.makedirs(photo_path.parent, exist_ok=True)

    picam2.switch_mode_and_capture_file(cfg, photo_path, signal_function=qpicamera2.signal_done, delay=30)

def finish_picture_capture(job):
    global n
    picam2.wait(job)
    button.setEnabled(True)
    n += 1
    
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

button = QPushButton("Click to capture JPEG")
button.clicked.connect(start_picture_capture)

layout_v = QVBoxLayout()
layout_v.addWidget(button)

layout_h = QHBoxLayout()
layout_h.addWidget(qpicamera2, 80)
layout_h.addLayout(layout_v, 20)

window.setWindowTitle("Legendary Selfie")
window.resize(1800, 900)
window.setLayout(layout_h)

picam2.start()
window.show()

app.exec()
