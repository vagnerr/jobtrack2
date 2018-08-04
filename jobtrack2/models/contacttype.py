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

class ContactType(Base):
    """ The SQLAlchemy declarative model class for a ContactType object.
        Arbritrary contact types eg Phone, Email, Webaddress etc.
        for detailing agency/agent/company"""
    __tablename__ = 'contacttype'
    id = Column(Integer, primary_key=True)
    keyword = Column(Text)
    description = Column(Text)

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
    creator = relationship('User', backref='created_contacttypes')
