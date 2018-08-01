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


# https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
KeywordLink = Table('keyword_lnk', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('job_id', Integer, ForeignKey('job.id')),
    Column('keyword_id', Integer, ForeignKey('keyword.id'))
    # Could add creator info here???
)

#class Item(Base):
#    __tablename__ = 'Item'
#    id = Column(Integer, primary_key=True)
#    name = Column(String(255))
#    description = Column(Text)
#    details = relationship('Detail', secondary=ItemDetail, backref='Item')

class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column(Text)
    jobs = relationship('Job', secondary=KeywordLink, backref='keyword')