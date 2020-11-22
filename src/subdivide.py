# subdivide.py
# trims image objects into minimum-area bounding boxes, and saves them.
# records metadata about the original translation & orientation of objects

import argparse
import cv2
import numpy as np
import os
import yaml

def subdivide_file(in_file, out_folder, do_output):
  # open file
  try:
    raw_image = cv2.imread(in_file, cv2.IMREAD_UNCHANGED)
    if do_output:
      print('Opened ' + in_file)
  except:
    raise Exception('Failed to read ' + str(in_file) +'. Does it exist?')
  if not os.path.isdir(out_folder):
        raise Exception("Output folder " + out_folder + " does not exist.")

  # recolor transparency as white
  mod_image = raw_image.copy()
  trans_mask = raw_image[:,:,3] == 0
  mod_image[trans_mask] = [255, 255, 255, 255]

  # get all present contours (using Otsu's binarization)
  gray = cv2.cvtColor(mod_image, cv2.COLOR_BGRA2GRAY)
  thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # get contours at the top of the hierarchy
  item_idxs = hierarchy[0][:][:,3] == -1
  item_ctrs = np.array(contours)[item_idxs]
  if do_output:
    print("Found " + str(len(contours)) + ' total contours')
    print('Identified ' + str(len(item_ctrs)) + ' items')

  # bound items
  for i, ctr in enumerate(item_ctrs):
      # get rotated bounding rect
      rect = cv2.minAreaRect(ctr) #((ctrx, ctry), (width, height), rotation)
      corners = cv2.boxPoints(rect)
      box = np.int0(corners)
      width = int(rect[1][0])
      height = int(rect[1][1])

      # warp rect into new image; good solution comes from
      # https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
      src_pts = box.astype("float32")
      dst_pts = np.array([[0, height-1],
                          [0, 0],
                          [width-1, 0],
                          [width-1, height-1]], dtype="float32")
      T = cv2.getPerspectiveTransform(src_pts, dst_pts) # transformation matrix
      warped = cv2.warpPerspective(raw_image, T, (width, height))

      # save image
      outfile = out_folder + '/item_' + str(i) + '.png'
      try:
        cv2.imwrite(outfile, warped)
      except:
        raise Exception("Failed to write to " + outfile + ".")

      # construct and save metadata
      outmeta = out_folder + '/item_' + str(i) + '.yaml'
      metadata = {'center':{'x':rect[0][0], 'y':rect[0][1]},
                  'rotation':rect[2],
                  'dimensions':{'width':width, 'height':height}
                 }
      with open(outmeta, 'w') as outyaml:
        yaml.dump(metadata, outyaml)
      if do_output:
        print('Saved item_' + str(i) + '.png, item_' + str(i) + '.yaml to ' + out_folder)

# define script behavior
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Trims images into independent items, and saves them as separate files.')
  parser.add_argument('filename', metavar='filename', type=str, help='image to subdivide')
  parser.add_argument('folder', metavar='folder', type=str, help='destination folder for result images')
  parser.add_argument('-o', '--output', default=False, action='store_true', help='include output logging')
  args = parser.parse_args()
  subdivide_file(args.filename, args.folder, args.output)
