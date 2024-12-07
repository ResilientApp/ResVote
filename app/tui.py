import xmlrpc.client
import fire
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Input, Label
from textual.screen import Screen
from src.util import load_server_config


class LoginScreen(Screen):
    """Screen for user login or registration with admin/user selection."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.is_admin = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Login Screen", id="login_title")
        yield Vertical(
            Label("Please enter your credentials:"),
            Input(placeholder="Username", id="username_input"),
            Input(placeholder="Password", id="password_input", password=True),
            Label("Select Role:", id="role_label"),
            Horizontal(
                Button("User", id="user_role_btn"),
                Button("Admin", id="admin_role_btn"),
            ),
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

        if event.button.id == "user_role_btn":
            self.is_admin = False
            message_label.update("Selected role: User")
        elif event.button.id == "admin_role_btn":
            self.is_admin = True
            message_label.update("Selected role: Admin")

        elif event.button.id == "login_btn":
            try:
                success = self.app.server.login(username, password)
                if success:
                    self.app.voter_id = username
                    if self.is_admin:
                        self.app.push_screen(AdminScreen())
                    else:
                        self.app.push_screen(MainScreen())
                else:
                    message_label.update("Login failed. Invalid credentials or role.")
                    self.query_one("#username_input", Input).value = ""
                    self.query_one("#password_input", Input).value = ""
            except Exception as e:
                message_label.update(f"Error connecting to server: {e}")

        elif event.button.id == "register_btn":
            try:
                success = self.app.server.register(username, password, self.is_admin)
                if success:
                    self.app.voter_id = username
                    if self.is_admin:
                        self.app.push_screen(AdminScreen())
                    else:
                        self.app.push_screen(MainScreen())
                else:
                    message_label.update("Registration failed. User already exists.")
                    self.query_one("#username_input", Input).value = ""
                    self.query_one("#password_input", Input).value = ""
            except Exception as e:
                message_label.update(f"Error connecting to server: {e}")


class MainScreen(Screen):
    """Main menu screen displayed after login for regular users."""

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
        if event.button.id and event.button.id.startswith("election_"):
            selected_election = str(event.button.label)
            label = self.query(Label).first()

            try:
                user_vote = self.app.server.get_user_vote(
                    selected_election, self.app.voter_id
                )
                if user_vote is not None:
                    label.update(
                        f"You have already voted for {user_vote} in {selected_election}. Please choose another election."
                    )
                    return
            except Exception as e:
                label.update(f"Error loading candidates: {e}")

            try:
                candidates = self.app.server.get_candidates(selected_election)
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
    """Screen for displaying candidates of a selected election and voting."""

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
            selected_candidate = str(event.button.label)
            label = self.query_one("#vote_title", Label)
            # Cast the vote
            try:
                success = self.app.server.create_vote(
                    self.app.voter_id,
                    self.election_name,
                    selected_candidate,
                )
                if success:
                    label.update(
                        f"Your vote for {selected_candidate} in {self.election_name} has been recorded. Exiting..."
                    )
                    self.set_timer(2.0, self.app.exit)
                else:
                    label.update("Failed to cast vote. Please try again.")
            except Exception as e:
                label.update(f"Error casting vote: {e}")


class CreateElectionScreen(Screen):
    """Screen for admins to create a new election."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
        ("b", "back", "Back to Admin Screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Create a New Election", id="create_election_title")
        yield Vertical(
            Label("Enter Election ID:"),
            Input(placeholder="Election ID", id="election_id_input"),
            Label("Enter Candidates (comma-separated):"),
            Input(placeholder="candidate1,candidate2", id="candidates_input"),
            Button("Create", id="create_btn"),
            Button("Cancel", id="cancel_btn"),
            id="create_election_controls",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        election_id = self.query_one("#election_id_input", Input).value.strip()
        candidates_str = self.query_one("#candidates_input", Input).value.strip()
        label = self.query_one("#create_election_title", Label)

        if event.button.id == "create_btn":
            try:
                # Pass the creator username from self.app.voter_id
                success = self.app.server.create_election(
                    self.app.voter_id, election_id, candidates_str
                )
                if success:
                    label.update(f"Election {election_id} created successfully!")
                    self.set_timer(2.0, self.return_to_admin)
                else:
                    label.update(
                        "Failed to create election. Election may already exist."
                    )
            except Exception as e:
                label.update(f"Error creating election: {e}")
        elif event.button.id == "cancel_btn":
            self.return_to_admin()

    def return_to_admin(self):
        # Go back to AdminScreen
        self.app.pop_screen()

    def action_back(self):
        self.return_to_admin()


class AdminScreen(Screen):
    """Screen for admins with visualization, generate and create election options."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
        ("b", "back", "Back to Login"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_action = None  # "visualization", "generation"
        self.elections_loaded = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label("Admin Menu", id="admin_title")
        yield Vertical(
            Label("Select an action:"),
            Button("Visualization", id="visualization_btn"),
            Button("Generate", id="generate_btn"),
            Button("Create Election", id="create_election_btn"),
            id="admin_actions",
        )
        # A container for elections and results
        yield Vertical(id="admin_elections")
        yield Footer()

    def load_elections(self):
        admin_elections = self.query_one("#admin_elections", Vertical)
        # Clear out old children if any
        for child in list(admin_elections.children):
            child.remove()

        try:
            elections = self.app.server.get_elections()
            if elections:
                admin_elections.mount(Label("Available Elections:"))
                for i, election_name in enumerate(elections):
                    admin_elections.mount(
                        Button(election_name, id=f"admin_election_{i}")
                    )
            else:
                admin_elections.mount(Label("No elections available."))
        except Exception as e:
            admin_elections.mount(Label(f"Error loading elections: {e}"))

    def show_result(self, result: str):
        """Show the result of the selected action."""
        admin_elections = self.query_one("#admin_elections", Vertical)
        # Clear old content
        for child in list(admin_elections.children):
            child.remove()
        admin_elections.mount(Label(result))

    def on_button_pressed(self, event: Button.Pressed):
        label = self.query_one("#admin_title", Label)
        if event.button.id == "visualization_btn":
            self.selected_action = "visualization"
            label.update("Visualization selected. Choose an election:")
            self.load_elections()
        elif event.button.id == "generate_btn":
            self.selected_action = "generation"
            label.update("Generation selected. Choose an election:")
            self.load_elections()
        elif event.button.id == "create_election_btn":
            # Go to the create election screen
            self.app.push_screen(CreateElectionScreen())
        elif event.button.id and event.button.id.startswith("admin_election_"):
            selected_election = str(event.button.label)
            # Call the appropriate RPC based on self.selected_action
            try:
                if self.selected_action == "visualization":
                    # visualization_result = self.app.server.total_vo(
                    #     selected_election
                    # )
                    total_votes = self.app.server.total_votes(selected_election)
                    votes_per_candidate = self.app.server.votes_per_candidate(
                        selected_election
                    )

                    # Format the results
                    if total_votes is None:
                        # Election does not exist
                        full_result = f"Election '{selected_election}' does not exist."
                    else:
                        # full_result = f"Visualization result for {selected_election}: {visualization_result}\n"
                        full_result = f"Total votes: {total_votes}\n"

                        if votes_per_candidate is not None:
                            full_result += "Votes per candidate:\n"
                            for candidate, count in votes_per_candidate.items():
                                full_result += f" - {candidate}: {count}\n"
                        else:
                            full_result += "No candidate vote data available.\n"

                    self.show_result(full_result.strip())

                elif self.selected_action == "generation":
                    result = self.app.server.generation_votes(selected_election)
                    self.show_result(
                        f"Generation result for {selected_election}: {result}"
                    )
            except Exception as e:
                self.show_result(f"Error: {e}")


class MyApp(App):
    """Main application class."""

    def __init__(self, server_url: str):
        super().__init__()
        self.server_url = server_url
        self.server: xmlrpc.client.ServerProxy
        self.voter_id: str = ""

    def on_mount(self):
        # Enable allow_none if needed
        self.server = xmlrpc.client.ServerProxy(self.server_url, allow_none=True)
        self.push_screen(LoginScreen())

    def action_quit(self):
        self.exit()

    def action_back(self):
        # Go back to the previous screen
        self.pop_screen()


def main(config_path: str = "config.yaml"):
    host, port = load_server_config(config_path).unwrap()
    server_url = f"http://{host}:{port}"
    app = MyApp(server_url=server_url)
    app.run()


if __name__ == "__main__":
    fire.Fire(main)
