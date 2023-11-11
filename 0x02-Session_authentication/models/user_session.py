#!/usr/bin/env python3
"""
UserSession module.
"""
from models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class UserSession(Base):
    """ UserSession class.
    """

    __tablename__ = 'user_sessions'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False, unique=True)
    user = relationship('User', back_populates='user_sessions')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
