import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import Queue
import threading
import time

class Capture(threading.Thread):
  def __init__(self, threadID, name, queue, config):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.queue = queue
    self.config = config
    self.exit = threading.Event()
    self.totalframes = 0


  def run(self):
    # initialize camera
    try:
      self.camera = PiCamera()
      self.camera.resolution = (self.config['WIDTH'], self.config['HEIGHT'])
      self.camera.framerate = 12
      rawCapture = PiRGBArray(self.camera, size=(self.config['WIDTH'], self.config['HEIGHT']))
      time.sleep(1)
    except:
      print "Error opening camera"
      exit(1)
    # add frames to queue
    for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      self.queue.put(frame.array)
      self.totalframes += 1
      if self.config['debug'] == 1:
        print "Captured frame", self.totalframes
      rawCapture.truncate(0)
      if self.exit.is_set():
        self.camera.close()
        break

