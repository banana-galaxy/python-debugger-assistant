import curses
from curses import wrapper
from typing import Callable, Dict

class DebuggerScreen():
	def __init__(self, scrn: curses.window, commands: Dict[str, Callable]):
		self.screen = scrn
		self.commands = commands

		self.commands_window = curses.newwin(
			curses.LINES,
			curses.COLS // 2,
			0,
			0
		)
		self.output_window = curses.newwin(
			curses.LINES,
			curses.COLS - (curses.COLS // 2),
			0,
			curses.COLS // 2
		)
		
		self.screen.border()
		self.commands_window.border()
		self.output_window.border()

		curses.curs_set(0)

		self.init_commands(commands)
		self.init_output_window()

		self.screen.refresh()
		self.commands_window.refresh()
		self.output_window.refresh()

		self.start_keystroke_listener(
			{
				10: lambda: self.screen.addstr(1, 1, "hi")
			}
		)

	def init_commands(self, commands: Dict[str, Callable]):

		title = "COMMANDS"
		padding = (curses.COLS // 4 - len(title) // 2 - 1) * " "
		new_line = " " + "─" * (curses.COLS // 2 - 4) + " "

		title = padding + title + padding

		self.commands_window.addstr(
			1,
			1,
			new_line
		)
		self.commands_window.addstr(
			2,
			1,
			title,
			curses.A_BOLD
		)
		self.commands_window.addstr(
			3,
			1,
			new_line
		)

		for num, cmd in enumerate(commands.keys()):
			self.commands_window.addstr(
				2 * num + 6,
				3,
				"> " + cmd,
			)

	def init_output_window(self):

		title = "OUTPUT"
		padding = (curses.COLS // 4 - len(title) // 2 - 1) * " "
		new_line = " " + "─" * (curses.COLS // 2 - 4) + " "

		title = padding + title + padding

		self.output_window.addstr(
			1,
			1,
			new_line
		)
		self.output_window.addstr(
			2,
			1,
			title,
			curses.A_BOLD
		)
		self.output_window.addstr(
			3,
			1,
			new_line
		)

	def start_keystroke_listener(self, keybinds: Dict[int, Callable]):

		while True:
			char = self.screen.getch()
			func = keybinds.get(char, lambda: 0)
			func()
			self.screen.refresh()