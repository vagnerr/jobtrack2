from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from .meta import Base


class JobType(Base):
    """ The SQLAlchemy declarative model class for a JobType object.
        Ie. Contract/Perminent"""
    __tablename__ = 'jobtype'
    id = Column(Integer, primary_key=True)
    keyword = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_jobtypes')