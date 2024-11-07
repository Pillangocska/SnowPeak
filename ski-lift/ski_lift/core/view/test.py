from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container, ScrollableContainer
from textual.widgets import Header, Footer, Input, RichLog, Static, Button
from textual.screen import ModalScreen
from textual.binding import Binding
from queue import Queue
import asyncio
import random
from datetime import datetime

DEFAULT_HELP_TEXT: str = """
    insert_card <card_id>
        - Inserts a card into the system, using the specified <card_id>.

    remove_card
        - Removes the currently inserted card from the system.

    change_state <state>
        - Changes the engine state to the specified <state>.
          Valid states include MAX_STEAM, FULL_STEAM, HALF_STEAM, and STOPPED.

    display_status
        - Displays the current status of the lift system.

    emergency_stop
        - Stop the ski lift in a case of an emergency.

    abort <command_id>
        - Aborts a delayed command with the specified <command_id>.

    help
        - Displays this help message listing all available commands.
"""

WELCOME_TEXT: str = """
 __                      ___           _
/ _\\_ __   _____      __/ _ \\___  __ _| | __
\\ \\| '_ \\ / _ \\ \\ /\\ / / /_)/ _ \\/ _` | |/ /
_\\ \\ | | | (_) \\ V  V / ___/  __/ (_| |   <
\\__/_| |_|\\___/ \\_/\\_/\\/    \\___|\\__,_|_|\\_\\
"""

class HelpScreen(ModalScreen):
    """A modal screen to display help information"""

    BINDINGS = [
        Binding("escape", "close_help", "Close", show=True),
        Binding("q", "close_help", "Close", show=True),
    ]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    .help-modal {
        width: 90%;
        height: 90%;
        background: $surface;
        border: thick $accent;
        padding: 0;
    }

    .help-title {
        background: $accent;
        color: $text;
        padding: 1;
        text-align: center;
        width: 100%;
        text-style: bold;
    }

    ScrollableContainer {
        height: 100%;
        border: none;
        background: transparent;
    }

    .help-content {
        width: 100%;
        height: auto;
        padding: 1 2;
    }

    .help-text {
        margin: 0 1;
        color: $text;
        text-align: left;
        width: 100%;
    }

    /* Add style for the footer information */
    .help-footer {
        margin-top: 1;
        padding: 1;
        color: $text-muted;
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(classes="help-modal"):
            yield Static("Available commands", classes="help-title")
            with ScrollableContainer():
                with Container(classes="help-content"):
                    yield Static(DEFAULT_HELP_TEXT, classes="help-text")
                    yield Static("Press 'ESC' or 'q' to close", classes="help-footer")

    def action_close_help(self) -> None:
        """Close the help screen"""
        self.app.pop_screen()

class WelcomeBanner(Static):
    """A static welcome banner"""
    def __init__(self):
        super().__init__(WELCOME_TEXT)
        self.can_focus = False

class CustomHeader(Static):
    """A custom header widget with a specific title"""

    DEFAULT_CSS = """
    CustomHeader {
        background: $boost;
        color: $text;
        height: 1;
        width: 100%;
        content-align: center middle;
        dock: top;
    }

    CustomHeader:focus-within {
        background: $accent;
    }
    """

    def __init__(self, title: str):
        super().__init__(title)
        self.title = title

class MessageLog(RichLog):
    """A custom log widget with a title"""

    DEFAULT_CSS = """
    MessageLog {
        height: 100%;
        border: tall gray;
        background: $surface;
        padding: 0 1;
        margin: 0 1;
        layout: vertical;
        overflow-y: scroll;
    }

    MessageLog:focus {
        border: tall green;
    }

    .log-content {
        height: 1fr;  /* Take remaining space */
        overflow-y: auto;
        padding: 0 1;
    }
    """

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.header = CustomHeader(title)
        self.can_focus = True
        self.styles.height = "1fr"

    def compose(self) -> ComposeResult:
        yield self.header

    def on_focus(self) -> None:
        """Called when the widget gains focus"""
        self.styles.border = ("tall", "green")

    def on_blur(self) -> None:
        """Called when the widget loses focus"""
        self.styles.border = ("tall", "gray")

class SnowPeakApp(App):
    """SnowPeak Terminal Interface"""

    TITLE = "SnowPeak Control Center"
    SUB_TITLE = "System Monitor and Control Interface"

    CSS = """
    Screen {
        layout: grid;
        grid-size: 1 4;  /* 1 column, 4 rows */
        grid-gutter: 1;
    }

    WelcomeBanner {
        height: 8;
        content-align: center middle;
        background: $boost;
        color: $accent;
        border: tall $background;
        padding: 0 2;
    }

    MessageLog {
        height: 100%;
        border: tall gray;
        background: $surface;
        padding: 0 1;
        margin: 0 1;
        overflow-y: scroll;
    }

    MessageLog > RichLog {
        height: 1fr;
        min-height: 10;
        background: $surface;
        color: $text;
        overflow-y: scroll;
        padding: 0 1;
        border: none;
    }

    MessageLog:focus {
        border: tall green;
    }

    Input {
        dock: bottom;
        height: 3;
        border: tall $accent;
        background: $surface;
        margin: 1;
        padding: 0 2;
    }

    Input:focus {
        border: tall $accent-lighten-2;
    }

    Input > .input--cursor {
        color: $text;
        background: $accent;
    }

    Input > .input--placeholder {
        color: $text-disabled;
    }

    #welcome {
        text-align: center;
    }

    HelpScreen {
        align: center middle;
    }

    #help-container {
        width: 80%;
        height: auto;
        background: $surface;
        border: thick $accent;
        padding: 1 2;
        margin: 1 2;
    }

    .help-title {
        text-align: center;
        text-style: bold;
        background: $boost;
        padding: 1;
        color: $text;
        margin-bottom: 1;
    }

    .help-content {
        margin: 1 0;
        height: auto;
        min-height: 20;
        color: $text;
    }

    .help-footer {
        text-align: center;
        color: $text-disabled;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("tab", "focus_next", "Focus Next", show=False),
        Binding("shift+tab", "focus_previous", "Focus Previous", show=False),
        # Add the help command binding
        Binding("f1", "show_help", "Show Help", show=True),
    ]

    DEMO_MESSAGES = [
        "Hello from the demo service!",
        "System status: OK",
        "Processing request...",
        "Database connection successful",
        "Cache updated",
        "New client connected",
        "Background task completed",
        "Memory usage: 45%",
        "Network latency: 23ms",
        "Scheduled maintenance in 2 hours"
    ]

    def __init__(self):
        super().__init__()
        self.msg_queue = Queue()
        self.command_queue = Queue()
        self.message_counter = 0
        self._input_ready = False

    def compose(self) -> ComposeResult:
        # Welcome banner at the top
        yield WelcomeBanner()

        # Message logs with custom titles
        incoming = MessageLog("📥 System Event Monitor", id="incoming")
        incoming.styles.border_top = ("heavy", "gray")

        outgoing = MessageLog("📤 Command Output Terminal", id="outgoing")
        outgoing.styles.border_bottom = ("heavy", "gray")

        yield incoming
        yield outgoing
        yield Input(
            placeholder="Enter command... (Tab to switch focus, Enter to send)",
            id="command_input"
        )
        yield Footer()

    async def on_mount(self) -> None:
        """Called when app is mounted"""
        # First set up our widgets
        self.incoming_log = self.query_one("#incoming")
        self.outgoing_log = self.query_one("#outgoing")
        input_widget = self.query_one(Input)
        input_widget.focus()

        # Wait a brief moment to ensure everything is ready
        await asyncio.sleep(0.1)
        self._input_ready = True

        # Now start the message processors
        self.set_interval(2, self.generate_demo_message)
        self.set_interval(1/60, self.process_messages)

    def action_focus_next(self) -> None:
        """Handle tab key to move focus"""
        current = self.screen.focused
        if current:
            widgets = [w for w in self.screen.focus_chain if w.can_focus]
            try:
                index = widgets.index(current)
                next_widget = widgets[(index + 1) % len(widgets)]
                next_widget.focus()
            except ValueError:
                if widgets:
                    widgets[0].focus()

    def action_focus_previous(self) -> None:
        """Handle shift+tab key to move focus backwards"""
        current = self.screen.focused
        if current:
            widgets = [w for w in self.screen.focus_chain if w.can_focus]
            try:
                index = widgets.index(current)
                next_widget = widgets[(index - 1) % len(widgets)]
                next_widget.focus()
            except ValueError:
                if widgets:
                    widgets[-1].focus()

    def generate_demo_message(self):
        """Generate a random demo message"""
        if not self._input_ready:  # Only generate messages when ready
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        message = random.choice(self.DEMO_MESSAGES)
        self.msg_queue.put(("incoming", f"[{timestamp}] {message}"))

    def process_messages(self):
        """Process messages from the queue"""
        try:
            while not self.msg_queue.empty():
                msg_type, message = self.msg_queue.get()
                if msg_type == "incoming":
                    # Use the stored reference instead of querying every time
                    self.incoming_log.write(f"← {message}")
                else:
                    # Use the stored reference instead of querying every time
                    self.outgoing_log.write(f"→ {message}")
        except Exception as e:
            # Log any errors to help with debugging
            print(f"Error processing messages: {e}")

    def action_show_help(self) -> None:
        """Show the help screen when F1 is pressed or command is selected"""
        self.push_screen(HelpScreen())

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input"""
        if not self._input_ready or not event.value.strip():
            return

        command = event.value.lower()
        event.input.value = ""

        # Check if the command is 'help'
        if command == "help":
            self.action_show_help()
            return

        # Process other commands
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.msg_queue.put(("outgoing", f"[{timestamp}] Command sent: {command}"))

        await asyncio.sleep(0.5)
        self.msg_queue.put(("incoming", f"[{timestamp}] Received acknowledgment for: {command}"))

        event.input.focus()


if __name__ == "__main__":
    app = SnowPeakApp()
    app.run()
