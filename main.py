import pyautogui 
import math
import sys
import re
from enum import Enum



# Represents a relative direction for patterns.
# HARD_LEFT represents a sharp left turn; Compass' is two HARD_LEFT, for example.
# The others work similarly.
class RelativeDir(Enum):
    HARD_LEFT = 2
    LEFT = 1
    STRAIGHT = 0
    RIGHT = -1
    HARD_RIGHT = -2

# Represents an absolute direction for patterns.
# The up and down variants are 60 degrees from horizontal, to fit with the hex grid.
class AbsoluteDir(Enum):
    RIGHT = 0
    UP_RIGHT = 1
    UP_LEFT = 2
    LEFT = 3
    DOWN_LEFT = 4
    DOWN_RIGHT = 5

# Converts a WASD code to a list of RelativeDir members.
# Input: A string using only a, q, w, e, and d. 
# Output: A list of RelativeDirs. Mapping:
#   a = hard left
#   q = left
#   w = straight
#   e = right
#   d = hard_right
def wasd_code_to_relative_dir_list(wasd_code):
    list = []
    for c in wasd_code:
        if c == 'a':
            list.append(RelativeDir.HARD_LEFT)
        elif c == 'q':
            list.append(RelativeDir.LEFT)
        elif c == 'w':
            list.append(RelativeDir.STRAIGHT)
        elif c == 'e':
            list.append(RelativeDir.RIGHT)
        elif c == 'd':
            list.append(RelativeDir.HARD_RIGHT)
    return list

# Hardcoded pattern constants. These are used for the read/append loop.
SCRIBES_REFLECTION = wasd_code_to_relative_dir_list('aqqqqq')
SCRIBES_GAMBIT = wasd_code_to_relative_dir_list('deeeee')
CONSIDERATION = wasd_code_to_relative_dir_list('qqqaw')
INTEGRATION_DISTILLATION = wasd_code_to_relative_dir_list('edqde')
VACANT_REFLECTION = wasd_code_to_relative_dir_list('qqaeaae')

# Constants for some other spells for testing reasons.
MINDS_REFLECTION = wasd_code_to_relative_dir_list('qaq')
COMPASS_PURIFICATION = wasd_code_to_relative_dir_list('aa')
ALIDADES_PURIFICATION = wasd_code_to_relative_dir_list('wa')
ARCHERS_DISTILLATION = wasd_code_to_relative_dir_list('wqaawdd')

# The Raycast Mantra!
RAYCAST_MANTRA = [MINDS_REFLECTION, COMPASS_PURIFICATION, MINDS_REFLECTION, ALIDADES_PURIFICATION, ARCHERS_DISTILLATION]

# Rotate an absolute direction (0-5, with 0 being right and rotating left 60 degrees from there) by a relative direction.
def rotate_dir(direction, relative_direction):
    return (direction + relative_direction.value) % 6

# Draw a pattern from the current location. Always starts with a rightwards move.
# Inputs:
#   move_amt: The absolute amount to move; this is the amount between dots in the hex grid.
#   relative_directions: A list of RelativeDir enum data; this defines the pattern to draw.
# Outputs:
#   The given pattern is drawn on the screen (if you have the staff open, anyway).
def draw_pattern(move_amt, relative_directions):
    # Initial direction; 0 = right.
    direction = 0

    # Hold mouse down, and only release when pattern drawing is finished.
    pyautogui.mouseDown()

    # Move right to start.
    move_space(move_amt, direction)

    # For each relative direction, turn that way and then drag.
    for rel_dir in relative_directions:
        direction = rotate_dir(direction, rel_dir)
        move_space(move_amt, direction)
        
    # Pattern drawing is done, so release the mouse.
    pyautogui.mouseUp()

# Read the default settings from file.
# Inputs:
#   Expects a file named default_settings in the working directory.
#   The first line is the X offset of the top-left dot from the top-left of the screen.
#   The second line is the Y offset of the top-left dot from the top-left of the screen.
#   The third line is the distance between the top-left dot and the one immediately to the right.
#   All of these values are in pixels.
# Outputs:
#   The preceding three values, as integers; it returns the distance between dots first, then the x offset, then the y offset.
def init_defaults():
    x_offset = 0
    y_offset = 0
    move_amt = 0
    with open("default_settings", "r") as file:
        x_offset = int(file.readline())
        y_offset = int(file.readline())
        move_amt = int(file.readline())

    pyautogui.moveTo(x_offset, y_offset, duration=0)

    return move_amt, x_offset, y_offset

# directions:
# 0 right
# 1 upright
# 2 upleft
# 3 left
# 4 downleft
# 5 downright
def move_space(move_amt, direction):
    # apply rotation matrix to direction
    # [move_amt, 0]^T
    # x = x*cos(th) - x*sin(th)
    # y = y*sin(th) + y*cos(th)
    angle = (math.pi/3) * direction
    x = (math.cos(angle)*move_amt)
    y = (-math.sin(angle)*move_amt)

    pyautogui.move(x, y)


def append_pattern(move_amt, top_left_x, top_left_y, pattern):
    pyautogui.moveTo(top_left_x, top_left_y, duration=0)
    move_space(move_amt, 5)

    # scribe's reflection
    draw_pattern(move_amt, SCRIBES_REFLECTION)
    
    # consideration
    move_space(move_amt, 0)
    draw_pattern(move_amt, CONSIDERATION)

    # user pattern
    # set to center of screen ish
    pyautogui.moveTo(top_left_x, top_left_y, duration=0)
    move_space(move_amt * 6, 0)
    move_space(move_amt * 5, 5)

    # draw pattern
    draw_pattern(move_amt, pattern)
    
    # integration distillation
    pyautogui.moveTo(top_left_x, top_left_y, duration=0)
    move_space(move_amt * 3, 5)
    draw_pattern(move_amt, INTEGRATION_DISTILLATION)

    # scribe's gambit
    move_space(move_amt * 3, 5)
    draw_pattern(move_amt, SCRIBES_GAMBIT)


def start_new_pattern_list(move_amt, top_left_x, top_left_y):
    move_space(move_amt * 2, 5)
    draw_pattern(move_amt, VACANT_REFLECTION)

    move_space(move_amt * 2, 0)
    draw_pattern(move_amt, SCRIBES_GAMBIT)
    

def append_pattern_list(move_amt, top_left_x, top_left_y, pattern_list):
    for pattern in pattern_list:
        append_pattern(move_amt, top_left_x, top_left_y, pattern)
        pyautogui.rightClick()


def write_spell(move_amt, top_left_x, top_left_y, pattern_list):
    start_new_pattern_list(move_amt, top_left_x, top_left_y)
    pyautogui.rightClick()
    append_pattern_list(move_amt, top_left_x, top_left_y, pattern_list)

# Dictionary showing conversions between NBT data angle notation and the QAQ notation used elsewhere in-game,
# (and in this program)
# (casefolded to reduce issues)
NBT_to_QAQ_DICT = {
    "0b": "w",
    "1b": "e",
    "2b": "d",
    "3b": "s", # This one is actually never used anywhere :P
    "4b": "a",
    "5b": "q"
}
def extract_pattern(block_data: str):
    """
    Extracts patterns from NBT data
    :param block_data: intended to be data obtained from hitting F3+I on a spell slate (or similar), but should accept
    anything with the same notation
    :return: a tuple with a list of angles in the first index and a start direction in the second, both in qaq notation
    """
    # Regex development/examples:
    # https://regex101.com/r/1nR9sU/5
    extract_angles_regex = re.compile(r"angles:\s*\[B;((?:\s*[0-5][Bb]\s*,?\s*)+)")
    # https://regex101.com/r/IPtUBz/3
    extract_start_regex = re.compile(r"start_dir:\s*(.{2})}")
    # Search Blockdata for patterns and get the first match:
    try:
        angle_list = re.search(extract_angles_regex, block_data).group(1).split(",")
        start_dir = re.search(extract_start_regex, block_data).group(1)
    except AttributeError:  # Convert AttributeError to something more descriptive
        raise ValueError("No Patterns Found")
    # Convert to qaq
    angle_list = [NBT_to_QAQ_DICT[angle.strip().casefold()] for angle in angle_list]
    start_dir = NBT_to_QAQ_DICT[start_dir.strip().casefold()]

    return angle_list, start_dir


def split_file(hex_file:str): # str(filepath) -> list[str(iotaname)]
    """
    Reads a .hex file and splits it into a list of spells the program can iterate over, discarding comments
    (Currently just ignores function calls)
    :param hex_file: filepath to the spell list
    :return: a python list of Iota names for further parsing downstream
    TODO: Add handling for function definitions
    """
    # Read File into a string
    with open(hex_file, 'r') as file:
        spell_file = file.read()

    # Purge Comments
    # https://regex101.com/r/tvLXdO/1
    comment_regex = re.compile(r"//(.*)\n")
    spell_file = re.sub(comment_regex, "\n", spell_file)

    # Replace Parens with Iotas
    spell_file = re.sub(r"{","Introspection", spell_file)
    spell_file = re.sub(r"}","Retrospection", spell_file)

    # Split into Iota names
    # https://regex101.com/r/x4lg1D/3
    iota_regex = re.compile(r"^\s*\b(.*)\s*$")
    iota_list = [clean_iota(match.group(1)) for match in re.finditer(iota_regex, spell_file)]

    return iota_list

def clean_iota(iota:str): # str(iotaname) -> str(iotaname)
    """
    Helper function that removes formatting from Iota names to allow for punctuation and case insensitivity
    :param iota: Name of an Iota (ie: r"Augur's Exaltation  ")
    :return: That same iota but standardized (ie: r"augursexaltation")
    """
    # Standard string cleaning
    iota = iota.strip().casefold()
    # Clear punctuation
    # Currently removes spaces, underscores, and apostrophes
    iota = re.sub(r"['_ ]", "", iota)
    return iota


# Prints the help message.
# Inputs: None
# Outputs: A description of all usable commands.
def print_help():
    print("To run:")
    print("main.py help")
    print("\t Prints this menu")
    
    print("")
    print("main.py get_code '[input]'")
    print("\t Reads the WASD code for a pattern.")
    print("\t Write the pattern to a scroll or slate, place the scroll/slate/GreatScroll on a wall, use f3+i to copy the data, and pass it, quoted, as the [input] argument. (Single quotes ' are recommended, as Minecraft uses double quotes \" within NBT strings.)")
    
    print("")
    print("main.py write_spell [filename]")
    print("\t TODO NOT IMPLEMENTED YET THIS JUST DOES RAYCAST")
    print("\t Reads a file and writes the spell contained within.")
    print("\t Comments using // or # are ignored.")
    print("\t Numbers and Bookkeeper's Gambit are currently not supported.")

    print("")
    print("There must be a file called default_settings in the working directory, with the following structure:")
    print("[x_offset]")
    print("[y_offset]")
    print("[dist_between_dots]")
    print("")
    print("All values are in pixels.")
    return 0

if __name__ == "__main__":
    # parse arguments
    args = sys.argv
    # If no args or some helpy request, print help message.
    if len(args) == 1 or args[1] == '-h' or args[1] == '--help' or args[1] == 'help':
        print_help()
    elif args[1] == 'get_code':
        print("".join(extract_pattern(args[2])[0]))
    elif args[1] == 'write_spell':
        # TODO
        pyautogui.PAUSE = 0.033
        move_amt, top_left_x, top_left_y = init_defaults()
        write_spell(move_amt, top_left_x, top_left_y, RAYCAST_MANTRA)
    elif args[1] == 'test_default_settings':
        TODO
