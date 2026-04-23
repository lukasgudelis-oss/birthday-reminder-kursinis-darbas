from notifiable import Notifiable
from birthday import Birthday


class User(Notifiable):
    def __init__(self, username: str, email: str) -> None:
        self._username = username
        self._email = email
        self._birthdays = []

    def get_username(self) -> str:
        return self._username

    def get_email(self) -> str:
        return self._email

    def get_birthdays(self) -> list:
        return self._birthdays

    def add_birthday(self, birthday: Birthday) -> None:
        self._birthdays.append(birthday)

    def remove_birthday(self, name: str) -> bool:
        for b in self._birthdays:
            if b.get_name().lower() == name.lower():
                self._birthdays.remove(b)
                return True
        return False

    def send_notification(self, message: str) -> None:
        print(f"[{self._username}] Pranesimas: {message}")

    def __str__(self) -> str:
        return f"User({self._username}, {self._email})"


class AdminUser(User):
    def send_notification(self, message: str) -> None:
        print(f"[ADMIN - {self._username}] *** {message} ***")
