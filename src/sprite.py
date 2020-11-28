from drawntype import DrawnType
from math import radians
import yaml

class Sprite(DrawnType):

  def __init__(self, name, res_image_path, parent='.', meta_path=None, start_ext_id=1, start_sub_id=1):
    super().__init__(name, start_ext_id, start_sub_id,'Sprite', parent)

    use_id = self._get_ext_id_safe()
    
    # add image external resources
    self.ext_resource_string = self._ext_resource_string(res_image_path, 'Texture', use_id)

    # create node, with metadata/parent if existent
    self.node_string = self._node_string(self.name, self.node_type, self.parent)
    self.node_string += f'texture = ExtResource( {use_id} )\n'
    if meta_path is not None:
      # load existent metadata
      with open(meta_path, 'r') as meta_file:
        metadata = yaml.safe_load(meta_file)
        if 'center' in metadata:
          self.node_string += f'position = Vector2( {metadata["center"]["x"]},{metadata["center"]["y"]} )\n'
        if 'rotation' in metadata:
          self.node_string += f'rotation = {radians(metadata["rotation"])}\n'
    else:
      # don't center sprite (to preserve spatial relationships)
      self.node_string += 'centered = false\n'

  def get_ext_resources_string(self):
    return self.ext_resource_string

  def get_node_string(self):
    return self.node_string + '\n'


if __name__ == '__main__':
  sprite = Sprite('test_name', 'images/test_sprite.png')
  
  # test basic sprite
  print(sprite.get_ext_resources_string() + '\n' + sprite.get_node_string())