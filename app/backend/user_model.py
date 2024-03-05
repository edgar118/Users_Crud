
from sqlalchemy import Column, String, Integer
from backend.config import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    user_info = relationship(
        'UserInfo',
        back_populates='user'
    )