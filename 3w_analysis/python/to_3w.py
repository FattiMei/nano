import XYZ3W
import binascii
import argparse

def to_3w (buffer):
    return XYZ3W.create_3w_file (buffer)


parser = argparse.ArgumentParser (description = "Converts gcode in 3w files")
parser.add_argument ('input_filename')
parser.add_argument ('-o', default = 'out.3w')

args = parser.parse_args ()

with open (args.input_filename, 'rb') as f:
    buffer = f.read ()

    with open (args.o, 'wb') as f2:
        f2.write (to_3w (buffer))
