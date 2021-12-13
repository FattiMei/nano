import binascii
import struct
import re
from collections import namedtuple


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# Costanti per la versione 5 del formato 3w
SIGNATURE = b'3DPFNKG13WTW'
ID = 1
VERSION = 5
ZIPTAG_OFFSET = 8
ZIPTAG_CODE = b'TagEJ256'
INFO_OFFSET = 68
ID2 = 1


# Offset e lunghezza dei blocchi
HEADER_LEN = 112
GCODE_OFFSET = 0x2000


# Parametri di default per la mia macchina
DEFAULT_PARAMETERS = {
        'filename': '.3w',
        'machine': 'dv1NW0A000',
        'filament': '50, 50'

}


END_STRING = b';END'
NEWLINE = b'\r\n'


# Layout in memoria per la struttura header
FORMAT_STRING = '!12sbb2xI8x8sIIII60x'
HEADER_STRUCT = struct.Struct(FORMAT_STRING)


# Chiave crittografica
KEY = b'@xyzprinting.com@xyzprinting.com'
CIPHER = AES.new(KEY, AES.MODE_ECB)


# struttura dati per gestire un file 3w, è una tuple di byte objects
xyz_file = namedtuple('xyz_file', ['header', 'print_info', 'zero_padding', 'gcode'])


def ZERO_PADDING_LEN(print_info_len: int):
    return GCODE_OFFSET - HEADER_LEN - print_info_len


# funzioni per generare i blocchi del formato 3w
def pack_header(print_info_len: int, crc32: int):
    return HEADER_STRUCT.pack(SIGNATURE,
                              ID,
                              VERSION,
                              ZIPTAG_OFFSET,
                              ZIPTAG_CODE,
                              print_info_len,
                              INFO_OFFSET,
                              ID2,
                              crc32)


def pack_print_info(print_info_len: int):
    # è irrilevante con quale carattere si riempie la struttura
    # basta che non sia NULL
    return b'M' * print_info_len


def pack_zero_padding(print_info_len: int):
    return bytes(ZERO_PADDING_LEN(print_info_len))


def pack_gcode(plain_gcode: bytes):
    # si assume che il gcode sia canonico (vedi specifica)
    padded_gcode = plain_gcode

    if len(plain_gcode) % 16 != 0:
        padded_gcode = pad(data_to_pad=plain_gcode,
                           block_size=16,
                           style='pkcs7')

    assert len(padded_gcode) % 16 == 0
    return CIPHER.encrypt(padded_gcode)


def decompose_3w_file(mem):
    try:
        first_zero_offset = mem.index(0, HEADER_LEN, GCODE_OFFSET)
    except ValueError:
        first_zero_offset = GCODE_OFFSET
    

    header          = mem[0:HEADER_LEN]
    print_info      = mem[HEADER_LEN:first_zero_offset]
    zero_padding    = mem[HEADER_LEN + len(print_info):GCODE_OFFSET]
    gcode           = mem[GCODE_OFFSET:]

    return xyz_file._make((header, print_info, zero_padding, gcode))


# Funzioni per validare i blocchi del formato 3w
def validate_header(mem):
    _, _, _, _, _, print_info_len, _, _, crc32 = HEADER_STRUCT.unpack(mem)
    return mem == pack_header(print_info_len, crc32)


def validate_print_info(mem, print_info_len):
    return len(mem) == print_info_len and mem.find(0) == -1


def validate_zero_padding(mem, print_info_len):
    return len(mem) == ZERO_PADDING_LEN(print_info_len) == mem.count(0)


def validate_gcode(mem, crc32):
    return crc32 == binascii.crc32(mem) and len(mem) % 16 == 0


def validate_3w_file(xyz_file):
    result = False

    if validate_header(xyz_file.header):
        print_info_len, crc32 = unpack_header(xyz_file.header)

        result = (validate_print_info   (xyz_file.print_info, print_info_len) and
                  validate_zero_padding (xyz_file.zero_padding, print_info_len) and
                  validate_gcode        (xyz_file.gcode, crc32))

    return result


# funzioni per estrarre informazioni dai blocchi del formato 3w
def unpack_header(mem):
    _, _, _, _, _, print_info_len, _, _, crc32 = HEADER_STRUCT.unpack(mem)
    return print_info_len, crc32


def unpack_gcode(mem):
    decrypted_gcode = CIPHER.decrypt(mem)

    if decrypted_gcode.endswith(END_STRING):
        result = decrypted_gcode
    else:
        result = unpad(padded_data=decrypted_gcode,
                       block_size=16,
                       style='pkcs7')

    return result


# funzioni per trasformare il gcode originario
def strip_gcode_comments(plain_gcode):
    without_comments = re.sub(b';.*', b'', plain_gcode, flags=re.MULTILINE)
    return re.sub(b'^\r?\n', b'', without_comments, flags=re.MULTILINE)


def pack_gcode_parameters(parameters):
    return NEWLINE.join([bytes(f'; {key} = {value}', encoding='utf-8') for key, value in parameters.items()])


# funzioni per la conversione tra i formati gcode e 3w
def convert_gcode_to_3w(plain_gcode, params=DEFAULT_PARAMETERS):
    PRINT_INFO_LEN = 32

    gcode_blocks = [pack_gcode_parameters(params),
                    strip_gcode_comments(plain_gcode),
                    END_STRING]

    encrypted_gcode = pack_gcode(NEWLINE.join(gcode_blocks))
    header          = pack_header(PRINT_INFO_LEN, binascii.crc32(encrypted_gcode))
    print_info      = pack_print_info(PRINT_INFO_LEN)
    zero_padding    = pack_zero_padding(PRINT_INFO_LEN)

    return xyz_file._make((header, print_info, zero_padding, encrypted_gcode))


def convert_3w_to_gcode(xyz_file):
    if validate_3w_file(xyz_file):
        plain_gcode = unpack_gcode(xyz_file.gcode)

        return plain_gcode
    else:
        raise ValueError('The file specified does not follow 3w specification')
