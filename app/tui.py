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
        # Create a container that will hold the elections once loaded
        yield Vertical(
            Label("Loading elections...", id="loading_label"), id="election_list"
        )
        yield Footer()

    def on_mount(self) -> None:
        # Fetch elections from the server and update UI
        self.load_elections()

    def load_elections(self):
        try:
            elections = self.app.server.get_elections()  # returns list[str]
            election_list = self.query_one("#election_list", Vertical)

            # Remove existing children (including the loading label) by calling remove() on each child
            for child in list(election_list.children):
                child.remove()

            if elections:
                election_list.mount(Label("Welcome! Choose an election:"))
                for i, election_name in enumerate(elections):
                    election_list.mount(Button(election_name, id=f"election_{i}"))
            else:
                election_list.mount(Label("No elections available."))

        except Exception as e:
            election_list = self.query_one("#election_list", Vertical)
            # Remove all children before showing error
            for child in list(election_list.children):
                child.remove()
            election_list.mount(Label(f"Error loading elections: {e}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        label = self.query(Label).first()
        # When an election is selected, update the label
        label.update(f"You selected {event.button.label}.")


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
