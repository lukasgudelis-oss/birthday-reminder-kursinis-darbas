# test_birthday_reminder.py
# Unit testai su unittest framework

import unittest
from datetime import date

from validators import is_valid_name
from birthday import Birthday
from user import User, AdminUser
from manager import BirthdayManager


class TestIsValidName(unittest.TestCase):

    def test_valid_simple_name(self):
        self.assertTrue(is_valid_name("Jonas"))

    def test_valid_name_with_space(self):
        self.assertTrue(is_valid_name("Ana Maria"))

    def test_empty_string(self):
        self.assertFalse(is_valid_name(""))

    def test_name_with_number(self):
        self.assertFalse(is_valid_name("Jonas1"))

    def test_name_with_special_char(self):
        self.assertFalse(is_valid_name("Jonas@"))

    def test_name_with_dash(self):
        # Bruksnelis nera raides - turi grazinti False
        self.assertFalse(is_valid_name("Van-Der"))


class TestBirthday(unittest.TestCase):

    def setUp(self):
        self.bd = Birthday("Jonas", date(1995, 6, 15))

    def test_get_name(self):
        self.assertEqual(self.bd.get_name(), "Jonas")

    def test_get_birth_date(self):
        self.assertEqual(self.bd.get_birth_date(), date(1995, 6, 15))

    def test_is_today_false(self):
        # 1995-06-15 tikrai ne siandien (nebent testas paleidamas birzeliu)
        today = date.today()
        if today.month == 6 and today.day == 15:
            self.assertTrue(self.bd.is_today())
        else:
            self.assertFalse(self.bd.is_today())

    def test_is_today_true(self):
        today = date.today()
        bd_today = Birthday("Siandieninis", today)
        self.assertTrue(bd_today.is_today())

    def test_days_until_non_negative(self):
        self.assertGreaterEqual(self.bd.days_until(), 0)

    def test_str_contains_name(self):
        self.assertIn("Jonas", str(self.bd))


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("petras", "petras@example.com")

    def test_get_username(self):
        self.assertEqual(self.user.get_username(), "petras")

    def test_get_email(self):
        self.assertEqual(self.user.get_email(), "petras@example.com")

    def test_add_birthday(self):
        bd = Birthday("Jonas", date(1990, 1, 1))
        self.user.add_birthday(bd)
        self.assertEqual(len(self.user.get_birthdays()), 1)

    def test_remove_birthday_success(self):
        bd = Birthday("Jonas", date(1990, 1, 1))
        self.user.add_birthday(bd)
        result = self.user.remove_birthday("Jonas")
        self.assertTrue(result)
        self.assertEqual(len(self.user.get_birthdays()), 0)

    def test_remove_birthday_not_found(self):
        result = self.user.remove_birthday("Neegzistuojantis")
        self.assertFalse(result)

    def test_remove_birthday_case_insensitive(self):
        bd = Birthday("Jonas", date(1990, 1, 1))
        self.user.add_birthday(bd)
        result = self.user.remove_birthday("JONAS")
        self.assertTrue(result)

    def test_send_notification(self, ):
        # Tikriname kad send_notification nekelia klaidos
        try:
            self.user.send_notification("Testas")
        except Exception as e:
            self.fail(f"send_notification() isskele klaida: {e}")


class TestAdminUser(unittest.TestCase):

    def test_admin_is_user(self):
        # Inheritance - AdminUser turi buti User egzempliorius
        admin = AdminUser("admin", "admin@example.com")
        self.assertIsInstance(admin, User)

    def test_admin_send_notification(self):
        admin = AdminUser("admin", "admin@example.com")
        try:
            admin.send_notification("Admin testas")
        except Exception as e:
            self.fail(f"AdminUser send_notification() isskele klaida: {e}")


class TestBirthdayManagerSingleton(unittest.TestCase):

    def test_singleton(self):
        # Singleton - du objektai turi buti tas pats egzempliorius
        m1 = BirthdayManager()
        m2 = BirthdayManager()
        self.assertIs(m1, m2)


class TestBirthdayManagerOperations(unittest.TestCase):

    def setUp(self):
        # Singleton - reikia pasirupinti kad testai nesusipainiotų
        self.manager = BirthdayManager()
        self.user = User("tester", "tester@example.com")
        self.manager.add_user(self.user)

    def test_add_and_get_user(self):
        retrieved = self.manager.get_user("tester")
        self.assertEqual(retrieved.get_username(), "tester")

    def test_get_nonexistent_user(self):
        result = self.manager.get_user("niekam_neegzistuoja")
        self.assertIsNone(result)

    def test_save_and_load(self):
        bd = Birthday("Testuojamas", date(2000, 5, 20))
        self.user.add_birthday(bd)
        self.manager.save_to_file("tester", "test_output.csv")

        # Naujas vartotojas nuskaito is failo
        new_user = User("tester", "tester@example.com")
        self.manager.add_user(new_user)
        self.manager.load_from_file(new_user, "test_output.csv")

        names = [b.get_name() for b in new_user.get_birthdays()]
        self.assertIn("Testuojamas", names)


if __name__ == "__main__":
    unittest.main()
