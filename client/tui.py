import xmlrpc.client
import fire
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Input, Label
from textual.screen import Screen
from src.util import load_server_config


class LoginScreen(Screen):
    """Screen for user login or registration."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Login Screen", id="login_title")
        yield Vertical(
            Label("Please enter your credentials:"),
            Input(placeholder="Username", id="username_input"),
            Input(placeholder="Password", id="password_input", password=True),
            Horizontal(
                Button("Login", id="login_btn"),
                Button("Register", id="register_btn"),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        message_label = self.query(Label).first()

        if event.button.id == "login_btn":
            try:
                success = self.app.server.login(username, password)
                if success:
                    self.app.push_screen(MainScreen())
                else:
                    message_label.update("Login failed. Invalid username or password.")
                    self.query_one("#username_input", Input).value = ""
                    self.query_one("#password_input", Input).value = ""
            except Exception as e:
                message_label.update(f"Error connecting to server: {e}")

        elif event.button.id == "register_btn":
            try:
                success = self.app.server.register(username, password)
                if success:
                    self.app.push_screen(MainScreen())
                else:
                    message_label.update("Registration failed. User already exists.")
                    self.query_one("#username_input", Input).value = ""
                    self.query_one("#password_input", Input).value = ""
            except Exception as e:
                message_label.update(f"Error connecting to server: {e}")


class MainScreen(Screen):
    """Main menu screen displayed after login."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
        ("b", "back", "Back to Login"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Main Menu", id="main_title")
        yield Vertical(
            Label("Welcome! Choose an option:"),
            Button("Option 1", id="opt1_btn"),
            Button("Option 2", id="opt2_btn"),
            Button("Option 3", id="opt3_btn"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        label = self.query(Label).first()
        # Example of further server interaction could go here
        if event.button.id == "opt1_btn":
            label.update("You selected Option 1.")
        elif event.button.id == "opt2_btn":
            label.update("You selected Option 2.")
        elif event.button.id == "opt3_btn":
            label.update("You selected Option 3.")


class MyApp(App):
    """Main application class."""

    def __init__(self, server_url: str):
        super().__init__()
        self.server_url = server_url
        self.server: xmlrpc.client.ServerProxy

    def on_mount(self):
        # Initialize the server proxy once here, so all screens can use it
        self.server = xmlrpc.client.ServerProxy(self.server_url)
        # Start the app on the login screen
        self.push_screen(LoginScreen())


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()
    server_url = f"http://{host}:{port}"
    app = MyApp(server_url=server_url)
    app.run()


if __name__ == "__main__":
    fire.Fire(main)
