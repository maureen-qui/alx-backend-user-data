#!/usr/bin/env python3
"""
Session Expiration Authentication module.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Class to manage the API authentication with expiration.
    """

    def __init__(self):
        """ Initialize SessionExpAuth.
        """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ Create a Session ID with expiration.
        """
        session_id = super().create_session(user_id)

        if session_id:
            session_dict = {
                "user_id": user_id,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user_id for Session ID with expiration.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        user_id = session_dict.get('user_id')

        if self.session_duration <= 0:
            return user_id

        created_at_str = session_dict.get('created_at')

        if not created_at_str:
            return None

        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return user_id
