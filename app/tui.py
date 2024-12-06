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
            Label("Loading elections...", id="loading_label"), id="election_list"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.load_elections()

    def load_elections(self):
        election_list = self.query_one("#election_list", Vertical)
        for child in list(election_list.children):
            child.remove()

        try:
            elections = self.app.server.get_elections()  # returns list[str]

            if elections:
                election_list.mount(Label("Welcome! Choose an election:"))
                for i, election_name in enumerate(elections):
                    election_list.mount(Button(election_name, id=f"election_{i}"))
            else:
                election_list.mount(Label("No elections available."))

        except Exception as e:
            for child in list(election_list.children):
                child.remove()
            election_list.mount(Label(f"Error loading elections: {e}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # When the user selects an election, get the candidates from the server.
        if event.button.id and event.button.id.startswith("election_"):
            selected_election = event.button.label
            label = self.query(Label).first()

            candidates = self.app.server.get_candidates(str(selected_election))
            try:
                if candidates:
                    # Push the VoteScreen with the list of candidates
                    self.app.push_screen(
                        VoteScreen(
                            election_name=selected_election, candidates=candidates
                        )
                    )
                else:
                    label.update(f"No candidates available for {selected_election}.")
            except Exception as e:
                label.update(f"Error loading candidates: {e}")


class VoteScreen(Screen):
    """Screen for displaying candidates of a selected election."""

    BINDINGS = [("escape", "quit", "Quit"), ("b", "back", "Back")]

    def __init__(self, election_name: str, candidates: list[str]):
        super().__init__()
        self.election_name = election_name
        self.candidates = candidates

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label(f"Candidates for {self.election_name}", id="vote_title")
        yield Vertical(Label("Choose a candidate:"), id="candidate_list")
        yield Footer()

    def on_mount(self):
        candidate_list = self.query_one("#candidate_list", Vertical)
        # Add a button for each candidate
        for i, candidate in enumerate(self.candidates):
            candidate_list.mount(Button(candidate, id=f"candidate_{i}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("candidate_"):
            selected_candidate = event.button.label
            # Here you could call another RPC method like `vote(self.election_name, selected_candidate)`
            # For demonstration, we just update the label
            label = self.query("#vote_title", Label).first()
            label.update(f"You selected {selected_candidate}.")
            # Maybe automatically go back or do something else


class MyApp(App):
    """Main application class."""

    def __init__(self, server_url: str):
        super().__init__()
        self.server_url = server_url
        self.server: xmlrpc.client.ServerProxy

    def on_mount(self):
        self.server = xmlrpc.client.ServerProxy(self.server_url)
        self.push_screen(LoginScreen())


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()
    server_url = f"http://{host}:{port}"
    app = MyApp(server_url=server_url)
    app.run()


if __name__ == "__main__":
    fire.Fire(main)
