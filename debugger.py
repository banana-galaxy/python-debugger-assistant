import sys
import curses
import traceback
import importlib
from pprint import pformat
from typing import Callable, Dict, Tuple
from tui import DebuggerScreen


class Debugger:
    def __init__(self, debuggerscreen: DebuggerScreen, logo: str):
        self.module_name = sys.argv[1]

        try:
            self.module = importlib.import_module(self.module_name)
        except Exception as e:
            raise Exception(
                f"Could not import module - {self.module_name}\nError - {e.__str__()}"
            )

        self.screen = debuggerscreen
        self.commands: Dict[str, Callable] = {}
        self.screen.init(self.commands, logo)
        self.reload()

    def update_commands(self):

        self.commands: Dict[str, Callable] = {
            "Reload Module": self.reload,
        }

        new_cmds = [i for i in dir(self.module) if "__" not in i]
        for i in new_cmds:
            self.commands["Run Function " + i + "()"] = self.handler_func(
                getattr(self.module, i)
            )

        self.commands["Exit Debugger"] = exit
        self.screen.commands = self.commands
        self.screen.current_command_index = 0

        self.screen.commands_window.clear()
        self.screen.commands_window.border()
        self.screen.draw_commands_window()
        self.screen.select_command(0)
        self.screen.commands_window.refresh()

    def reload(self):
        try:
            del sys.modules[self.module_name]
            self.module = importlib.import_module(self.module_name)
            self.update_commands()
            return f"Reloaded module - {self.module.__name__}", 0
        except BaseException as e:
            raise (e)

    def handler_func(self, func):
        """Wraps around functions in the module, to format output, and catch errors"""

        def wrapper():
            result: Tuple

            try:
                result = (
                    "Result - \n"
                    + pformat(func(), width=curses.COLS // 3, compact=False),
                    0,
                )
            except Exception:
                result = "\n".join(traceback.format_stack()), 1

            self.screen.output_window.clear()
            self.screen.output_window.border()
            self.screen.draw_output_window()
            self.screen.output_window.refresh()

            return result

        return wrapper
