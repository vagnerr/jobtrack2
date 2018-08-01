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


class JobRelated(Base):
    """ The SQLAlchemy declarative model class for a JobRelated object.
        Allows linking of multiple jobs together for arbittrary reasons."""
    __tablename__ = 'jobrelated'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    parent_id = Column(ForeignKey('job.id'), nullable=False)
    parent = relationship('Job', backref='child_jobs')
    child_id = Column(ForeignKey('job.id'), nullable=False)
    child = relationship('Job', backref='parent_jobs')

    #"New" Fields added for V2
#    creator_id = Column(ForeignKey('users.id'), nullable=False) # Everything will have a creator
#    creator = relationship('User', backref='created_pages')