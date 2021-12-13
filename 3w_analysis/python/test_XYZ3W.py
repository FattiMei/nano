import unittest
import XYZ3W


FILEPATH_3W = "../../3w_files/bistable_mechanism.3w"
FILEPATH_GCODE = "../../cura_files/bistable_mechanism.gcode"


class TestFileValidation(unittest.TestCase):
    def setUp(self):
        with open(FILEPATH_3W, "rb") as file:
            self.mem = file.read()

            # Questa è l'unica operazione che non testo
            self.blocks = XYZ3W.decompose_3w_file(self.mem)
            self.print_info_len = len(self.blocks.print_info)


    def test_header_packing(self):
        self.assertEqual(self.blocks.header, XYZ3W.pack_header(0x000006c2, 0x8fb3ab15))


    def test_header_unpacking(self):
        print_info_len, crc32 = XYZ3W.unpack_header(self.blocks.header)

        self.assertEqual(print_info_len, 0x000006c2)
        self.assertEqual(crc32, 0x8fb3ab15)


    def test_header_validation(self):
        self.assertTrue(XYZ3W.validate_header(self.blocks.header))


    def test_print_info_validation(self):
        self.assertTrue(XYZ3W.validate_print_info(self.blocks.print_info,
            self.print_info_len))


    def test_zero_padding_validation(self):
        self.assertTrue(XYZ3W.validate_zero_padding(self.blocks.zero_padding,
            self.print_info_len))


    def test_gcode_validation(self):
        _, crc32 = XYZ3W.unpack_header(self.blocks.header)
        self.assertTrue(XYZ3W.validate_gcode(self.blocks.gcode, crc32))


    def test_file_validation(self):
        self.assertTrue(XYZ3W.validate_3w_file(self.blocks))
