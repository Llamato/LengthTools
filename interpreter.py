__version__ = "1.0"
__author__ = "Llamato"

from instructions import Instructions
import disassembler
import sys
import threading
from collections import deque
from enum import Enum


class StackUnderflowError(Exception):
    Message = "Stack underflow error. Interpretation stopped"
    Code = 0


class InvalidCommandError(Exception):
    Message = "Invalid command error. Interpretation stopped"
    Code = 1


class AddressNotReachableError(Exception):
    Message = "Address not reachable error. Interpretation stopped"
    Code = 2


class Stack:
    Storage = deque([])
    Top = 0

    def update_top(self):
        self.Top = len(self.Storage)-1

    def push(self, element):
        self.Storage.append(element)
        self.update_top()

    def pop(self):
        try:
           return self.Storage.pop()
        except IndexError:
            raise StackUnderflowError(StackUnderflowError.Message)

    def rotate(self, c):
        self.Storage.rotate(-c)

    def swap(self, a, b):
        temp = self.Storage[a]
        self.Storage[a] = self.Storage[b]
        self.Storage[b] = temp



class LengthThread(threading.Thread):
    class States(Enum):
        New = 0
        NoError = 1
        Stopped = 255
    def __init__(self, code, input_stream=sys.stdin, output_stream=sys.stdout):
        threading.Thread.__init__(self)
        self.Stack = Stack()
        self.State = LengthThread.States.New
        self.ProgramCounter = 0
        self.Code = code
        self.InputStream = input_stream
        self.OutputStream = output_stream

    def inp(self):
        raw_input = self.InputStream.readline().rstrip("\n")
        ascii_number = 0
        if raw_input != "":
            ascii_number = ord(raw_input[0])
        self.Stack.push(ascii_number)
        self.ProgramCounter += 1

    def add(self):
        a = self.Stack.pop()
        b = self.Stack.pop()
        self.Stack.push(b+a)
        self.ProgramCounter += 1

    def sub(self):
        a = self.Stack.pop()
        b = self.Stack.pop()
        self.Stack.push(b-a)
        self.ProgramCounter += 1

    def dup(self):
        self.Stack.push(self.Stack.Storage[-1])
        self.ProgramCounter += 1

    def cond(self):
        a = self.Stack.pop()
        self.ProgramCounter += 1
        if a == 0:
            if self.Code[self.ProgramCounter] == Instructions.push or self.Code[self.ProgramCounter] == Instructions.gotou:
                self.ProgramCounter += 2
            else:
                self.ProgramCounter += 1

    def gotou(self):
        self.ProgramCounter += 1
        self.ProgramCounter = self.Code[self.ProgramCounter]

    def outn(self):
        self.OutputStream.write(str(self.Stack.pop()))
        self.ProgramCounter += 1

    def outa(self):
        self.OutputStream.write(chr(self.Stack.pop()))
        self.ProgramCounter += 1

    def rol(self):
        self.Stack.rotate(1)
        self.ProgramCounter += 1

    def swap(self):
        self.Stack.swap(-1, -2)
        self.ProgramCounter += 1

    def mul(self):
        a = self.Stack.pop()
        b = self.Stack.pop()
        self.Stack.push(b*a)
        self.ProgramCounter += 1

    def div(self):
        a = self.Stack.pop()
        b = self.Stack.pop()
        self.Stack.push(b//a)
        self.ProgramCounter += 1

    def pop(self):
        self.Stack.pop()
        self.ProgramCounter += 1

    def gotos(self):
        address = self.Stack.pop() - 1
        if address < 1 or address > len(self.Code):
            self.State = AddressNotReachableError.Code
            raise AddressNotReachableError(AddressNotReachableError.Message)
        self.ProgramCounter = address

    def push(self):
        self.ProgramCounter += 1
        self.Stack.push(self.Code[self.ProgramCounter])
        self.ProgramCounter += 1

    def ror(self):
        self.Stack.rotate(-1)
        self.ProgramCounter += 1

    def step(self):
        instruction_pointer = {
            Instructions.inp: self.inp,
            Instructions.add: self.add,
            Instructions.sub: self.sub,
            Instructions.dup: self.dup,
            Instructions.cond: self.cond,
            Instructions.gotou: self.gotou,
            Instructions.outn: self.outn,
            Instructions.outa: self.outa,
            Instructions.rol: self.rol,
            Instructions.swap: self.swap,
            Instructions.mul: self.mul,
            Instructions.div: self.div,
            Instructions.pop: self.pop,
            Instructions.gotos: self.gotos,
            Instructions.push: self.push,
            Instructions.ror: self.ror
        }
        instruction_pointer[self.Code[self.ProgramCounter]]()

    def stop(self):
        self.State = LengthThread.States.Stopped
        self.ProgramCounter = 0
        self.Stack.Storage.clear()
        self.InputStream.close()
        self.OutputStream.close()

    def execute(self, ignore_invalid_commands=True):
        self.State = LengthThread.States.NoError
        self.ProgramCounter = 0
        while self.ProgramCounter < len(self.Code) and self.State == LengthThread.States.NoError:
            try:
                self.step()
            except (IndexError, KeyError):
                if ignore_invalid_commands:
                    print("Invalid Command ignored",file=sys.stderr)  # Debug???
                    self.ProgramCounter += 1
                else:
                    self.State = InvalidCommandError.Code
                    raise InvalidCommandError(InvalidCommandError.Message)
        self.State = LengthThread.States.Stopped

    def run(self):  # Needed for Multithreading
        if self.State == LengthThread.States.New:
            self.execute()

    def __del__(self):
        self.stop()


def user_quit_handler():
    print("Program execution aborted by user")
    exit(0)


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
        print("File not found error.", file=sys.stderr)
        exit(0)
    except PermissionError:
        print("Missing permissions to read source code file.", file=sys.stderr)
        exit(0)

    for line in src_file_contents:
        line = line.rstrip("\n")
        program.append(disassembler.disassemble_code(line))
    MainThread = LengthThread(program)
    MainThread.execute()
