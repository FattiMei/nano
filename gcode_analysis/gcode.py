import re
from collections import namedtuple

TOKEN_REGEX = '[FGMSXYZ](0|-?[1-9][0-9]*)(.[0-9]+)?'
TOKEN_COMPILED_REGEX = re.compile(TOKEN_REGEX)


token = namedtuple('token', ['type', 'value'])


def strip_gcode_comments(line):
    try:
        start_of_comment = line.index(';')
    except ValueError:
        start_of_comment = len(line)

    return line[0:start_of_comment]


def parse_token(word):
    token_match = TOKEN_COMPILED_REGEX.match(word)

    if token_match:
        return token._make((word[0], float(word[1:])))
    else:
        raise ValueError('Invalid token')
