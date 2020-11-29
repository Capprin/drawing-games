from drawntype import DrawnType
from math import radians
import yaml

class Physics(DrawnType):

  def __init__(self, name, res_image_path, meta_path, start_ext_id, start_sub_id, parent='.'):
    super().__init__(name, start_ext_id, start_sub_id, node_type='RigidBody2D', parent=parent)

    self.node_string = self._node_string(self.name, self.node_type, self.parent)

    # load metadata into dict
    with open(meta_path, 'r') as meta_file:
      metadata = yaml.safe_load(meta_file)
    
    # add transform info
    if 'center' in metadata:
      self.node_string += f'position = Vector2( {metadata["center"]["x"]}, {metadata["center"]["y"]} )\n'
    if 'rotation' in metadata:
      self.node_string += f'rotation = {radians(metadata["rotation"])}\n'

    # add sprite node manually (different process for metadata)
    used_ext_id = self._get_ext_id_safe()
    self.node_string += self._node_string(name + '_sprite', 'Sprite', self.name)
    self.ext_resources_string = self._ext_resource_string(res_image_path, 'Texture', used_ext_id)
    self.node_string += f'texture = ExtResource( {used_ext_id} )\n'

    # add collision polygon
    self.node_string += self._node_string(name + '_collider', 'CollisionPolygon2D', self.name)
    if 'dimensions' in metadata:
      delta_x = metadata['dimensions']['width']/2
      delta_y = metadata['dimensions']['height']/2
      corners_arr = [delta_x, delta_y, delta_x, -delta_y, -delta_x, -delta_y, -delta_x, delta_y]
      self.node_string += f'polygon = PoolVector2Array( {", ".join([str(el) for el in corners_arr])})\n'

  def get_ext_resources_string(self):
    return self.ext_resources_string

  def get_node_string(self):
    return self.node_string