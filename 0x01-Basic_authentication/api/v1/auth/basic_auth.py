# api/v1/auth/basic_auth.py

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        # Return None for invalid or missing authorization headers
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None

        # Extract and return the Base64 part of the Authorization header
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        # Return None if base64_authorization_header is None or not a string
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None

        try:
            # Check if the header starts with "Basic " and extract the base64 part
            if base64_authorization_header.startswith("Basic "):
                base64_part = base64_authorization_header[6:]
                # Decode the Base64 string and return it as a UTF-8 string
                decoded_bytes = base64.b64decode(base64_part)
                return decoded_bytes.decode("utf-8")
            else:
                return None  # Header doesn't start with "Basic "

        except Exception:
            return None  # Invalid Base64
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        # Return None, None for invalid or missing decoded authorization headers
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ':' not in decoded_base64_authorization_header
        ):
            return None, None

        # Split the decoded string into email and password using :
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        # Return None for invalid or missing user_email or user_pwd
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        # Search for the user in the database based on email
        users = User.search({'email': user_email})

        # Return None if user not found in the database
        if not users:
            return None

        user = users[0]

        # Return None if the provided password is not valid
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        # Return None for invalid or missing request
        if request is None:
            return None

        # Retrieve the authorization header from the request
        auth_header = self.authorization_header(request)

        # Return None if authorization header is not valid
        if auth_header is None:
            return None

        # Extract and decode the Base64 part of the authorization header
        decoded_auth_header = self.decode_base64_authorization_header(auth_header)

        # Return None if decoding fails
        if decoded_auth_header is None:
            return None

        # Extract user credentials from the decoded authorization header
        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)

        # Return the User instance based on the extracted credentials
        return self.user_object_from_credentials(user_email, user_pwd)
# For testing the method
if __name__ == "__main__":
    import uuid

    # Create a user test
    user_email = str(uuid.uuid4())
    user_clear_pwd = str(uuid.uuid4())
    user = User()
    user.email = user_email
    user.first_name = "Bob"
    user.last_name = "Dylan"
    user.password = user_clear_pwd
    print("New user: {}".format(user.display_name()))
    user.save()

    # Retrieve this user via the class BasicAuth
    a = BasicAuth()

    u = a.user_object_from_credentials(None, None)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(89, 98)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials("email@notfound.com", "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, user_clear_pwd)
    print(u.display_name() if u is not None else "None")

    a = BasicAuth()
    print(a.extract_base64_authorization_header(None))
    print(a.extract_base64_authorization_header(89))
    print(a.extract_base64_authorization_header("Holberton School"))
    print(a.extract_base64_authorization_header("Basic Holberton"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.extract_base64_authorization_header("Basic1234"))

    print(a.decode_base64_authorization_header(None))
    print(a.decode_base64_authorization_header(89))
    print(a.decode_base64_authorization_header("Holberton School"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

    print(a.extract_user_credentials(None))
    print(a.extract_user_credentials(89))
    print(a.extract_user_credentials("Holberton School"))
    print(a.extract_user_credentials("Holberton:School"))
    print(a.extract_user_credentials("bob@gmail.com:toto1234"))
