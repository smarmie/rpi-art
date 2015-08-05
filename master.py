#!/usr/bin/python

from capture import Capture
from detect import Detect

import argparse
import cv2
import ConfigParser
from Queue import Queue
import sys
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="configuration file")
parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
arguments = parser.parse_args()
if arguments.config is None:
  config_file = 'rpi-art.conf'
else:
  config_file = arguments.config
config_defaults = { 'width': 640, 'height': 480, 'fps': 24, 'slices': 8, 'debug': 'False' }
config = ConfigParser.ConfigParser(config_defaults)
config.read(config_file)
if arguments.debug:
  config.set('rpi-art', 'debug', 'True')

capture_queue = Queue()
capture_thread = Capture(1, "Capture", capture_queue, config)
detect_thread = Detect(2, "Detect", capture_queue, config)
capture_thread.start()
detect_thread.start()

try:
  while True:
    if config.getboolean('rpi-art', 'debug'):
      print "Queue length", capture_queue.qsize()
    time.sleep(1)
except KeyboardInterrupt:
  capture_thread.exit.set()
  detect_thread.exit.set()
