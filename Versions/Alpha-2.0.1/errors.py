import os
from pathlib import Path

path1 = Path(__file__).parents[2]

class AlreadyExists(Exception):
    def __init__(self, name, message="Input already exists!"):
        self.name = name
        self.message = message
        super().__init__(f"{self.message}: '{name}'")

class EmptyEntry(Exception):
    def __init__(self, message="Entry is empty!"):
        self.message = message
        super().__init__(self.message)

class InvalidValue(Exception):
    def __init__(self, value, message="Invalid Value"):
        self.value = value
        self.message = message
        super().__init__(f"{self.message}: '{value}'")

class NotEmpty(Exception):
    def __init__(self, desc, message="already has a value!"):
        self.desc = desc
        self.message = message
        super().__init__(f"{desc} {self.message}")

def error_logging(error_name, date, time):
    path = fr"{path1}\Log\Error"
    error_file = open(fr"{path}\{date}.txt", "a")
    error_file.write(f"Error name: {error_name} ({date}-{time})\n")
    error_file.close()