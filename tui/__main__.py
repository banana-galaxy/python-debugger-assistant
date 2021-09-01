import curses
from curses import wrapper
from tui import DebuggerScreen

def main(screen: curses.window):

	debugger = DebuggerScreen(
		screen,
		{
			"reload": print,
			"exit": print,
			"function": input,
			"abc": bool,
			"lkjdsd": int,
			"dorime": str, # Commands that can be used
		}
	)

	curses.napms(5000)


if __name__ == "__main__":
	wrapper(main)