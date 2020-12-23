# static.py
# static physics object drawnType (ground, for example). Doesn't move.

from drawntype import DrawnType
from math import radians
from segment import segment
from sprite import Sprite
import yaml

class Static(DrawnType):

  MAX_SEGMENT_ERR_PX = 10

  def __init__(self, name, res_image_path, image_full_path, start_ext_id, start_sub_id, parent='.', meta_path=None, one_way=False):
    super().__init__(name, start_ext_id, start_sub_id, node_type='StaticBody2D', parent=parent)

    # start node string
    self.node_string = self._node_string(self.name, self.node_type, self.parent)
    # get position and rotation, if metadata exists
    if meta_path is not None:
      # load existent metadata
      with open(meta_path, 'r') as meta_file:
        metadata = yaml.safe_load(meta_file)
        if 'center' in metadata:
          self.node_string += f'position = Vector2( {metadata["center"]["x"]},{metadata["center"]["y"]} )\n'
        if 'rotation' in metadata:
          self.node_string += f'rotation = {radians(metadata["rotation"])}\n'

    # create sprite node(s), with myself as parent
    sprite = Sprite(name + '_sprite', res_image_path, start_ext_id, start_sub_id, parent=self.name)
    self.node_string += sprite.get_node_string()
    self.ext_resources_string = sprite.get_ext_resources_string()
    self.sub_resources_string = sprite.get_sub_resources_string()
    # set my current index ID's based on sprite
    self._curr_ext_id = sprite.get_last_ext_id()
    self._curr_sub_id = sprite.get_last_sub_id()

    # use provided image to create colliders (using segments from segment.py)
    colliders = segment(image_full_path, self.MAX_SEGMENT_ERR_PX)
    for idx, points_list in enumerate(colliders):
      self.polygon_node(idx, points_list, one_way)

  def polygon_node(self, idx, points, one_way):
    self.node_string += self._node_string(self.name + '_polygon_' + str(idx), 'CollisionPolygon2D', self.name)
    self.node_string += 'polygon = PoolVector2Array( '
    points_string = ""
    for point in points:
      points_string += str(point[0]) + ', ' + str(point[1]) + ', '
    self.node_string += points_string[:-2] + " )\n"
    self.node_string += "one_way_collision = " + "true" if one_way else "false"

  def get_ext_resources_string(self):
    return self.ext_resources_string

  def get_sub_resources_string(self):
    return self.sub_resources_string

  def get_node_string(self):
    return self.node_string

if __name__ == '__main__':
  static_node = Static('static', 'test/ground_test.png', 'test/ground_test.png', 1, 1)
  with open('tmp.tscn', 'w') as f:
    f.write(static_node.get_ext_resources_string() + '\n')
    f.write(static_node.get_sub_resources_string() + '\n')
    f.write(static_node.get_node_string())