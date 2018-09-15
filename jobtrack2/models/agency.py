from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Agency(Base):
    """ The SQLAlchemy declarative model class for a Agency object."""
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_agencies')