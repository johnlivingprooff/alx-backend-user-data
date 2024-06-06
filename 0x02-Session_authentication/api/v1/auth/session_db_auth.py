#!/usr/bin/env python3
"""Session DB Auth Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from typing import TypeVar
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth class"""
    def create_session(self, user_id: str = None) -> str:
        """Create session method"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """User ID for session ID method"""
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at is None:
            return None
        if (user_session.created_at + timedelta(
                                                seconds=self.session_duration
                                                ) < datetime.now()):
            return None
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy session method"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
