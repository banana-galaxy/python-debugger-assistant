import curses
import regex
from pprint import pformat
from typing import Callable, Dict


class DebuggerScreen:
    def __init__(self, screen: curses.window) -> None:
        self.screen = screen

    def init(self, commands: Dict[str, Callable], logo: str):
        """Initialise screen and windows"""

        self.commands = commands
        self.logo = logo

        self.current_command_index = 0  # First command is selected

        self.commands_window_width = 2 * curses.COLS // 5
        self.output_window_width = curses.COLS - self.commands_window_width

        self.commands_window = curses.newwin(
            curses.LINES, self.commands_window_width, 0, 0
        )
        self.output_window = curses.newwin(
            curses.LINES, self.output_window_width, 0, self.commands_window_width
        )

        self.init_colors()

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

    def init_colors(self):
        # Default colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Scheme for commands window
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # Scheme for output window content
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Scheme for titles
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # Scheme for python logo
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # Errors
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

        self.commands_window.bkgdset(" ", curses.color_pair(2))
        self.output_window.bkgdset(" ", curses.color_pair(2))

    def draw_commands_window(self):
        """Initialise commands window with title and command lists"""

        title = "COMMANDS"
        padding = (self.commands_window_width // 2 - len(title) // 2 - 1) * " "
        new_line = " " + "???" * (self.commands_window_width - 4) + " "

        title = padding + title + padding

        # Draw the title
        self.commands_window.addstr(1, 1, new_line, curses.color_pair(4))
        self.commands_window.addstr(2, 1, title, curses.A_BOLD | curses.color_pair(4))
        self.commands_window.addstr(3, 1, new_line, curses.color_pair(4))

        # Draw each command, with spaces to fill up empty space
        for num, cmd in enumerate(self.commands.keys()):
            self.commands_window.addstr(
                2 * num + 6,
                3,
                "> " + cmd + " " * (self.commands_window_width - len("> " + cmd) - 4),
            )

    def draw_output_window(self):
        """Initialise output window with title and logo"""

        self.init_output_window()

        try:
            self.draw_output_window_logo()
        except Exception:
            # Screen is too small for the logo
            self.output_window.clear()
            self.output_window.border()
            self.init_output_window()

    def init_output_window(self):
        """Initialise output window with title"""

        title = "OUTPUT"
        padding = (self.output_window_width // 2 - len(title) // 2 - 1) * " "
        line = " " + "???" * (self.output_window_width - 4) + " "

        title = padding + title + padding

        self.output_window.addstr(1, 1, line, curses.color_pair(4))
        self.output_window.addstr(2, 1, title, curses.A_BOLD | curses.color_pair(4))
        self.output_window.addstr(3, 1, line, curses.color_pair(4))

    def draw_output_window_logo(self):
        """Draw logo in output window"""

        y_pad = curses.LINES // 2 - len(self.logo.split("\n")) // 2 + 1

        for ln, text in enumerate(self.logo.split("\n")):
            text = text.strip()
            padding = (self.output_window_width // 2 - len(text) // 2 - 1) * " "

            t1, t2 = text.split("|")

            # Python logo has 2 colors - yellow on top left,
            # and blue on bottom right
            # so `|` is used to separate these two groups in the logo

            self.output_window.addstr(y_pad + ln, 1, padding + t1, curses.color_pair(5))
            self.output_window.addstr(
                y_pad + ln,
                1 + len(t1) + len(padding),
                t2 + padding,
                curses.color_pair(4),
            )

    def select_command(self, pos: int):
        line = 2 * pos + 6

        self.draw_commands_window()  # Overwrite previously drawn styles

        # Highlight the currently selected command
        self.commands_window.chgat(
            line,
            3,
            self.commands_window_width - 6,
            curses.A_STANDOUT | curses.A_ITALIC | curses.color_pair(1),
        )

    def paginate(self, text: str):
        """Ensure that text doesn't overflow horizontally"""

        paginated = [""]
        pos = 0
        for char in text:
            pos += 1
            if pos >= self.output_window_width - 5:
                paginated.append("")
                paginated[-1] += char
                pos = 0
            elif char == "\n":
                pos = 0
                paginated.append("")
            else:
                paginated[-1] += char

        return paginated

    def handle_command(self):
        """Run a command, capture the output, paginate it, then prettify and display it"""

        # Clear the output window
        self.output_window.clear()
        self.output_window.border()
        self.init_output_window()

        cmds = list(self.commands.keys())
        cmd = cmds[self.current_command_index]
        handler = self.commands[cmd]

        result = handler()

        error = result[1] != 0  # Check if an error ocurred while running the command.
        result = result[0]

        color = [curses.color_pair(1), curses.color_pair(6)][error]

        self.output_window.clear()
        self.output_window.border()
        self.init_output_window()

        if cmd.startswith("Run Function "):
            # Some pretty printing

            name = regex.search(r"Run Function (\w+)\(\)", cmd)
            if name:
                handler.__name__ = name.groups()[0]
            else:
                handler.__name__ = "Anonymous"

            if not error:
                res = result
                result = self.paginate(
                    pformat(result, width=curses.COLS // 3, compact=False)
                )
                self.output_window.addstr(
                    6,
                    3,
                    f"Call to function {handler.__name__}() returned -",
                    curses.color_pair(3),
                )
                self.output_window.addstr(
                    len(result) + 8, 3, f"Return type = {type(res)}"
                )
            else:
                result = self.paginate(
                    f"Error while calling function {handler.__name__}!\n" + result
                )
        else:
            result = self.paginate(result)

        for pos, line in enumerate(result):
            self.output_window.addstr(pos + 7 - int(error), 3, line, color)

    def listen(self):
        """Start listening for inputs"""

        while True:
            char = self.screen.getch()

            if char == 10:
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
