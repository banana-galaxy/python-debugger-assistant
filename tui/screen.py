import curses
from typing import Callable, Dict


class DebuggerScreen:
    def __init__(
        self,
        scrn: curses.window,
        commands: Dict[str, Callable],
        masterkey: int,
        logo: str,
    ):
        """Initialise screen and windows"""

        self.screen = scrn
        self.commands = commands
        self.masterkey = masterkey
        self.logo = logo

        self.current_command_index = 0  # First command is selected

        self.commands_window = curses.newwin(curses.LINES, curses.COLS // 2, 0, 0)

        self.output_window = curses.newwin(
            curses.LINES, curses.COLS - (curses.COLS // 2), 0, curses.COLS // 2
        )

        # Draw borders for screen and windows
        self.screen.border()
        self.commands_window.border()
        self.output_window.border()

        curses.curs_set(0)  # Hide the cursor

        # Initialise windows
        self.draw_commands_window()
        self.draw_output_window()

        # Make sure first command is selected
        self.select_command(self.current_command_index)

        self.screen.refresh()
        self.commands_window.refresh()
        self.output_window.refresh()

    def draw_commands_window(self):
        """Initialise commands window with title and command lists"""

        title = "COMMANDS"
        padding = (curses.COLS // 4 - len(title) // 2 - 1) * " "
        new_line = " " + "─" * (curses.COLS // 2 - 4) + " "

        title = padding + title + padding

        # Draw the title
        self.commands_window.addstr(1, 1, new_line)
        self.commands_window.addstr(2, 1, title, curses.A_BOLD)
        self.commands_window.addstr(3, 1, new_line)

        # Draw each command, with spaces to fill up empty space
        for num, cmd in enumerate(self.commands.keys()):
            self.commands_window.addstr(
                2 * num + 6,
                3,
                "> " + cmd + " " * (curses.COLS // 2 - len("> " + cmd) - 4),
            )

    def draw_output_window(self):
        """Initialise output window with title and logo"""

        self.init_output_window()

        try:
            self.draw_output_window_logo()
        except Exception as e:
            # Screen is too small for the logo
            self.output_window.clear()
            self.output_window.border()
            self.init_output_window()

    def init_output_window(self):
        """Initialise output window with title"""

        title = "OUTPUT"
        padding = (curses.COLS // 4 - len(title) // 2 - 1) * " "
        line = " " + "─" * (curses.COLS // 2 - 4) + " "

        title = padding + title + padding

        self.output_window.addstr(1, 1, line)
        self.output_window.addstr(2, 1, title, curses.A_BOLD)
        self.output_window.addstr(3, 1, line)

    def draw_output_window_logo(self):
        """Draw logo in output window"""

        y_pad = curses.LINES // 2 - len(self.logo.split("\n")) // 2 + 4 // 2

        for ln, text in enumerate(self.logo.split("\n")):
            padding = (curses.COLS // 4 - len(text) // 2 - 1) * " "

            self.output_window.addstr(y_pad + ln, 1, padding + text + padding)

    def select_command(self, pos: int):
        line = 2 * pos + 6

        self.draw_commands_window()  # Overwrite previously drawn styles

        # Highlight the currently selected command
        self.commands_window.chgat(
            line, 3, curses.COLS // 2 - 6, curses.A_STANDOUT | curses.A_ITALIC
        )

    def handle_command(self):

        # Clear the output window
        self.output_window.clear()
        self.output_window.border()
        self.init_output_window()

        cmds = list(self.commands.keys())
        handler = self.commands[cmds[self.current_command_index]]
        handler(self.output_window)

    def listen(self):
        """Start listening for inputs"""

        while True:
            char = self.screen.getch()

            if char == self.masterkey:
                self.handle_command()

            elif char == curses.KEY_DOWN:
                if self.current_command_index < len(self.commands) - 1:
                    self.current_command_index += 1
                else:
                    self.current_command_index = 0

                self.select_command(self.current_command_index)

            elif char == curses.KEY_UP:
                if self.current_command_index > 0:
                    self.current_command_index -= 1
                else:
                    self.current_command_index = len(self.commands) - 1

                self.select_command(self.current_command_index)

            self.output_window.refresh()
            self.commands_window.refresh()
