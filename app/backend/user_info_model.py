
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.config import Base

class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

    # Relationships
    user_id = Column(
        Integer, ForeignKey('user.id'), index=True
    )
    user = relationship(
        'User', foreign_keys=[user_id]
    )
