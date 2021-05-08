__version__ = "1.0"
__author__ = "Llamato"

from lengthtools.disassembler import diassembler
from lengthtools.interpreter import interpreter
import sys

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, quit)
    program = []
    src_file_contents = ""
    try:
        src_file = open(sys.argv[1], "r")
        src_file_contents = src_file.readlines()
        src_file.close()
    except IndexError:
        print("Please supply source code file via program parameter.")
        exit(0)
    except FileNotFoundError:
        print("File not found error. Please supply source code file via program parameter.", file=sys.stderr)
        exit(0)
    except PermissionError:
        print("Missing permissions to read source code file.", file=sys.stderr)
        exit(0)

    program_code = []
    for index, line in enumerate(src_file_contents):
        line = line.rstrip("\n")
        src_file_contents[index] = line
        program_code.append(disassembler.disassemble_code(line))

    MainThread = interpreter.LengthThread(program_code)
    while MainThread.ProgramCounter < len(MainThread.Code) and MainThread.State == interpreter.NoError:
        print("\nAt line:", MainThread.ProgramCounter+1, "Current Instruction:", disassembler.convert_code_to_mnemonic(MainThread.Code[MainThread.ProgramCounter]), "Stack:", list(MainThread.Stack.Storage))
        MainThread.step()
    MainThread.stop()
    print("Program ended normally")
