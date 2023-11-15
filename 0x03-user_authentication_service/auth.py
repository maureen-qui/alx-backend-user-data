"""auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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
            # Check if user with given email already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user does not exist, proceed with registration
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


# Test the _hash_password function
if __name__ == "__main__":
    password = "Hello Holberton"
    hashed_password = _hash_password(password)
    print(hashed_password)

# Test the register_user function
if __name__ == "__main__":
    email = 'me@me.com'
    password = 'mySecuredPwd'

    auth = Auth()

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))
