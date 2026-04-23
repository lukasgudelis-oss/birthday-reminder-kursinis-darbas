from datetime import date


class Birthday:
    def __init__(self, name: str, birth_date: date) -> None:
        self._name = name
        self._birth_date = birth_date

    def get_name(self) -> str:
        return self._name

    def get_birth_date(self) -> date:
        return self._birth_date

    def days_until(self) -> int:
        today = date.today()
        this_year = self._birth_date.replace(year=today.year)
        if this_year < today:
            this_year = this_year.replace(year=today.year + 1)
        return (this_year - today).days

    def is_today(self) -> bool:
        today = date.today()
        return (
            self._birth_date.month == today.month
            and self._birth_date.day == today.day
        )

    def __str__(self) -> str:
        return (
            f"{self._name} - {self._birth_date.strftime('%Y-%m-%d')} "
            f"(po {self.days_until()} d.)"
        )
