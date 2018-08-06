from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
    DateTime,
    Table,

)
from sqlalchemy.orm import relationship

from .meta import Base

class AgentContact(Base):
    """ The SQLAlchemy declarative model class for a AgentContact object."""
    __tablename__ = 'agentcontact'
    id = Column(Integer, primary_key=True)
    #keyword = Column(Text)

    agent_id = Column(ForeignKey('agent.id'), nullable=True) # don't always have an agency upfront
    agent = relationship('Agent', backref='contacts')

    data = Column(Text)

    contacttype_id = Column(ForeignKey('contacttype.id'), nullable=False) # don't always have an agency upfront
    contacttype = relationship('ContactType')   #, backref='agentcontacts'
