__version__ = "1.0"
__author__ = "Llamato"

from instructions import Instructions


class AssemblerError(Exception):
    def get_error_msg(self, v):
        return str(v) + "is not a valid in instruction nor valid data"


class InvalidInstructionError(AssemblerError):
    def get_error_msg(self, v):
        return str(v) + " is not a valid instruction"


class InvalidDataError(AssemblerError):
    def get_error_msg(self, v):
        return str(v) + " is not valid data"


def fill_string_to_match(string, filler, target_length):
    current_fill_char = 0
    while len(string) < target_length:
        string += filler[current_fill_char]
        current_fill_char += 1
        if current_fill_char == len(filler):
            current_fill_char = 0
    return string


def convert_line_to_code(line):
    if line in Instructions.Opcodes.keys():
        return Instructions.Opcodes[line]
    else:  # Should we implement char support later?
        try:
            data = int(line)
            return data
        except ValueError:
            errored_out = True
    if errored_out:
        raise AssemblerError(str(line) + " is not a valid in instruction nor valid data")


def assemble_code(block, fill_char=" "):
    if type(block) is list:
        for index, element in enumerate(block):
            block[index-1] = assemble_code(element)
        return block
    elif type(block) is int:
        return "".ljust(block, fill_char)


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        end = "\n"
        if line[-1] == end:
            line = line.rstrip(end)
        print(assemble_code(convert_line_to_code(line), fill_char="0"), end=end)
