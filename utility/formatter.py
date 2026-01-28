from utility.variables import *

# Format special characters that must be escaped with a preceding '\
def format_markdown(text):
    # '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
    specials = ['_', '*', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in specials:
        text = text.replace(c, '\\'+c)
    return text