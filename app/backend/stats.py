
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from backend.config import Base

class EndpointStats(Base):
    __tablename__ = "endpoint_stats"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    count = Column(Integer)
    total_time = Column(Float)
    location = Column(String)
    region = Column(String)
    country = Column(String)