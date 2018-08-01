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
from .keyword import KeywordLink
from .agent import JobAgentLink

class Job(Base):
    """ The SQLAlchemy declarative model class for a Job object.
        Main job details."""
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    adddate = Column(DateTime, nullable=False)
    reference = Column(Text, nullable=False)
    changedate = Column(DateTime, nullable=False)

    nextaction_id = Column(ForeignKey('nextaction.id'), nullable=True)  # only time would be null is if the job has been closed
    nextaction = relationship('NextAction', backref='jobs')

    title = Column(Text, nullable=False)
    interviewdate = Column(DateTime, nullable=True)

    company_id = Column(ForeignKey('company.id'), nullable=True) # don't always know the company upfront
    company = relationship('Company', backref='jobs')

    location_id = Column(ForeignKey('location.id'), nullable=True) # don't always know the location upfront
    location = relationship('Location', backref='jobs')

    agency_id = Column(ForeignKey('agency.id'), nullable=True) # don't always have an agency upfront
    agency = relationship('Agency', backref='jobs')

    type_id = Column(ForeignKey('jobtype.id'), nullable=True) # don't always have an agency upfront
    jobtype = relationship('JobType', backref='jobs')

    salary = Column(Text, nullable=True)

    source_id = Column(ForeignKey('source.id'), nullable=True) # don't always have an agency upfront
    source = relationship('Source', backref='jobs')

    status_id = Column(ForeignKey('status.id'), nullable=True) # don't always have an agency upfront
    status = relationship('Status', backref='jobs')

    fake = Column(Boolean, nullable=False)

    #"New" Fields added for V2
    deleted = Column(Boolean)  # delete JOb. hide from interface before ultimately purging them. (NOTE That would need to kill the related data)
  #  creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
   # creator = relationship('User', backref='created_pages')

    # LNK table for keywords...
    #https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
    keywords = relationship('Keyword', secondary=KeywordLink, backref='job')

    agents = relationship('Agent', secondary=JobAgentLink, backref='job')
