import os
import sys
from math import ceil, log2

from PIL import Image
from PIL.Image import new

for fp in sys.argv[1:]:
    infile, extension = os.path.splitext(fp)
    if extension not in [".png", ".jpg", ".jpeg", ".bmp"]:
        print("Cannot convert: ", fp, " Use a png, jpg or bmp, not ", extension)
        sys.exit(0)
    im = Image.open(fp)
    mode = im.mode
    if mode != 'RGBA':
        print("Image not in RGBA, converting to RGBA.")
        im = im.convert("RGBA")
    memwidth = 32
    width, height = im.size
    print('Parsing:')

    # Parse every pixel
    MEMORY_INITIALIZATION_RADIX = 16
    MEMORY_INITIALIZATION_VECTOR = ''

    for y in range(height):
        MEMORY_INITIALIZATION_VECTOR += '\n'
        for x in range(width):
            rgba = im.getpixel((x, y))
            MEMORY_INITIALIZATION_VECTOR += ''.join(
                '{:02X}'.format(a) for a in rgba) + ' '

    print('Parsing successful')

    # Write to object file
    coename = (infile+'.coe')
    coe = open(coename, 'w')
    coe.write(';This is a .COE file generated via the convertor.py tool.\n' +
              ';Each value is a RGBA 32-bit in hex. \n' + ';\n' +
              ';This is a file of width: ' + str(width) + ' and height: ' + str(height) +
              '\n;So the memory has a width='+str(memwidth)+', and depth='+str(width*height) +
              '\n;(So that means the addra is ' + str(ceil(log2(width*height)))+' if minimum area 8kx2 is used)\n\n' +
              'memory_initialization_radix='+str(MEMORY_INITIALIZATION_RADIX)+'; This means the file is in HEX.\n' +
              'memory_initialization_vector='+MEMORY_INITIALIZATION_VECTOR+';'
              )

    print('File writing succesful! Exiting')
