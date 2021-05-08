import sys

from instructions import Instructions
import disassembler


def generate_code_for_ascii_char(char):
    char_code = []
    if char.isascii():
        char_code = [Instructions.push, ord(char), Instructions.outa]
    return char_code


def generate_code_for_ascii_line(line):
    line_code = []
    for char in line:
        line_code.extend(generate_code_for_ascii_char(char))
    return line_code


def generate_code_for_ascii_text(text):
    text_code = []
    for line in text:
        generate_code_for_ascii_line(line)
        text_code.extend(line)
    return text_code


if __name__ == "__main__":
    for line in sys.stdin:
        line_code = generate_code_for_ascii_line(line)
        for atom in line_code:
            print(disassembler.convert_code_to_mnemonic(atom))
