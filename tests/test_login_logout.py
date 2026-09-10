import shutil
import tempfile
import unittest
from pathlib import Path
import db
from app import create_app

class TestLoginLogout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  #this creates temporary copy of db
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = Path(cls.temp_dir.name) / "test_fundraising.db"
        shutil.copy("fundraising.db", cls.test_db_path)

        db.DB_PATH = cls.test_db_path
        cls.app = create_app()
        cls.app.config["TESTING"] = True

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def setUp(self):
        self.client = self.app.test_client() #fake browser for route testing

    def test_login_user_admin_success(self):
        response = self.client.post("/login", data={"userName": "aaronlim", "passWord": "pass101", "profileId": "1"},
                                    follow_redirects = True
                                    )
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertIsNotNone(session.get("account_id"))
            self.assertEqual(session.get("profile_id"), 1)

    def test_login_fundraiser_success(self):
        response = self.client.post("/login", data = {"userName": "alextan", "passWord": "pass106", "profileId": "2"},
                                    follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertIsNotNone(session.get("account_id"))
            self.assertEqual(session.get("profile_id"), 2)

    def test_login_donor_success(self):
        response = self.client.post(
            "/login",
            data = {"userName": "leahtan", "passWord": "pass169", "profileId": "3"},
            follow_redirects = True)
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertIsNotNone(session.get("account_id"))
            self.assertEqual(session.get("profile_id"), 3)

    def test_login_platform_management_success(self):
        response = self.client.post(
            "/login",
            data = {"userName": "ivanlee", "passWord": "pass192", "profileId": "4"},
            follow_redirects = True
        )
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertIsNotNone(session.get("account_id"))
            self.assertEqual(session.get("profile_id"), 4)

    def test_login_wrong_password_fails(self):
        response = self.client.post(
            "/login",
            data = {"userName": "evanng", "passWord": "pass300", "profileId": "1"},
            follow_redirects = True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

        with self.client.session_transaction() as session:
            self.assertIsNone(session.get("account_id"))

    def test_login_wrong_username_fails(self):
        response = self.client.post(
            "/login",
            data = {"userName": "evanjames", "passWord": "pass105", "profileId": "1"},
            follow_redirects = True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

        with self.client.session_transaction() as session:
            self.assertIsNone(session.get("account_id"))

    def test_logout_success(self):
        self.client.post("/login",
                         data = {"userName": "aaronlim", "passWord": "pass101", "profileId": "1"},
                         follow_redirects=True)
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertIsNone(session.get("account_id"))
            self.assertIsNone(session.get("profile_id"))
            self.assertIsNone(session.get("session_id"))

