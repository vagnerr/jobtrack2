from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship

from .meta import Base


class JobNote(Base):
    """ The SQLAlchemy declarative model class for a Jobnote object.
        This is for making notes about the particular job"""
    __tablename__ = 'jobnote'
    id = Column(Integer, primary_key=True)
    adddate = Column(DateTime, nullable=False)
    data = Column(Text, nullable=False)

    job_id = Column(ForeignKey('job.id'), nullable=False)
    job = relationship('Job', backref='job_notes')
    agent_id = Column(ForeignKey('agent.id'), nullable=True) # Not all jobs/notes have an agent
    agent = relationship('Agent', backref='job_notes')

    #"New" Fields added for V2
    deleted = Column(Boolean(create_constraint=False))  # delete note. hide from interface before ultimately purging them.
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_notes')