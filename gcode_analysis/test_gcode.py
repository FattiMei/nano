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


    def test_parse_token(self):
        self.assertEqual(gcode.token('G', 20), gcode.parse_token('G20'))
        self.assertEqual(gcode.token('G', 20), gcode.parse_token('G20.0'))
        self.assertEqual(gcode.token('M', 116), gcode.parse_token('M116'))


    def test_line_decomposition(self):
        line = 'G1   F600   X7.505   Y20.735 E0.02941   '
        token_list = [
                        gcode.token('G', 1),
                        gcode.token('F', 600),
                        gcode.token('X', 7.505),
                        gcode.token('Y', 20.735),
                        gcode.token('E', 0.02941)
                     ]

        result = [gcode.parse_token(word) for word in gcode.split_words(gcode.strip_gcode_comments(line)) if word != '']
        self.assertEqual(token_list, result)
