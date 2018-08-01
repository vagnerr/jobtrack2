from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Location(Base):
    """ The SQLAlchemy declarative model class for a Location object.
        Where is the job usually abstract, eg London/Reading etc"""
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False, unique=True)

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_locations')