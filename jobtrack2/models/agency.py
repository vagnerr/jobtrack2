from sqlathanor import (
    Column,
    Table,
)

from sqlalchemy import(
    ForeignKey,
    Integer,
    Text,
    Boolean,
)


from sqlathanor import relationship


from .meta import Base


class Agency(Base):
    """ The SQLAlchemy declarative model class for a Agency object."""
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True, autoincrement=True, supports_dict = True,)
    name = Column(Text, nullable=False, unique=True, supports_dict = True,)

    #"New" Fields added for V2
    creator_id = Column(ForeignKey('users.id'), nullable=False, supports_dict = True,) # Everything will have a creator
    creator = relationship('User', backref='created_agencies')