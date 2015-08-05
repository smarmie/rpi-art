import cv2
import ConfigParser
import Queue
import threading
import time

class Detect(threading.Thread):
  def __init__(self, threadID, name, queue_in, config):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.queue_in = queue_in
    self.config = config
    self.exit = threading.Event()
    self.prevFrame = None
    self.totalframes = 0


  def run(self):
    while not self.exit.is_set():
      if self.queue_in.empty():
        continue
      frame = self.queue_in.get()
      if self.queue_in.qsize() > int(self.config.get('rpi-art', 'max_queue_size')):
        continue

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (21, 21), 0)

      # if the first frame is None, initialize it
      if self.prevFrame is None:
        self.prevFrame = gray
        continue

      # compute the absolute difference between the current frame and the previous frame
      frameDelta = cv2.absdiff(self.prevFrame, gray)
      thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

      # dilate the thresholded image to fill in holes, then find contours on thresholded image
      thresh = cv2.dilate(thresh, None, iterations=2)
      (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      detected_contours = list()
      # loop over the contours
      for contour in contours:
        # if the contour is too small, ignore it
        #if cv2.contourArea(c) < args["min_area"]:
        #  continue
        # compute the bounding box for the contour
        (x1, y1, x2, y2) = cv2.boundingRect(contour)
        detected_contours.append((x1, y1, x2, y2))

      self.totalframes += 1
      if self.config.getboolean('rpi-art', 'debug'):
        print "Processed frame", self.totalframes

