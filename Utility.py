# region -------------Info------------
# Name: utility
# Version: 1.0
# By: Yaniv Sharon
# endregion -------------Info------------

# region -------------Imports---------

# endregion -------------Imports---------

# region -------------Methods-----------
def add_to_mark(file_text, add_text=''):
    splitted = file_text.split('<!oh hey mark>')
    return '%s%s%s' % (splitted[0], add_text, splitted[1])


def all_chars(text, char=' '):
    for i in xrange(len(text)):
        if text[i] != char:
            return False
    return True
# endregion -------------Methods-----------