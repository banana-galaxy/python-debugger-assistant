import curses
from curses import wrapper

from tui import DebuggerScreen, logo
from debugger import Debugger


def main(win: curses.window):

    # Ensure that screen is large enough
    assert curses.COLS >= 60, "Screen is not wide enough!"
    assert curses.LINES >= 20, "Screen is not long enough!"

    curses.cbreak()

    screen = DebuggerScreen(win)
    Debugger(screen, logo)

    screen.listen()


if __name__ == "__main__":

    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
