from sqlathanor  import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class MixJsonBase(object):
    # allow us to (via sqlathanor) automatically convert to JSON
    # in the auto JSON renderer We will only get a flat 1 level
    # result ( no fancy agent.agency.name ) but for basic ajax
    # calls that should be sufficient.
    # Yes: We are using to_dict, not to_json here because if
    # we don't then an array of items being returned gets
    # gets an additional string quotation layer added :-(
    def __json__(self, o):
        return self.to_dict()  #pylint: disable=E1101



metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
