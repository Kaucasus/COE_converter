# COE_converter

This is a very simple command line tool written in python that takes a jpg, png and bitmap picture and transforms it to a Xilinx .coe file for use in block memory.

NOTE: Currently creating a VGA map with an alpha layer produces the wrong values, so don't.

## Prerequisites


- [Have a python 3 environment](https://www.python.org/downloads/)
- [Have the python image library Pillow installed](https://python-pillow.org/)
- Have the coeconverter.py file included in this repo

## Usage

Run the script in your terminal of choice, it should be cross-platform. Only tested on Windows with Vivado 2019.2.

- HDMI is a RGB value with 8-bits for every colour
- VGA is a single 8-bit value consisting of 3 Red, 3 Green and 2 Blue.
- gray is a 8-bit grayscale image
- bit is a 8-bit value which is either full black or full white

Alpha is an 8 bit value that defines the transparency, standard it's on.

```bash
usage: coeconverter.py [-h] [-a] [-f] [-o OUTPUT] image {HDMI,VGA,gray,bit}

positional arguments:
  image                 give the image to convert
  {HDMI,VGA,gray,bit}   give the mode to convert to, default is HDMI

optional arguments:
  -h, --help            show this help message and exit
  -a, --alpha           disables 8 bit alpha output for COE
  -f, --force           overwrite the file if a same .coe file already exists
  -o OUTPUT, --output OUTPUT
                        Name of the output file to write
```
