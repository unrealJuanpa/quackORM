import mysql.connector

"""
Quack ORM agrega automaticamente un campo ID como entero autonumerico a cada tabla
tambien agrega los campos createdAt y updatedAt
"""

class quackTable(object):
    def __init__(self) -> None:
        pass

class quackDataTypes:
    def String(primaryKey:bool=False, required:bool=False):
        ret = 'TEXT'
        required = (required or primaryKey)
        if primaryKey: ret += ' PRIMARY KEY'
        if required: ret += ' NOT NULL'
        return ret
    
    def Int(primaryKey:bool=False, autoIncrement:bool=False, required:bool=False):
        ret = 'INT'
        required = (required or primaryKey)
        if primaryKey: ret += ' PRIMARY KEY'
        if autoIncrement: ret += ' AUTO_INCREMENT'
        if required: ret += ' NOT NULL'
        return ret
    
    def Float(intDigits:int=10, decDigits:int=2, required:bool=False):
        ret = f'DECIMAL({intDigits},{decDigits})'
        if required: ret += ' NOT NULL'
        return ret

    def Bool(required:bool=False):
        ret = 'BOOLEAN'
        if required: ret += ' NOT NULL'
        return ret
    
    def Date(primaryKey:bool=False, required:bool=False):
        ret = 'DATE'
        required = (required or primaryKey)
        if primaryKey: ret += ' PRIMARY KEY'
        if required: ret += ' NOT NULL'
        return ret

    def DateTime(primaryKey:bool=False, required:bool=False):
        ret = 'DATETIME'
        required = (required or primaryKey)
        if primaryKey: ret += ' PRIMARY KEY'
        if required: ret += ' NOT NULL'
        return ret
    
    def Time(primaryKey:bool=False, required:bool=False):
        ret = 'TIME'
        required = (required or primaryKey)
        if primaryKey: ret += ' PRIMARY KEY'
        if required: ret += ' NOT NULL'
        return ret
    

class quack(object):
    def __init__(self, dbtype:str, dbname:str, dropDBOnMigrate:bool, host='localhost', user='root', password='') -> None:
        assert dbname != 'sys' and dbname != 'mysql' and dbname != "information_schema', 'The database can't be a mysql database"
        self.dbtype = dbtype
        self.dbname = dbname
        self.dropDBOnMigrate = dropDBOnMigrate

        if dbtype == 'mysql':
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
        elif False:
            pass

    def executeAndFetch(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        ret = []
        for d in data:
            ret.append(d)
        return ret
    
    def migrate(self, *args):
        # strongTables = [c for c in args if len(c.__bases__) == 1]
        # weakTables = [c for c in args if len(c.__bases__) != 1]

        print(f'Tables to migrate: {len(args)}')
        args = sorted(args, key = lambda x: len(x.__bases__)) 

        sqlquery = ''

        if self.dropDBOnMigrate:
            print('Dropping previous database if exists...')
            sqlquery += f'DROP DATABASE IF EXISTS {self.dbname};\n'
            sqlquery += f'CREATE DATABASE {self.dbname};\n'

        print('Trying to migrate structure to database...')
        sqlquery += f'USE {self.dbname};\n'

        for i in range(len(args)):
            tableparams = [c for c in dir(args[i]()) if not c.startswith('__')]
            tableparams = ',\n    '.join([f'{c} {getattr(args[i](), c)}' for c in tableparams])

            fk = args[i].__bases__[:-1]
            fk = ',\n    '.join([f'id{c.__name__.capitalize()}Fk INT NOT NULL,\n    FOREIGN KEY(id{c.__name__.capitalize()}Fk) REFERENCES {c.__name__}(id{c.__name__.capitalize()})' for c in fk])
            if len(fk) > 1:
                fk = '\n    ' + fk + ','

            sqlquery += f'''
            CREATE TABLE {args[i].__name__} (
                id{args[i].__name__.capitalize()} INT AUTO_INCREMENT NOT NULL,
                {str(tableparams)},{fk}
                PRIMARY KEY(id{args[i].__name__.capitalize()})
            );
            '''.replace('            ', '')

        
        self.executeAndFetch(sqlquery)
        print('Migration finished.')