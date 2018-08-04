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

class CompanyContact(Base):
    """ The SQLAlchemy declarative model class for a CompanyContact object."""
    __tablename__ = 'companycontact'
    id = Column(Integer, primary_key=True)
    #keyword = Column(Text)

    data = Column(Text)

    company_id = Column(ForeignKey('company.id'), nullable=False) # don't always have an agency upfront
    company = relationship('Company', backref='contacts')


    contacttype_id = Column(ForeignKey('contacttype.id'), nullable=False) # don't always have an agency upfront
    contacttype = relationship('ContactType')   #, backref='companycontacts'
