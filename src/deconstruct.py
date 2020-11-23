# deconstruct.py
# given a folder of image layers, subdivides each layer into items
# creates a folder for each layer

import argparse
import os
import subdivide
from tqdm import tqdm

def deconstruct(in_dir, out_dir, verbose_output=False):
  # check directories
  if not os.path.isdir(in_dir):
    raise Exception('Input directory ' + in_dir + ' does not exist.')
  if not os.path.isdir(out_dir):
    raise Exception('Output directory ' + out_dir + ' does not exist.')
  
  # get input image files
  img_files = [f for f in os.listdir(in_dir) if f.endswith('.png')]

  # subdivide each image
  t = tqdm(img_files, desc='Subdividing:') #for nice output
  for img in t:
    # update description
    t.set_description('Subdividing: ' + img)
    t.refresh()

    name = os.path.splitext(img)[0]
    curr_out_dir = os.path.join(out_dir, name)
    if not os.path.isdir(curr_out_dir):
      os.mkdir(curr_out_dir)
    try:
      subdivide.subdivide(os.path.join(in_dir, img), curr_out_dir, verbose_output)
    except:
      if verbose_output:
        print('Failed to subdivide ' + img + '. Run "python subdivide.py -o' + os.path.join(in_dir, img) + curr_out_dir + '" for more verbose output.')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Deconstructs folders of images into their constituent items.')
  parser.add_argument('input_dir', metavar='<input directory>', type=str, help='directory containing input images')
  parser.add_argument('output_dir', metavar='<output directory>', type=str, help='destination directory for output')
  parser.add_argument('-v', '--verbose', default=False, action='store_true', help='do verbose output logging')
  args = parser.parse_args()
  deconstruct(args.input_dir, args.output_dir, args.verbose)