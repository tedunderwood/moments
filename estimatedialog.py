# estimatedialogue

import sys

def startsquote(word):
    if word.startswith('"'):
        return True
    elif word.startswith('“'):
        return True
    elif word.startswith("'"):
        return True
    elif word.startswith("‘"):
        return True
    else:
        return False

def endsquote(word):
    if word.endswith('"'):
        return True
    elif word.endswith('”'):
        return True
    elif word.endswith('’’'):
        return True
    elif word.endswith(".'"):
        return True
    elif word.endswith(",'"):
        return True
    elif word.endswith("!'"):
        return True
    elif word.endswith("’"):
        return True
    else:
        return False


def count_dialog(listoflines):
    '''
    Estimates lines of dialogue, and returns that figure
    along with a word count and count of quotation marks.
    '''

    indialog = False
    # this flag toggles on and off as we move

    totalwords = 0
    dialogwords = 0
    totalquotes = 0

    for line in listoflines:
        try:
            line = line.strip()
            words = line.split()
            numwords = len(words)
        except:
            print(line)
            sys.exit(0)

        for idx, word in enumerate(words):
            totalwords += 1

            if word == '"' or word == '”' or word == '“' or word == '’’':
                if not indialog or idx == 0:
                    indialog = True
                else:
                    indialog = False
                # Hitting a raw quotation mark simply
                # toggles our status. If it's the first
                # token in a line, it toggles ON.
                # nothing is incremented.

            elif idx == 0 and '"' in word:
                indialog = True
                dialogwords += 1
                # The first word in a line is strongly biased to toggle on.

            elif startsquote(word):
                indialog = True
                dialogwords += 1
                # Words that begin with a quotation mark, toggle on and increment.

            elif endsquote(word):
                indialog = False
                dialogwords += 1
                # words that end with a quotation mark, toggle off an increment.

            elif idx == numwords - 1 and '"' in word or word.endswith('’') or word.endswith("'"):
                indialog = False
                dialogwords += 1
                # Words that end a line are biased to toggle off.
            else:
                if indialog:
                    dialogwords += 1

            if "'" in word or '"' or '“' in word or '”' in word:
                totalquotes += 1

    return totalwords, dialogwords, totalquotes



