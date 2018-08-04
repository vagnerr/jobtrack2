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
    Column('primary', Boolean(create_constraint=False), nullable=True)
)


class Agent(Base):
    """ The SQLAlchemy declarative model class for a Agent object."""
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    agency_id = Column(ForeignKey('agency.id'), nullable=True) # Solo "agents"
    agency = relationship('Agency', backref='agents')

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_agents')

    jobs = relationship('Job', secondary=JobAgentLink, backref='agent')