#!/usr/bin/env python2
import random
import re
import sys

SCRIPT_NAME = "wordcolor"
SCRIPT_AUTHOR = "rkben"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "0BSD"
SCRIPT_DESC = "Automagically visualize keywords with associated colors. "\
    "https://en.wikipedia.org/wiki/Color_psychology#General_model"

MODE="INPUT"

COLOR = {"white": "00", "black": "01", "blue": "02",
          "green": "03", "red": "04", "brown": "05",
          "purple": "06", "orange": "07", "yellow": "08",
          "light_green": "09", "cyan": "10",
          "light_cyan": "11", "light_blue": "12",
          "pink": "13", "grey": "14", "light_grey": "15"}

REE = sys.version_info[0]
if REE == 2:
    import ConfigParser
    CONF = ConfigParser.ConfigParser()
else:
    import configparser
    CONF = configparser.ConfigParser()

def gross():
    # wonder if this closes, probably
    if REE == 2:
        # this is probably wherever you started weechat
        return CONF.readfp(open("words.cfg"))
    else:
        return CONF.read_file(open("words.cfg"))

def colorize(line):
    gross()
    for keyword,value in CONF.items("words"):
        matches = re.findall(keyword, line, re.IGNORECASE)
        # TODO nested loops are gross
        for word in matches:
            pat = re.search(keyword, word, re.IGNORECASE)
            if pat:
                origword = pat.group(0)
                # TODO replace int values with COLOR["str"]
                line = line.replace(
                    origword,
                    "\x03{}{}{}".format(value,origword,"\x0399")
                )
    return line

def updatelist(url=None):
    # TODO append to, replace, overwrite, whatever words.cfg
    # with a remote url
    pass

def updateindi(word=None, color=None):
    # TODO append to, replace, overwrite, whatever words.cfg
    # with individual entries, ie. blood=red
    pass

def command_input_text_for_buffer(data, modifier, modifier_data, input):
    return colorize(input)

def command_run_input(data, buffer, command):
    if command == "/input return":
        input = weechat.buffer_get_string(buffer, "input")
        if input.startswith("/set "):
            return weechat.WEECHAT_RC_OK
        input = colorize(input)
        weechat.buffer_set(buffer, "input", input)
    return weechat.WEECHAT_RC_OK

try:
    import weechat
except ImportError:
    import sys
    cc ={
        "00": "\033[97m", # white
        "01": "\033[30m", # black
        "02": "\033[34m", # blue
        "03": "\033[32m", # green
        "04": "\033[91m", # red -> light red
        "05": "\033[31m", # brown -> red
        "06": "\033[35m", # purple
        "07": "\033[33m", # orange -> yellow
        "08": "\033[93m", # yellow -> light yellow
        "09": "\033[92m", # light green
        "10": "\033[36m", # cyan
        "11": "\033[96m", # light cyan
        "12": "\033[94m", # light blue
        "13": "\033[95m", # pink -> light magenta
        "14": "\033[90m", # grey -> dark grey
        "15": "\033[37m", # light gret
        "99": "\033[0m",  # reset
    }
    if len(sys.argv) > 1:
        input = " ".join(sys.argv[1:])
    else:
        input = "top kek Blue blue blue green red BROWN DANKdank blue BLUE red ORANGE"
        colorized = colorize(input)
    pat = re.findall("\\x03(\d{2})", colorized)
    for color in pat:
       colorized = colorized.replace(color, cc[color])
    print(colorized)

else:
   if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
      if MODE == 'MESSAGE':
         weechat.hook_modifier('input_text_for_buffer', 'command_input_text_for_buffer', '')
      else:
         weechat.hook_command_run('/input return', 'command_run_input', '')

