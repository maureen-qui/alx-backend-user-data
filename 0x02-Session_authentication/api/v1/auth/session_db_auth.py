#!/usr/bin/env python3
"""
Session DB Authentication module.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Class to manage the API authentication with Session ID in the database.
    """

    def create_session(self, user_id=None):
        """ Create a Session ID and store it in the database.
        """
        session_id = super().create_session(user_id)

        if session_id:
            session_obj = UserSession(user_id=user_id, session_id=session_id)
            session_obj.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user_id for Session ID from the database.
        """
        if session_id is None:
            return None

        session_obj = UserSession.get(session_id)

        if session_obj:
            if self.session_duration <= 0:
                return session_obj.user_id

            if session_obj.created_at + timedelta(seconds=self.session_duration) >= datetime.utcnow():
                return session_obj.user_id

        return None

    def destroy_session(self, request=None):
        """ Destroy Session ID from the database.
        """
        if request and 'session_id' in request.cookies:
            session_id = request.cookies.get('session_id')
            session_obj = UserSession.get(session_id)

            if session_obj:
                session_obj.delete()
