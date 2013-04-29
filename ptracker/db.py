from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, String
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
def init(user, password, name):
    if user is None:
        raise Exception("You must supply a user")
    if password is None:
        raise Exception("You must supply a password")
    if name is None:
        raise Exception("You must supply a DB name")

    init.engine = create_engine('postgres://{0}:{1}@localhost/{2}'.format(user, password, name))
    Session.configure(bind=init.engine)
    

def setupdb():
    Base.metadata.drop_all(init.engine)
    Base.metadata.create_all(init.engine)
