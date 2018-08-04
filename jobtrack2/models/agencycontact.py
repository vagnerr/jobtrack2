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

class AgencyContact(Base):
    """ The SQLAlchemy declarative model class for a AgencyContact object."""
    __tablename__ = 'agencycontact'
    id = Column(Integer, primary_key=True)
    #keyword = Column(Text)

    data = Column(Text)

    agency_id = Column(ForeignKey('agency.id'), nullable=True) # don't always have an agency upfront
    agency = relationship('Agency', backref='contacts')

    contacttype_id = Column(ForeignKey('contacttype.id'), nullable=False) # don't always have an agency upfront
    contacttype = relationship('ContactType')   #, backref='agencycontacts'
