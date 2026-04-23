from datetime import date

from validators import is_valid_name
from birthday import Birthday
from user import User, AdminUser
from manager import BirthdayManager


def main():
    manager = BirthdayManager()

    print("=== Birthday Reminder ===")
    username = input("Iveskite vartotojo varda: ").strip()
    role = input("Role (user/admin): ").strip().lower()

    if role == "admin":
        user = AdminUser(username, f"{username}@example.com")
    else:
        user = User(username, f"{username}@example.com")

    manager.add_user(user)
    manager.load_from_file(user)

    while True:
        print("\n--- Meniu ---")
        print("1. Prideti gimtadiení")
        print("2. Istrinti gimtadiení")
        print("3. Rodyti artimiausius gimtadienius")
        print("4. Patikrinti siandienius gimtadienius")
        print("5. Issaugoti i faila")
        print("0. Iseiti")

        choice = input("Pasirinkimas: ").strip()

        if choice == "1":
            name = input("Vardas: ").strip()
            if not is_valid_name(name):
                print("Neteisingas vardas! Varde gali buti tik raides ir tarpai.")
                print("Pvz: Jonas, Ana Maria, Van Der Berg")
                input("\nPaspauskite Enter, kad gryztumete i meniu...")
                continue
            date_str = input("Data (YYYY-MM-DD): ").strip()
            try:
                birth_date = date.fromisoformat(date_str)
                user.add_birthday(Birthday(name, birth_date))
                print(f"{name} sekmingai pridetas.")
                input("\nPaspauskite Enter, kad gryztumete i meniu...")
            except ValueError:
                print("Neteisinga datos forma. Naudokite YYYY-MM-DD, pvz: 1995-06-15")
                input("\nPaspauskite Enter, kad gryztumete i meniu...")

        elif choice == "2":
            if not user.get_birthdays():
                print("\nNera ko trinti - gimtadieniu sarasas tuscias.")
                input("\nPaspauskite Enter, kad gryztumete i meniu...")
            else:
                print("\n--- Gimtadieniu sarasas ---")
                for i, b in enumerate(user.get_birthdays(), 1):
                    print(f"{i}. {b}")
                print("--------------------------")
                name = input("\nIveskite varda kuri norite istrinti: ").strip()
                if user.remove_birthday(name):
                    print(f"{name} sekmingai istrintas.")
                else:
                    print(f"Vardas '{name}' nerastas sarase.")
                input("\nPaspauskite Enter, kad gryztumete i meniu...")

        elif choice == "3":
            days = input("Kiek dienu i prieki rodyti? (Enter = 30): ").strip()
            manager.print_upcoming(username, int(days) if days else 30)
            input("\nPaspauskite Enter, kad gryztumete i meniu...")

        elif choice == "4":
            manager.check_today(username)
            input("\nPaspauskite Enter, kad gryztumete i meniu...")

        elif choice == "5":
            manager.save_to_file(username)
            input("\nPaspauskite Enter, kad gryztumete i meniu...")

        elif choice == "0":
            manager.save_to_file(username)
            print("Iki! Viso gero!")
            break

        else:
            print("Nezinomas pasirinkimas, bandykite dar karta.")
            input("\nPaspauskite Enter, kad gryztumete i meniu...")


if __name__ == "__main__":
    main()
