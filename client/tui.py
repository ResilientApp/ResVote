from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Input, Label
from textual.screen import Screen


class LoginScreen(Screen):
    """Screen for user login or registration."""

    BINDINGS = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        # Remove title argument from Header
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
        username = self.query_one("#username_input", Input).value
        password = self.query_one("#password_input", Input).value

        if event.button.id == "login_btn":
            # Mock check for login
            if username == "user" and password == "pass":
                self.app.push_screen(MainScreen())
            else:
                self.query(Label).first().update("Invalid credentials. Try again.")
                self.query_one("#username_input", Input).value = ""
                self.query_one("#password_input", Input).value = ""

        elif event.button.id == "register_btn":
            # Mock registration logic
            if username and password:
                self.app.push_screen(MainScreen())
            else:
                self.query(Label).first().update(
                    "Please provide both username and password to register."
                )


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
        if event.button.id == "opt1_btn":
            label.update("You selected Option 1.")
        elif event.button.id == "opt2_btn":
            label.update("You selected Option 2.")
        elif event.button.id == "opt3_btn":
            label.update("You selected Option 3.")


class MyApp(App):
    """Main application class."""

    def on_mount(self):
        self.push_screen(LoginScreen())

    # def action_quit(self):
    #     self.exit()

    # def action_back(self):
    #     self.pop_screen()


if __name__ == "__main__":
    app = MyApp()
    app.run()
