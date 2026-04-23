import csv
from datetime import date

from birthday import Birthday
from user import User


class BirthdayManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._users = {}
        return cls._instance

    def add_user(self, user: User) -> None:
        self._users[user.get_username()] = user

    def get_user(self, username: str):
        return self._users.get(username)

    def check_today(self, username: str) -> None:
        user = self.get_user(username)
        if not user:
            print("Vartotojas nerastas.")
            return
        found = False
        for b in user.get_birthdays():
            if b.is_today():
                user.send_notification(
                    f"Siandien {b.get_name()} gimtadienis! Sveikiname!"
                )
                found = True
        if not found:
            print("Siandien gimtadieniu nera.")

    def print_upcoming(self, username: str, days: int = 30) -> None:
        user = self.get_user(username)
        if not user:
            print("Vartotojas nerastas.")
            return
        upcoming = [b for b in user.get_birthdays() if b.days_until() <= days]
        upcoming.sort(key=lambda b: b.days_until())
        if not upcoming:
            print(f"Artimiausiomis {days} dienomis gimtadieniu nera.")
            return
        print(f"\nArtimiausi gimtadieniai (per {days} d.):")
        for b in upcoming:
            print(f"  {b}")

    def save_to_file(self, username: str, filepath: str = "birthdays.csv") -> None:
        user = self.get_user(username)
        if not user:
            return
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "name", "birth_date"])
            for b in user.get_birthdays():
                writer.writerow([
                    user.get_username(),
                    b.get_name(),
                    b.get_birth_date().strftime("%Y-%m-%d")
                ])
        print(f"Issaugota i {filepath}")

    def load_from_file(self, user: User, filepath: str = "birthdays.csv") -> None:
        try:
            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username"] == user.get_username():
                        birth_date = date.fromisoformat(row["birth_date"])
                        user.add_birthday(Birthday(row["name"], birth_date))
            print(f"Ikelta is {filepath}")
        except FileNotFoundError:
            print("Failas nerastas, pradedam nuo tusto salygo.")
