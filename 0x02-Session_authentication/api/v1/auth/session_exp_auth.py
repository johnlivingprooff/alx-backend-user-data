#!/usr/bin/env python3
""" Module of Session Exp Auth views"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class"""
    def __init__(self):
        """Constructor"""
        if getenv('SESSION_DURATION'):
            try:
                self.session_duration = int(getenv('SESSION_DURATION'))
            except Exception:
                self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create session method"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """User ID for session ID method"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict.get('created_at')
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None
        return session_dict.get('user_id')
