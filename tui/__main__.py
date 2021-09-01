import curses
from curses import wrapper
from tui import DebuggerScreen

def main(screen: curses.window):

	curses.cbreak()

	debugger = DebuggerScreen(
		screen,
		{
			"reload": lambda a: a.addstr(6, 10, "reload was pressed"),
			"exit": lambda a: a.addstr(8, 10, "exit was pressed"),
			"function": lambda a: a.addstr(10, 10, "function was pressed"),
			"abc": lambda a: a.addstr(12, 10, "abc was pressed"),
		},
		10
	)

	debugger.listen()


if __name__ == "__main__":
	try:
		wrapper(main)
	except KeyboardInterrupt:
		pass
	except Exception as e:
		raise e