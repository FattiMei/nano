import unittest
import gcode

class TestGcodeParsing(unittest.TestCase):
    def test_strip_gcode_comments(self):
        test_comments = {
            'G21 ; set units to millimeters': 'G21 ',
            'G21;'                          : 'G21',
            '; print_time = 3600'           : ''
        }

        for input_value, output in test_comments.items():
            self.assertEqual(output, gcode.strip_gcode_comments(input_value))
