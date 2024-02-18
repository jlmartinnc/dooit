import appdirs
import msgpack
import os
from typing import Dict
from pathlib import Path
from os import makedirs

XDG_CONFIG = Path(appdirs.user_config_dir("dooit"))
XDG_DATA = Path(appdirs.user_data_dir("dooit"))


class Parser:
    """
    Parser class to manage and parse dooit's config and data
    """

    @property
    def last_modified(self) -> float:
        return os.stat(self.todo_data).st_mtime

    def __init__(self) -> None:
        self.check_files()

    def save(self, data) -> None:
        """
        Save the todos to data file
        """

        with open(self.todo_data, "wb") as stream:
            stream.write(msgpack.packb(data, use_bin_type=True))

    def load(self) -> Dict:
        """
        Retrieves the todos from data file
        """

        with open(self.todo_data, "rb") as stream:
            data = msgpack.unpackb(stream.read(), raw=False)

        return data

    def check_files(self) -> None:
        """
        Checks if all the files and folders are present
        to avoid any errors
        """

        makedirs(XDG_CONFIG, exist_ok=True)
        makedirs(XDG_DATA, exist_ok=True)

        self.todo_data = XDG_DATA / "todo.dat"
        self.config_file = XDG_CONFIG / "config.py"

        if not Path.is_file(self.todo_data):
            self.save(dict())

        if not Path.is_file(self.config_file):
            with open(self.config_file, "w") as _:
                pass
