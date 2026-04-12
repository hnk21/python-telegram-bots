from utility.helper import *

# Format special characters that must be escaped with a preceding '\' for markdown syntax
def format_markdown(text):
    specials = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in specials:
        text = text.replace(c, '\\'+c)
    return text