import XYZ3W
import binascii
import argparse


def to_gcode (buffer):
    header, print_info, zero_padding, gcode = XYZ3W.decompose_3w_file (buffer)
    return XYZ3W.unpack_gcode (gcode)


parser = argparse.ArgumentParser (description = "Converts 3w files")
parser.add_argument ('input_filename')
parser.add_argument ('-o', default = 'out.gcode')

args = parser.parse_args ()

with open (args.input_filename, 'rb') as f:
    buffer = f.read ()

    with open (args.o, 'wb') as f2:
        f2.write (to_gcode (buffer))

