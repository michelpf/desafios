import traceback

def truncate_clean(text, init, max_char_line_m, text_justified, max_char_line, justification=False):
    '''
    Function to truncate a given text when the boundary end is a space character.
    :param str text:
        Text value.
    :param str init:
        Init index, position to start the analysis.
    :param int max_char_line_m:
        Maximum chars per line aggregated.
    :param int text_justified:
        Text justified.
    :param int max_char_line:
        Maximum char per line.
    :param bool justification:
        If true, returns a text justified exactly to the max char per line filling between
        words with space character. This is optional.
    :return: max_char_line_m, size, text_justified to be reused.
    '''

    space_index = text[init:max_char_line_m].rfind(' ') + init

    if text[init:init + 1] == ' ':
        space_index += 1

    line_justified = text[init:space_index].strip()

    if justification:
        line_justified = justify_spaces(line_justified, max_char_line)

    text_justified += line_justified + '\n'
    init = space_index
    max_char_line_m = init + max_char_line

    return max_char_line_m, init, text_justified

def justify_spaces(text, max_char):
    '''
    Function to justificate a given text with spaces between words
    :param str text:
        Text value.
    :param int max_char:
        Maximum chars.
    :return: text justified
    '''

    if len(text) == max_char:
        return text
    else:
        spaces = max_char - len(text)
        words = text.split(' ')
        spaces += len(words) - 1
        space_count, space_rest = divmod(spaces, len(words) - 1)
        text_justified = ''
        index = 0
        while spaces > 0:
            for idx, word in enumerate(words):
                if spaces > 0 and idx < len(words):
                    if idx == 0:
                        text_justified += word + (' ' * (space_count + space_rest))
                        spaces -= space_count + space_rest
                    else:
                        text_justified += word + (' ' * space_count)
                        spaces -= space_count
                else:
                    text_justified += word + ' '

        return text_justified.strip()


def truncate(text, max_char_line, justification=False):

    '''
    Function to justificate a given text with spaces between words
    :param str text:
        Text value.
    :param int max_char_line:
        Maximum chars per line.
    :param bool justification:
        If true, returns a text justified exactly to the max char per line filling between
        words with space character. This is optional.
    :return: text justified
    '''

    if max_char_line <= 15:
        raise Exception("The mininum value was exceeded. Check your max value provided.")

    text_justified = ''
    lines = text.split('\n')
    for line in lines:
        max_char_line_m = max_char_line
        init = 0
        while init < len(line):
            if max_char_line_m == (len(line) - 1) or line[max_char_line_m] == ' ' or line[max_char_line_m] == '.' or line[max_char_line_m] == ',':

                if len(line) > (max_char_line_m + 2) and line[init:max_char_line_m + 2].find('."') > 0:
                    max_char_line_m, init, text_justified = \
                        truncate_clean(line, init, max_char_line_m, text_justified, max_char_line, justification)
                    continue

                if line[init:init + 1] == ' ':
                    max_char_line_m += 1

                line_justified = line[init:max_char_line_m].strip()

                if justification:
                    line_justified = justify_spaces(line_justified, max_char_line)

                text_justified += line_justified + '\n'

                init += max_char_line
                max_char_line_m += max_char_line

                if max_char_line_m >= len(line):
                    max_char_line_m = len(line) - 1
            else:
                max_char_line_m, init, text_justified = \
                    truncate_clean(line, init, max_char_line_m, text_justified, max_char_line, justification)

                if max_char_line_m >= len(line):
                    max_char_line_m = len(line) - 1
    return text_justified

try:

    text = 'In the beginning God created the heavens and the earth. Now the earth was ' \
           'formless and empty, darkness was over the surface of the deep, and the Spirit ' \
           'of God was hovering over the waters.\nAnd God said, "Let there be light," and there was light. ' \
           'God saw that the light was good, and he separated the light from the darkness. God called the ' \
           'light "day," and the darkness he called "night." And there was evening, and there was morning - the first day.'

    text_justified = truncate(text, 40)
    text_justified_spaces = truncate(text, 40, justification=True)

    print("Texto original:\n")
    print(text)

    print("\nTexto modificado (max 40):\n")
    print(text_justified)

    print("\nTexto modificado (max 40) com justification:\n")
    print(text_justified_spaces)

    text = 'But I must explain to "you" how all this mistaken idea of denouncing pleasure and praising pain was born ' \
           'and I will give you a complete account of the system, and expound the actual teachings of the great ' \
           'explorer of the truth, the master-builder of human happiness.\n\nNo one rejects, dislikes, or avoids'

    text_justified = truncate(text, 15)
    text_justified_spaces = truncate(text, 20, justification=True)

    print("Texto original:\n")
    print(text)

    print("\nTexto modificado (max 20):\n")
    print(text_justified)

    print("\nTexto modificado (max 20) com justification:\n")
    print(text_justified_spaces)

except:
    traceback.print_exc()