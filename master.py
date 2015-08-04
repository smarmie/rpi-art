#!/usr/bin/python

import cv2
from Queue import Queue
import threading
import time
from capture import Capture
from detect import Detect

# some constants
config = dict()
config['HEIGHT'] = 720
config['WIDTH'] = 1280
config['FPS'] = 4
config['TOTAL_SLICES'] = 8
config['debug'] = 1

capture_queue = Queue()
capture_thread = Capture(1, "Capture", capture_queue, config)
detect_thread = Detect(2, "Detect", capture_queue, config)
capture_thread.start()
detect_thread.start()

try:
  while True:
    if config['debug'] == 1:
      print "Queue length", capture_queue.qsize()
    time.sleep(1)
except KeyboardInterrupt:
  capture_thread.exit.set()
  detect_thread.exit.set()
