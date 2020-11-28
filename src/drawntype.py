
# stores a "type", which defines a collection of godot nodes
# types ought to be self-contained, and construct all of their own:
    # external resources
    # sub-resources
class DrawnType:

  # initializes a type. all setup logic must be done in this step
  # end_(ext,sub)_id ought to accurately reflect the id's used
  def __init__(self, name, node_type='Node2D', parent='.', start_ext_id=1, start_sub_id=1):
    self.name = name
    self.node_type = node_type
    self.parent = parent
    self.end_ext_id=start_ext_id
    self.end_sub_id=start_sub_id

  # returns all external resources
  def get_ext_resources_string(self):
    return ''

  # returns all sub-resources
  def get_sub_resources_string(self):
    return ''

  # returns all nodes and their components
  def get_node_string(self):
    return self._node_string(self.name, self.node_type, self.parent) + '\n'


  # helper static methods

  @staticmethod
  def _node_string(name, node_type, parent):
    return f'[node name="{name}" type="{node_type}" parent="{parent}"]\n'

  @staticmethod
  def _ext_resource_string(path, ext_type, ext_id):
    return f'[ext_resource path="res://{path}" type="{ext_type}" id={ext_id}]\n'

  @staticmethod
  def _sub_resource_string(sub_type, sub_id):
    return f'[sub_resource type="{sub_type}" id={sub_id}]\n'
