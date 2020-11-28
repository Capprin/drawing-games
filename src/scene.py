# scene.py
# defines an object to store, write .tscn files

from drawntype import DrawnType
from sprite import Sprite

class Scene:

  TYPES = []

  def __init__(self, level_name=None):
    # populate initial lines
    self.header = '[gd_scene load_steps=1 format=2]\n'
    if level_name is None:
      level_name = 'level'
    self.nodes = '[node name="' + level_name + '" type="Node2D"]\n\n'
    # vars
    self.ext_resources = ''
    self.sub_resources = ''
    self.curr_ext_resource_id = 1
    self.curr_sub_resource_id = 1

  # adds a drawn type, optionally linking an asset and metadata
  def add_type(self, name, drawn_type=None, asset_path=None, meta_path=None):
    # make asset path safe
    if asset_path is not None:
      asset_path = asset_path.replace('\\', '/')
    
    # TODO: try to figure out a way to make the current ID less influenced by drawn types
        # maybe have them hand back an increment, instead of an absolute position?
    add_type = DrawnType(name, start_ext_id=self.curr_ext_resource_id, start_sub_id=self.curr_sub_resource_id)
    # break out for specific node types
    if drawn_type is not None and drawn_type in self.TYPES:
      if drawn_type == 'sprite':
        add_type = Sprite(name, asset_path, meta_path=meta_path, start_ext_id=self.curr_ext_resource_id, start_sub_id=self.curr_sub_resource_id)
    elif asset_path is not None:
      # use sprites, if asset path exists
      add_type = Sprite(name, asset_path, meta_path=meta_path, start_ext_id=self.curr_ext_resource_id, start_sub_id=self.curr_sub_resource_id)
    
    # add node, external, sub content
    self.nodes += add_type.get_node_string()
    self.ext_resources += add_type.get_ext_resources_string()
    self.sub_resources += add_type.get_sub_resources_string()
    # update id's
    self.curr_ext_resource_id = add_type.get_last_ext_id()
    self.curr_sub_resource_id = add_type.get_last_sub_id()

  def write_scene(self, out_path):
    with open(out_path, 'w') as out_file:
      # write header
      out_file.write(self.header + '\n')
      out_file.write(self.ext_resources + '\n')
      out_file.write(self.sub_resources + '\n')
      out_file.writelines(self.nodes)

# test script
if __name__ == '__main__':
  test_scene = Scene()
  test_scene.add_type("empty_node")
  test_scene.add_type("sprite_node", asset_path="items/item_0.png")
  test_scene.add_type("sprite_node_2", asset_path="items/item_0.png")
  test_scene.write_scene('tmp.tscn')