__version__ = "1.0"
__author__ = "Llamato#9612"

import asyncio
import sys
import threading
import queue
from typing import Iterable

import discord
import lengthtools
import aiohttp
TOKEN = "ODM4MzI2NTA0Njg0OTEyNjQw.YI5eZg.n_hopMt3nL2ewjyd2VamSTN7mtg"
client = discord.Client()

CodePrefix = "LP:"
CommandPrefix = "LC:"
DiscordThreads = {}


class DiscordIoStream:
    def __init__(self, channel,respect_new_line=True):
        self.waiting_for_input = False
        self.io_queue = queue.Queue()
        self.io_changed = threading.Event()
        self.channel = channel
        self.respect_new_line=True
        self.current_message = ""

    def writeline(self, s):
        self.write()
        self.io_changed.set()

    def writelines(self, __lines: Iterable[str]) -> None:
        for line in __lines:
            self.writeline(line)

    def write(self, __s: str) -> int:
        if self.respect_new_line:
            msg_end = "\n" in __s
            __s = __s.rstrip("\r\n")
            self.current_message += __s
            if msg_end and not __s.isspace() and self.current_message != "":
                self.io_queue.put(self.current_message)
                self.current_message = ""
                self.io_changed.set()
        else:
            self.io_queue.put(__s)
            self.io_changed.set()

    def readline(self):
        return self.io_queue.get()

    def readlines(self):
        lines = list(self.io_queue.queue)
        self.io_queue.queue.clear()
        return lines

    def read(self):

        raise NotImplementedError
        #item = self.input_queue.queue[0]
        #char = item[0]

    def close(self):
        self.waiting_for_input = False
        self.io_changed.clear()
        self.io_queue.queue.clear()
        self.io_queue.queue.clear()


async def get_code_from_attachment(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        raw_data = await response.read();
        raw_string = raw_data.decode("utf-8")
        code = lengthtools.disassembler.disassemble_code(raw_string)
        return code


async def deconstruct_message(msg):  # Must be reworked to return command even if code can not be found before release.
    if len(msg.attachments) > 0:
        url = msg.attachments[0].url
        if url.endswith(".length"):
            code = await get_code_from_attachment(url)
            command = "run"
            return command,code
        return "", ""
    else:
        msg = msg.content
        code_start = msg.find("```length")
        command_start = 0
        command_end = code_start
        if command_end == -1:
            if msg.startswith("length:"):
                command_start = 7
                if msg[command_start] == " ":
                    command_start += 1
                command = msg[command_start:]
                return command, ""
            return "", ""
        command = msg[command_start:command_end].rstrip(" \n")
        code_start += 10
        code_end = msg.find("```", code_start)
        code = msg[code_start:code_end]
        code = lengthtools.disassembler.disassemble_code(code)
        return command, code


async def process_output_streams():
    while True:
        for author_id, discord_thread in DiscordThreads.items():
            if discord_thread.OutputStream.io_changed.is_set():
                while not discord_thread.OutputStream.io_queue.empty():
                    message = discord_thread.OutputStream.readline()
                    if not message.isspace():
                        await discord_thread.OutputStream.channel.send(message)
                discord_thread.OutputStream.io_changed.clear()
        await asyncio.sleep(0.1)


@client.event
async def on_message(message):
    if not message.author.bot:
        user_command, user_code = await deconstruct_message(message)
        user_command = user_command.lower()
        if user_command == "stop" and ((message.author.id in DiscordThreads.keys() and DiscordThreads[message.author.id].State == lengthtools.interpreter.Stopped) or message.author.id not in DiscordThreads):
           await message.channel.send("You are currently not running a program")
        elif user_command == "stop" and message.author.id in DiscordThreads.keys() and DiscordThreads[message.author.id].State != lengthtools.interpreter.Stopped:
            try:
                DiscordThreads[message.author.id].stop()
                DiscordThreads.pop(message.author.id)
                await message.channel.send("Your program has been stopped")
            except:
                await message.channel.send("An unknown error accrued. Your program could not be stopped.")
        elif (user_command == "" or user_code == "") and not (user_command == "" and user_code == ""):
            await message.channel.send("Please format your message like this\n\nCommand\n```length\nCode...\nCode...\nCode...```")
        elif message.author.id in DiscordThreads.keys() and user_command == "run":
            await message.channel.send("You may only run one program at once. Please stop the program you are currently running in order to be able to run a new one.")
        elif user_command == "run":
            try:
                DiscordThreadInputStream = DiscordIoStream(message.channel)
                DiscordThreadOutputStream = DiscordIoStream(message.channel)
                DiscordThreads[message.author.id] = lengthtools.interpreter.LengthThread(user_code, DiscordThreadInputStream, DiscordThreadOutputStream)  #DiscordThreadOutputStream Use sys.stdout for debugging if character erros accur
                DiscordThreads[message.author.id].start()
                await message.channel.send("Program started")
            except:
                DiscordThreads[message.author.id].stop()
                DiscordThreads.pop(message.author.id)
                await message.channel.send("An unknown error accrued. Your program could not be started.")
        elif message.author.id in DiscordThreads.keys():
            DiscordThreads[message.author.id].InputStream.write(message.content)


@client.event
async def on_ready():
    print("Length discord bot online!")


client.loop.create_task(process_output_streams())
client.run(TOKEN)
