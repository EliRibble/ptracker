from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, String

def setupdb(user, password, name):
    if user is None:
        raise Exception("You must supply a user")
    if password is None:
        raise Exception("You must supply a password")
    if name is None:
        raise Exception("You must supply a DB name")

    engine = create_engine('postgres://{0}:{1}@localhost/{2}'.format(user, password, name), echo=True)
    
    metadata = MetaData()
    users = Table('users', metadata,
        Column('name', String(200), primary_key=True)
    )
    metadata.create_all(engine)
    


