from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('solvers/CFOP/cfop.db', pragmas={'journal_mode': 'wal'})


class F2lDb(Model):
    case = CharField(max_length=5, primary_key=True)
    alg = CharField(max_length=255)

    class Meta:
        database = db


db.create_tables([F2lDb])
