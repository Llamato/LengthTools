__version__ = "1.0"
__author__ = "Llamato"

from instructions import Instructions


def disassemble_code(block):
    if "\n" in block:
        blocks = block.splitlines()
        while "" in blocks:
            blocks.remove("")
        for index, current_block in enumerate(blocks):
            blocks[index] = disassemble_code(current_block)
        return blocks
    return len(block)


def convert_code_to_mnemonic(code):
    try:
        return Instructions.Mnemonics[code]
    except KeyError as e:  # Improve to be able to handle blank lines in code
        return str(code)


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line = line.rstrip("\n")
        print(convert_code_to_mnemonic(disassemble_code(line)))
