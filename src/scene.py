# scene.py
# defines an object to store, write .tscn files

import yaml
from math import radians

class Scene:

  # TODO: define dict mapping name(type) string -> type object
  TYPES = {}

  def __init__(self, level_name=None):
    # vars
    self.assets = []
    self.nodes = []
    self.last_asset = 0
    # populate initial lines
    self.header = '[gd_scene load_steps=1 format=2]'
    if level_name is None:
      level_name = 'level'
    self.nodes += '\n[node name="' + level_name + '" type="Node2D"]'

  # adds external assets, returning its id
  # warning: assumes asset_path is from the project root
  def add_asset(self, asset_path):
    asset_path = asset_path.replace('\\', '/')
    self.last_asset += 1
    self.assets += '\n[ext_resource path="res://' + asset_path + '" type="Texture" id=' + str(self.last_asset) + ']'
    return self.last_asset

  # adds a node, optionally linking an asset and metadata
  def add_node(self, name, node_type=None, asset_path=None, meta_path=None):
    node_text = '\n[node name="' + name + '" '
    # break out for specific node types
    if node_type is not None and node_type in self.TYPES:
      # TODO: define behavior for specific types
      pass
    else:
      # use sprites, if asset path exists
      if asset_path is None:
        node_text += 'type="Node2D" parent="."]'
      else:
        self.add_asset(asset_path)
        node_text += 'type="Sprite" parent="."]\n'
        node_text += 'texture=ExtResource( ' + str(self.last_asset) + ' )'
      # include positional metatdata, if it exists
      if meta_path is not None:
        with open(meta_path, 'r') as meta_file:
          metadata = yaml.safe_load(meta_file)
          if 'center' in metadata:
            node_text += '\nposition = Vector2( ' + str(metadata['center']['x']) + ', ' + str(metadata['center']['y']) + ' )'
          if 'rotation' in metadata:
            node_text += '\nrotation = ' + str(radians(metadata['rotation']))
      else:
        # don't center sprite (to preserve spatial relationships)
        node_text += '\ncentered = false'
    # add node text
    self.nodes += '\n' + node_text

  def write_scene(self, out_path):
    with open(out_path, 'w') as out_file:
      # write header
      out_file.writelines(self.header)
      out_file.write('\n')
      # write resources(assets)
      out_file.writelines(self.assets)
      out_file.write('\n')
      # write nodes
      out_file.writelines(self.nodes)

# test script
if __name__ == '__main__':
  test_scene = Scene()
  test_scene.add_node("empty_node")
  test_scene.add_node("sprite_node", asset_path="images/test/out/items/item_0.png")
  test_scene.add_node("sprite_with_meta", asset_path="images/test/out/items/item_1.png", meta_path="images/test/out/items/item_1.yaml")
  test_scene.write_scene('tmp.tscn')