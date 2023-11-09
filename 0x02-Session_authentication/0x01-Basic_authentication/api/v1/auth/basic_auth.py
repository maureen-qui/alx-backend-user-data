# api/v1/auth/basic_auth.py

from api.v1.auth.auth import Auth

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

# For testing the method
if __name__ == "__main__":
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
