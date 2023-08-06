import random
import re

from functools import reduce

# needs to be a raw string in order to avoid deprecation warnings
# https://stackoverflow.com/a/50504635
DICE_STRING_MATCHER = r'^(\d*)d(100|20|12|10|8|6|4|3|2)([-\+]?\d)*$'

MULTIPLIER_INDEX = 1
DIE_INDEX = 2
MODIFIER_INDEX = 3

DEFAULT_MULTIPLIER = 1
DEFAULT_MODIFIER = 0

FORMAT_HELP = "Format: <OPTIONAL multiplier>d<sides><OPTIONAL modifier>, i.e. d6, 2d6, 2d6+1, 1d6-1"

def roll(die_string, seed=None):
    # allows us to avoid randomness in tests, will be random as long as seed is
    # not set
    random.seed(seed)

    match = re.search(DICE_STRING_MATCHER, die_string)

    if not match:
        raise ValueError(f"Invalid die string. {FORMAT_HELP}")

    multiplier = int(match[MULTIPLIER_INDEX] or DEFAULT_MULTIPLIER)
    die = int(match[DIE_INDEX])
    modifier = int(match[MODIFIER_INDEX] or DEFAULT_MODIFIER)

    return reduce(
        lambda memo, value: memo + random.randrange(die), range(multiplier), 0
    ) + modifier