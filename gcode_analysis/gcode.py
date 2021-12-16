import re
from collections import namedtuple

TOKEN_REGEX = r'[EFGMSXYZ](-?0|[1-9][0-9]*)(\.[0-9]+)?'
TOKEN_COMPILED_REGEX = re.compile(TOKEN_REGEX)


token = namedtuple('token', ['type', 'value'])


def strip_gcode_comments(line: str):
    try:
        start_of_comment = line.index(';')
    except ValueError:
        start_of_comment = len(line)

    return line[0:start_of_comment]


def split_words(line: str):
    return line.split(sep=' ')


def parse_token(word):
    match = TOKEN_COMPILED_REGEX.fullmatch(word)

    if match:
        # Si noti che abbiamo bisogno di distinguere tra 'G21' e 'G21.0'
        value = float(word[1:])
        
        return token._make((word[0], value))
    else:
        raise ValueError('Invalid token')
