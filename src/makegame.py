# makegame.py
# constructs godot node tree from image layers

import argparse
from deconstruct import deconstruct
from scene import Scene
from subdivide import subdivide
from shutil import copyfile, rmtree
import os
from tqdm import tqdm

total_assets = 0

# copies a single file to the output directory, safely
def copy_file(out_dir, asset_path, new_name=None, subfolder=None):
  if not os.path.isdir(out_dir):
    print("Output directory " + out_dir + " does not exist. Exiting...")
    exit(1)

  # confirm/create images directory
  img_dir = os.path.join(out_dir, 'images')
  if not os.path.isdir(img_dir):
    os.mkdir(img_dir)

  # copy asset
  img_name = None
  if new_name is None:
    img_name = os.path.basename(asset_path)
  else:
    img_name = new_name
  
  img_path = None
  if subfolder is None:
    img_path = os.path.join(img_dir, img_name)
  else:
    sub_path = os.path.join(img_dir, subfolder)
    if not os.path.isdir(sub_path):
      os.mkdir(sub_path)
    img_path = os.path.join(sub_path, img_name)
  
  copyfile(asset_path, img_path)
  return img_path

def add_asset(scene, asset_path, out_dir, asset_type=None, meta_path=None):
  global total_assets
  # copy asset to out_dir; all names are safe
  asset_basename = f'asset_{total_assets}'
  new_asset_path = copy_file(out_dir, asset_path, asset_basename + '.png', asset_type)
  # add a node to the scene (including metadata)
  # added with out_dir as root
  scene.add_type(asset_basename, asset_type, os.path.relpath(new_asset_path, out_dir), asset_path, meta_path)
  total_assets += 1

def create_level(pass_files, dec_files, out_dir, out_file, verbose_output):
  scene = Scene()

  # handle passthrough files
  t = tqdm(pass_files, desc='Passthrough:')
  for pass_file in t:
    t.set_description('Passthrough: ' + pass_file)
    t.refresh()
    if os.path.isfile(pass_file):
      asset_type = os.path.splitext(os.path.basename(pass_file))[0]
      add_asset(scene, pass_file, out_dir, asset_type)
    elif os.path.isdir(pass_file):
      dir_contents = [f for f in os.listdir(pass_file) if f.endswith('.png')]
      for f in dir_contents:
        asset_type = os.path.splitext(os.path.basename(f))
        add_asset(scene, f, out_dir, asset_type)
  
  # handle deconstruct files
  # create temp dir if not exists
  tmp_path = os.path.join(out_dir, 'tmp')
  if not os.path.isdir(tmp_path):
    os.mkdir(tmp_path)
  t = tqdm(dec_files, desc='Deconstructing:')
  for dec_file in t:
    t.set_description('Deconstructing: ' + dec_file)
    t.refresh()
    # use given name as "type;" make folder for it
    asset_type = os.path.splitext(os.path.basename(dec_file))[0]
    tmp_path_ext = os.path.join(tmp_path, asset_type)
    if not os.path.isdir(tmp_path_ext):
      os.mkdir(tmp_path_ext)
    if os.path.isfile(dec_file):
      # handle single image files
      subdivide(dec_file, tmp_path_ext)
      res_files = [f for f in os.listdir(tmp_path_ext)]
      for i in range(len(res_files)):
        if i % 2 == 0:
          add_asset(scene, os.path.join(tmp_path_ext, res_files[i]), out_dir, asset_type, os.path.join(tmp_path_ext, res_files[i+1]))
    elif os.path.isdir(dec_file):
      # handle directories of image files
      deconstruct(dec_file, os.path.join(tmp_path, asset_type))
      res_dirs = [f for f in os.listdir(tmp_path_ext)]
      for d in res_dirs:
        d_path = os.path.join(tmp_path_ext, d)
        res_files = [f for f in os.listdir(d_path)]
        for i in range(len(res_files)):
          if i % 2 == 0:
            add_asset(scene, os.path.join(d_path, res_files[i]), out_dir, asset_type, os.path.join(d_path, res_files[i+1]))
  
  # write scene file
  scene.write_scene(os.path.join(out_dir, out_file))
  # clean up (delete /tmp)
  rmtree(tmp_path)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Constructs a godot node tree (scene file) from image layers')
  parser.add_argument('-p', '--passthrough',
                      metavar='<passthrough path>',
                      type=str,
                      nargs='*',
                      help='file(s) or director(y|ies) containing files to be passed through')
  parser.add_argument('-d', '--deconstruct',
                      metavar='<deconstruct path>',
                      type=str,
                      nargs='*',
                      help='file(s) or director(y|ies) containing files to be deconstructed')
  parser.add_argument('-n', '--name',
                      metavar='<level name>',
                      type=str,
                      default='level.tscn',
                      help='name of output level file')
  parser.add_argument('-o', '--output',
                      metavar='<output file>',
                      type=str,
                      help='directory for map file and requesite assets')
  parser.add_argument('-v', '--verbose',
                      default=False,
                      action='store_true',
                      help='do verbose output logging')
  args = parser.parse_args()
  create_level(args.passthrough, args.deconstruct, args.output, args.name, args.verbose)