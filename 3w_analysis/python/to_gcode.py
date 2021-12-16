import XYZ3W
import argparse
import sys


def to_gcode (buffer):
    header, print_info, zero_padding, gcode = XYZ3W.decompose_3w_file(buffer)
    return XYZ3W.unpack_gcode(gcode)


parser = argparse.ArgumentParser(description = "Converts 3w file to gcode, dumps on stdout")
parser.add_argument('filename')
args = parser.parse_args()


with open(args.filename, 'rb') as f:
    buf = f.read()
    sys.stdout.buffer.write(to_gcode(buf))

