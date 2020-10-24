from argparse import Namespace
import os
import sys
import argparse
from math import ceil, log2

from PIL import Image
from PIL.Image import new


def CalcMemwidth(mode, alpha):
    width = 0
    if mode == 'HDMI':
        width += 24
    elif mode == 'VGA':
        width += 8
    elif mode == 'gray':
        width += 8
    else:
        width += 8

    if alpha:
        width += 8

    return width


def CalcMemoryVector(image: Image, mode, alpha, height, width):
    MEMORY_INITIALIZATION_VECTOR = ''

    if mode == 'HDMI':
        if alpha:
            image = image.convert('RGBA')
        else:
            image = image.convert('RGB')
    elif mode == 'VGA':
        VGA332Palette = [(int(((i & 224) >> 5)*(255/7)), int(((i & 28) >> 2)
                                                             * (255/7)), int((i & 3)*(255/3))) for i in range(256)]
        if alpha:
            image = image.convert('PA', palette=VGA332Palette)
            #Currently this produces a wrong output, so fail the program
            print("Creating a VGA map with alpha creates a wrong value, stopping the program.")
            sys.exit()
        else:
            image = image.convert('P', palette=VGA332Palette)
    elif mode == 'gray':
        if alpha:
            image = image.convert('LA')
        else:
            image = image.convert('L')
    else:
        image = image.convert('1')

    if isinstance(image.getpixel((0, 0)), int):
        for y in range(height):
            MEMORY_INITIALIZATION_VECTOR += '\n'
            for x in range(width):
                pixel = image.getpixel((x, y))
                MEMORY_INITIALIZATION_VECTOR += ''.join(
                    '{:02X}'.format(pixel)) + ' '
    else:
        for y in range(height):
            MEMORY_INITIALIZATION_VECTOR += '\n'
            for x in range(width):
                pixel = image.getpixel((x, y))
                MEMORY_INITIALIZATION_VECTOR += ''.join(
                    '{:02X}'.format(a) for a in pixel) + ' '

    return MEMORY_INITIALIZATION_VECTOR


parser = argparse.ArgumentParser()
# Set up parser arguments
parser.add_argument("image", help="give the image to convert")
parser.add_argument("mode", help="give the mode to convert to, default is HDMI", choices=[
                    'HDMI', 'VGA', 'gray', 'bit'], default='HDMI')
parser.add_argument(
    "-a", "--alpha", help="disables 8 bit alpha output for COE", action="store_false")
parser.add_argument(
    '-f', '--force', help="overwrite the file if a same .coe file already exists", action="store_true")
parser.add_argument("-o", "--output", help="Name of the output file to write")

# Get arguments used
args = parser.parse_args()

fp = args.image

infile, extension = os.path.splitext(fp)
if extension not in [".png", ".jpg", ".jpeg", ".bmp"]:
    print("Cannot convert: ", fp, " Use a png, jpg or bmp, not ", extension)
    sys.exit(0)

if args.output:
    filename = args.output
else:
    filename = infile

print('Making  {}.coe in mode: {}, and with{} alpha'.format(
    filename, args.mode, "" if args.alpha else "out"))

im = Image.open(fp)

memwidth = CalcMemwidth(args.mode, args.alpha)
width, height = im.size
print('Parsing:')

# Parse every pixel
MEMORY_INITIALIZATION_RADIX = 16
MEMORY_INITIALIZATION_VECTOR = CalcMemoryVector(
    im, args.mode, args.alpha, height, width)


print('Parsing successful')
# Create contents
contents = (';This is a .COE file generated via the convertor.py tool.\n' +
            (" with alpha " if args.alpha else " without alpha ") +
            ';Each value is a '+args.mode + str(memwidth)+'-bit in hex. \n' + ';\n' +
            ';This is a file of width: ' + str(width) + ' and height: ' + str(height) +
            '\n;So the memory has a width='+str(memwidth)+', and depth='+str(width*height) +
            '\n;(So that means the addra is ' + str(ceil(log2(width*height)))+' if minimum area 8kx2 is used)\n\n' +
            'memory_initialization_radix='+str(MEMORY_INITIALIZATION_RADIX)+'; This means the file is in HEX.\n' +
            'memory_initialization_vector='+MEMORY_INITIALIZATION_VECTOR+';\n')

# Write to object file
coename = (infile+'.coe')
if args.force:
    try:
        coe = open(coename, 'w')
    except IOError as e:
        print("Failed to make coe file. Error: {}".format(e))
else:
    try:
        coe = open(coename, 'x')
    except IOError as e:
        print("Failed to make coe file. Does the file already exist? If you want to overwrite this use -f\nError: {}".format(e))

try:
    coe.write(contents)
except IOError as e:
    print("Failed to write file. Error: {}".format(e))
    sys.exit()

print('File writing succesful! Exiting')
