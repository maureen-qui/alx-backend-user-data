from typing import List, TypeVar
from flask import request

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths to exclude from authentication.

        Returns:
            bool: True if authentication is required, False if it is excluded.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        
        for excluded_path in excluded_paths:
            # Check if the path starts with an excluded path (ignoring trailing slashes)
            if path.startswith(excluded_path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the Flask request.

        Args:
            request: The Flask request object.

        Returns:
            str: The authorization header value.
        """
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the Flask request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user object.
        """
        # Implement the logic to retrieve the current user based on the request.
        # For now, return None as specified in the task.
        return None
