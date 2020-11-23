# drawing-games

The goal of this project is to create game levels using only drawings as an
input. Input images are layers from a drawn level, each layer corresponding
to a specific "kind" of asset. Using these layers, individual assets are cropped
into their own files, and a level file is created for 
[Godot](https://godotengine.org/). By using this workflow, drawn assets can be
loaded as predetermined types, like physics objects, items, or characters.

## Dependencies

- [numpy](https://numpy.org/)
- [OpenCV](https://opencv.org/)
- [TQDM](https://github.com/tqdm/tqdm)

## Files

Each file has a command line interface, with help text. Use 
`python3 <filename> -h` for usage.

### subdivide.py
This script is the "brain" of the operation. It takes a single source `.png`
image, and splits it into individual asset files (`.png` and a metadata `.yaml`)
based on whether drawn items are isolated in the image.

### deconstruct.py
This is an extension on `subdivide.py`; it can take an input directory of `.png`
images, and subdivide each one. Each image is output in its own folder.

### scene.py
This script defines a _scene_ class, which keeps track of the `.tscn` format.
Individual assets are loaded using an instance of this object.

### makegame.py
This script combines all the capability of the preceding files into a single
command line interface. It can take individual image files or directories of
image files, and outputs a complete `.tscn` file, alongside a single `images`
directory containing assets. When loaded into Godot, the `.tscn` file ought to
look the same as the input image.