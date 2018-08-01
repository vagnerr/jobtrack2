from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Status(Base):
    """ The SQLAlchemy declarative model class for a Status object.
        This is for the status of the job ( Open / Closed / Rejected ... etc)"""
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    keyword = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)

    #"New" Fields added for V2

    # for c_c=false see -> https://bitbucket.org/zzzeek/sqlalchemy/issues/3067/naming-convention-exception-for-boolean
    active = Column(Boolean(create_constraint=False), default=True)  # Mark if this state signifies an open active job

    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_status')