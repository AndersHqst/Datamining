import psycopg2

def create_insert_statement(table_name, attributes):
    keys = []
    values = []
    for key, value in attributes.iteritems():
        keys.append(key)
        values.append(value)

    # Quick and dirty, but I guess we don't care about robustness
    statement = 'INSERT INTO ' 
    statement += table_name + ' (' 
    statement += ', '.join(keys) + ') VALUES (' 
    statement += ', '.join([str(value) for value in values]) + ');'

    return statement

class DatabaseWriter:

    def __init__(self, connection_string, table_name):
        self.connection_string = connection_string
        self.table_name = table_name

    def connect(self):
        self.connection = psycopg2.connect(self.connection_string)

    def disconnect(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def write_row(self, attributes):
        cursor = self.connection.cursor()
        cursor.execute(create_insert_statement(self.table_name, attributes))

class TestDatabaseWriter:

    def __init__(self, connection_string, table_name, filename=None):
        self.connection_string = connection_string
        self.table_name = table_name
        if filename is None:
            self.filename = 'db_test_' + table_name + '.txt'
        else:
            self.filename = filename

        with open(self.filename, 'w'):
            pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def commit(self):
        pass

    def write_row(self, attributes):
        with open(self.filename, 'a') as f:
            f.write(create_insert_statement(self.table_name, attributes) + '\n')
