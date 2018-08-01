from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship

from .meta import Base

# https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
JobAgentLink = Table('jobagent_lnk', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('job_id', Integer, ForeignKey('job.id')),
    Column('agent_id', Integer, ForeignKey('agent.id')),
    Column('primary', Boolean, nullable=False)
)


class Agent(Base):
    """ The SQLAlchemy declarative model class for a Agent object.
        This is for the next action of the job ( Call/ email/ close etc)"""
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)

    #"New" Fields added for V2
    agency_id = Column(ForeignKey('agency.id'), nullable=True) # Solo "agents"
    agency = relationship('Agency', backref='agents')

    #"New" Fields added for V2
   # creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
   # creator = relationship('User', backref='created_pages')

    jobs = relationship('Job', secondary=JobAgentLink, backref='agent')