__version__ = "0.5"
__author__ = "Llamato"

import sys
import assembler
import disassembler
import interpreter
import debugger

OptionsPrefix = "-"

OptionDescriptions = {
    "t": "Text file",
    "a": "assemble",
    "r": "disassemble",
    "i": "interpret and run",
    "d": "interpret and run with debugger (stack view)"
}


def show_splash_screen():
    print("Length esolang by Nailuj29")
    print("Assembler by", assembler.__author__)
    print("Disassembler by", disassembler.__author__)
    print("Interpreter by", interpreter.__author__)
    print("Debugger by", debugger.__author__)


def show_invalid_arguments_error():
    print("Invalid arguments", file=sys.stderr)


# Handle t parameter
TextFile = None
for index, argument in enumerate(sys.argv):
    if argument == OptionsPrefix + "t":
        try:
            TextFile = open(sys.argv[index], "r").readlines()
        except FileNotFoundError:
            print("File", sys.argv[index], "not found.", file=sys.stderr)
            exit(2)

ProgramCode = []


# Implement additional planed features later. Absolute minimum required functionality achieved
