# segment.py
# approximates all present highest-order contours (in input image) with segments

import argparse
import cv2
import numpy as np

def segment(image_path, error_max_px, trans_thresh=0.05):
  # open image
  try:
    raw_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  except:
    raise Exception('Failed to open ' + image_path + '.')
  # recolor transparency as white
  mod_image = raw_image.copy()
  trans_mask = raw_image[:,:,3] <= trans_thresh * 255
  mod_image[trans_mask] = [255, 255, 255, 255]
  # get all present external (high order) contours (using Otsu's binarization)
  gray = cv2.cvtColor(mod_image, cv2.COLOR_BGRA2GRAY)
  thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
  contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
  # construct segments
  ctr_segments = []
  for contour in contours:
    seg_raw = cv2.approxPolyDP(contour, error_max_px, True) #in form [..., [[x,y]],...]
    seg_clean = []
    for vertex in seg_raw:
      seg_clean.append((vertex[0][0], vertex[0][1])) #ea. ctr is list of tuples
    ctr_segments.append(seg_clean)
  return ctr_segments #list of lists of tuples (contours with lists of points)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Segments one (or more) high-order contour(s) present in input image')
  parser.add_argument('filename', metavar='filename', type=str, help='image to segment')
  parser.add_argument('error', metavar='error', type=float, help='maximum error (in px) between segment and input contour')
  args = parser.parse_args()
  res = segment(args.filename, args.error)
  print(res)