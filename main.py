import sys
import importlib
import curses
from curses import wrapper
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


def main(win: curses.window):

    # Ensure that screen is large enough
    assert curses.COLS >= 60, "Screen is not wide enough!"
    assert curses.LINES >= 20, "Screen is not long enough!"

    curses.cbreak()

    debugger = Debugger()
    debugger.load()

    commands = {
        "load": debugger.load,
        "reload": debugger.reload,
        "exit": exit,
    }
    new_cmds = [i for i in dir(debugger.module) if "__" not in i]
    for i in new_cmds:
        commands[i] = getattr(debugger.module, i)

    screen = DebuggerScreen(
        win,
        commands,
        10,  # ascii code for enter key => will be used to select commands
        logo,
        debugger.module,
    )

    screen.listen()


if __name__ == "__main__":

    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
