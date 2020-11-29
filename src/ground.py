import cv2
import numpy as np
from drawntype import DrawnType
from sprite import Sprite

class Ground(DrawnType):

  SEGMENT_LEN_PX = 50

  def __init__(self, name, res_image_path, image_full_path, start_ext_id, start_sub_id, parent='.'):
    super().__init__(name, start_ext_id, start_sub_id, node_type='StaticBody2D', parent=parent)

    # start node string
    self.node_string = self._node_string(self.name, self.node_type, self.parent)

    # create ground sprite node(s), with myself as parent
    ground_sprite = Sprite(name + '_sprite', res_image_path, start_ext_id, start_sub_id, parent=self.name)
    self.node_string += ground_sprite.get_node_string()
    self.ext_resources_string = ground_sprite.get_ext_resources_string()
    self.sub_resources_string = ground_sprite.get_sub_resources_string()
    # set my current index ID's based on sprite
    self._curr_ext_id = ground_sprite.get_last_ext_id()
    self._curr_sub_id = ground_sprite.get_last_sub_id()

    # use provided image to create segments
    self.segments = 0
    self.generate_segments(image_full_path, self.SEGMENT_LEN_PX)

  # create resources for a segment node (CollisionShape2D, SegmentShape2D)
  def segment_node(self, start_point=(0, 0), end_point=(0, 0)):
    # create sub-resource first
    used_sub_id = self._get_sub_id_safe()
    self.sub_resources_string += self._sub_resource_string('SegmentShape2D', used_sub_id)
    self.sub_resources_string += f'a = Vector2( {start_point[0]}, {start_point[1]} )\n'
    self.sub_resources_string += f'b = Vector2( {end_point[0]}, {end_point[1]} )\n'
    # create collider node
    self.node_string += self._node_string('segment_' + str(self.segments), 'CollisionShape2D', self.name)
    self.node_string += f'shape = SubResource( {used_sub_id} )\n'
    self.segments += 1

  # use OpenCV to get points for segments
  # most of this is the same as in subdivide.py
  def generate_segments(self, image_path, segment_len_px):
    # open file, if we can
    try:
      raw_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    except:
      # don't generate segments
      return
    # recolor transparency as white (using threshold)
    trans_thresh = 0.05
    mod_image = raw_image.copy()
    trans_mask = raw_image[:,:,3] <= trans_thresh * 255
    mod_image[trans_mask] = [255, 255, 255, 255]
    # get all present external contours (using Otsu's binarization)
    gray = cv2.cvtColor(mod_image, cv2.COLOR_BGRA2GRAY)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

    # create segments out of each contour
    max_x = raw_image.shape[1] - 1
    max_y = raw_image.shape[0] - 1
    for ctr in contours:
      # traverse contour; assume we start on "main contour"
      main_ctr = True
      main_cooldown = 4
      last_point = None
      for i, el in enumerate(ctr):
        # manage weird data structure
        point = tuple(el[0])
        # if we hit the edge, stop making segments until we hit another edge
        if main_cooldown == 0 and point[0] == 0 or point[0] == max_x or point[1] == 0 or point[1] == max_y:
          main_ctr = not main_ctr
          main_cooldown = 4
          continue
        elif main_cooldown > 0:
          main_cooldown -= 1
        # if we're on the main contour, create segments at regular intervals
        if main_ctr and (i % segment_len_px == 0 or i == len(ctr) - 1):
          if last_point is not None:
            self.segment_node(last_point, point)
          last_point = point


  def get_ext_resources_string(self):
    return self.ext_resources_string

  def get_sub_resources_string(self):
    return self.sub_resources_string

  def get_node_string(self):
    return self.node_string

if __name__ == '__main__':
  ground_node = Ground('ground', 'test/ground_test.png', 'test/ground_test.png', 1, 1)
  with open('tmp.tscn', 'w') as f:
    f.write(ground_node.get_ext_resources_string() + '\n')
    f.write(ground_node.get_sub_resources_string() + '\n')
    f.write(ground_node.get_node_string())
