#!/usr/bin/env python3
# auth.py
from db import DB
import bcrypt
import uuid
from user import User
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted hash of the input password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            User: User object representing the newly registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user credentials.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID.

        Returns:
            str: String representation of a new UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Create a session for the user.

        Args:
            email (str): User's email.

        Returns:
            str: Session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get user from session ID.

        Args:
            session_id (str): Session ID.

        Returns:
            User: User object corresponding to the session ID.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy user session.

        Args:
            user_id (int): User ID.
        """
        user = self._db.find_user_by(id=user_id)
        user.session_id = None
        self._db._session.commit()

    def get_reset_password_token(self, email: str) -> str:
        """
        Get reset password token.

        Args:
            email (str): User's email.

        Returns:
            str: Reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            user.reset_token = reset_token
            self._db._session.commit()
            return reset_token
        except NoResultFound:
            raise ValueError("User not found.")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user password.

        Args:
            reset_token (str): Reset password token.
            password (str): New password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            user.hashed_password = hashed_password
            user.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError("User not found.")

