import sys
import importlib
import curses
from curses import wrapper
from pprint import pformat

from tui import DebuggerScreen, logo


class Debugger:
    def __init__(self):
        self.module = None
        self.file_name = sys.argv[1].split(".")[0]

    def load(self):
        try:
            self.module = importlib.import_module(self.file_name.split(".")[0])
            return f"Loaded module - {self.module.__name__}", 0
        except BaseException as e:
            return f"Failed to load module: {e}", 1

    def reload(self):
        if self.module is None:
            return "Module has not been loaded!", 1

        try:
            importlib.reload(self.module)
            return f"Reloaded module - {self.module.__name__}", 0
        except BaseException as e:
            return f"Failed to reload module: {e}", 1

    def handler_func(self, func):
        """Wraps around functions in the module, to format output, and catch errors"""

        def wrapper():
            try:
                with open("debug.txt", "w") as f:
                    f.write(str(curses.COLS // 2 - 10))
                result = pformat(func(), width=curses.COLS // 3, compact=True)
                return "Result - " + result, 0
            except Exception as e:
                return e, 1

        return wrapper


def main(win: curses.window):

    # Ensure that screen is large enough
    assert curses.COLS >= 60, "Screen is not wide enough!"
    assert curses.LINES >= 20, "Screen is not long enough!"

    curses.cbreak()

    debugger = Debugger()
    #    debugger.load()

    commands = {
        "Load Module": debugger.load,
        "Reload Module": debugger.reload,
    }

    new_cmds = [i for i in dir(debugger.module) if "__" not in i]
    for i in new_cmds:
        commands["Run Function " + i + "()"] = debugger.handler_func(
            getattr(debugger.module, i)
        )

    commands["Exit Debugger"] = exit

    screen = DebuggerScreen(
        win,
        commands,
        logo,
        debugger,
    )

    screen.listen()


if __name__ == "__main__":

    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
