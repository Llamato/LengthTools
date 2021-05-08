__version__ = "1.0"
__author__ = "Llamato"


def get_lines(input):
    lines = input.split("\n")
    for line in lines:
        if line == "":
            lines.remove(line)
    return lines


def get_words(text):
        words = text.split()
        return words


def get_length_sum(strings):
    return len(" ".join(strings))


def textify_simple(asm, txt):
    output_lines = []
    text_pos = 0
    txt = txt.replace("\n", "")
    for asm_line in get_lines(asm):
        asm_line = asm_line.rstrip("\n")
        output_line_end = text_pos + len(asm_line)
        if output_line_end > len(txt):
            txt.ljust(output_line_end - len(txt))
        else:
            output_line = txt[text_pos:output_line_end]
        output_lines.append(output_line)
        text_pos = output_line_end
    return output_lines


def textify_keep_words(asm, txt):
    output_lines = []
    txt_words = get_words(txt)
    current_word = 0
    leftover_word = ""
    for asm_line in get_lines(asm):
        output_line_words = []
        if leftover_word != "":
            output_line_words.append(leftover_word)
        output_line_length = get_length_sum(output_line_words)
        while len(asm_line) > output_line_length and current_word < len(txt_words):
            output_line_words.append(txt_words[current_word])
            current_word += 1
            output_line_length = get_length_sum(output_line_words)
        if current_word >= len(txt_words):
            output_line_words.append("".ljust(len(asm_line)-output_line_length))
        if len(asm_line) < output_line_length:
            leftover_word = output_line_words[-1:][0]
            output_line_words = output_line_words[:-1]
            output_line_length = get_length_sum(output_line_words)  # Not effective. Is equaivalent to second to last round of while. Can we store that value somewhere?
            output_line_words.append("".ljust(len(asm_line)-output_line_length-1))
            if len(output_line_words) == 1:
                output_line_words.append("")
        elif len(asm_line) == output_line_length:
            leftover_word = ""
        output_lines.append(" ".join(output_line_words))
    return output_lines


if __name__ == "__main__":
    import sys
    try:
        asm_file = open(sys.argv[1], "r")  # Switch this around and make it so that that stdin can replace the second parameter
        txt_file = open(sys.argv[2], "r")
        asm_content = asm_file.read()
        asm_file.close()
        txt_content = txt_file.read()
        txt_file.close()
        #output_lines = textify_keep_words(asm_content, txt_content)
        output_lines = textify_keep_words(asm_content, txt_content)
        for output_line in output_lines:
            print(output_line)
    except IndexError as e:
        print("expected two arguments sourcecode file and text file", file=sys.stderr)
    except FileNotFoundError as e:
        print("file not found.", e.filename, file=sys.stderr)
    except PermissionError as e:
        print("access to file denied. Make sure you have the necessary permissions", file=sys.stderr)
