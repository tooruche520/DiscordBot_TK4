import importlib.util
from pathlib import Path
import sqlite3
import sys
import types
import unittest
from unittest.mock import patch


def load_user_database(connection):
    limit_counter = types.ModuleType("modules.LimitCounter")
    limit_counter.get_limit_count = lambda user_id: 0
    limit_counter.add_count = lambda user_id: None

    module_path = (
        Path(__file__).resolve().parents[1]
        / "modules"
        / "database"
        / "UserDatabase.py"
    )
    spec = importlib.util.spec_from_file_location(
        "user_database_under_test", module_path
    )
    module = importlib.util.module_from_spec(spec)

    with patch.dict(sys.modules, {"modules.LimitCounter": limit_counter}):
        with patch("sqlite3.connect", return_value=connection):
            spec.loader.exec_module(module)

    return module


class UserDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.database = load_user_database(self.connection)

    def test_first_experience_update_creates_unknown_user(self):
        user_id = "new-user"

        self.database.update_user_exp(user_id, 5)

        user = self.database.get_user_by_userid(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.experience, 5)

    def test_existing_user_experience_is_read_by_column_name(self):
        self.database.add_user(self.database.User("existing-user"))

        self.database.update_user_exp("existing-user", 12)

        user = self.database.get_user_by_userid("existing-user")
        self.assertEqual(user.experience, 12)

    def test_deployed_schema_preserves_twitch_and_experience_data(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.execute(
            """
            CREATE TABLE user_exp (
                id INTEGER NOT NULL PRIMARY KEY,
                user_id TEXT,
                adoption INTEGER,
                level DECIMAL,
                twitch_id TEXT,
                experience DECIMAL
            )
            """
        )
        connection.execute(
            """
            INSERT INTO user_exp(user_id, adoption, level, twitch_id, experience)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("deployed-user", 0, 1, "linked-twitch", 40),
        )
        connection.commit()
        database = load_user_database(connection)

        database.update_user_exp("deployed-user", 5)

        user = database.get_user_by_userid("deployed-user")
        twitch_id, experience = connection.execute(
            "SELECT twitch_id, experience FROM user_exp WHERE user_id = ?",
            ("deployed-user",),
        ).fetchone()
        self.assertEqual(user.experience, 45)
        self.assertEqual((twitch_id, experience), ("linked-twitch", 45))

if __name__ == "__main__":
    unittest.main()
