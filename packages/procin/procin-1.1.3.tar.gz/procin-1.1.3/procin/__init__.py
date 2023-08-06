"""Top-level package for procin."""
__author__ = """Powell Quiring"""
__email__ = "powellquiring@gmail.com"
__version__ = "1.1.3"

import subprocess

# import typing
import json
from pathlib import Path
import codecs
import os.path
import copy

class Command:
    def __init__(self, json=False, print_command=False, print_output=False, print_error=True, catch=False, cache=False, cache_dir=None):
        self.json = json
        self.print_command = print_command
        self.print_output = print_output
        self.print_error = print_error
        self.catch = catch
        self.cache = cache
        if self.cache:
            if cache_dir == None:
                raise AttributeError("cache_dir required")
            if cache_dir[0] == "/":
                self.cache_dir = cache_dir
            else:
                self.cache_dir = os.path.expanduser("~/procin/" + cache_dir)
        if self.cache:
            self.cache_path = Path(self.cache_dir)
            if self.cache_path.exists():
                if not self.cache_path.is_dir():
                    raise NotADirectoryError(self.cache_path)
            else:
                self.cache_path.mkdir()
        self.escape = {'^': '^', '$': 'd', ' ':'s', '\t': 't', '[':'l', ']':'r', '{':'L', '}': 'R', '/': 'f', '\\': 'b'}
        self.unescape = {value: key for (key, value) in self.escape.items()}
        self.unescape['n'] = 'n'

    
    def command_to_filename(self, command):
        """lossless conversion from a command to a file string"""
        filename = ""
        for word in command:
            for c in word:
                ch = c
                if c in self.escape:
                    ch = '^' + self.escape[c]
                filename += ch
            filename += "^n"
        return codecs.encode(filename, 'unicode-escape').decode('ascii')
    
    def filename_to_command(self, filename):
        lines = codecs.decode(filename, 'unicode-escape')
        escape = False
        command = []
        word = ""
        for c in lines:
            if escape:
                c = self.unescape[c]
                if c == 'n':
                    command.append(word)
                    word = ""
                else:
                    word += c
                escape = False
            else:
                if c == '^':
                    escape = True
                else:
                    word += c
        return command

    def file_cache_path(self, command):
        return Path(self.cache_dir) / self.command_to_filename(command)

    def clear_cache(self):
        for f in self.cache_path.glob("*"):
            if str(f)[-2:] == "^n":
                # make sure it ends in a new line, avoid catastrophe
                f.unlink()

    def in_cache(self, command):
        """text of the cache hit or None"""
        if self.cache:
            file_cache_path = self.file_cache_path(command)
            if file_cache_path.exists():
                return file_cache_path.read_text()
        return None

    def run_with_cache(self, command):
        stdout = self.in_cache(command)
        if stdout:
            return stdout
        out = subprocess.check_output(command)
        stdout = out.decode()
        if self.cache:
            self.file_cache_path(command).write_text(stdout)
        return stdout

    def run(self, command, **kwargs):
        c = copy.copy(self)
        for var, value in kwargs.items():
            if var in c.__dict__:
                c.__dict__[var] = value
            else:
                raise AttributeError(var)

        if c.print_command:
            print(' '.join(command))

        try:
            stdout = c.run_with_cache(command)
        except:
            if c.catch:
                print('*** Command execution failed')
                stdout = ""
            else:
                raise
        if c.print_output:
            print(stdout)
        if c.json:
            return json.loads(stdout)
        else:
            return stdout
