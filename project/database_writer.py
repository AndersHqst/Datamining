import psycopg2

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
        cursor.execute(self.create_insert_statement(attributes))

    def create_insert_statement(self, attributes):
        keys = []
        values = []
        for key, value in attributes.iteritems()
            keys.append(key)
            values.append(value)

        # Quick and dirty, but I guess we don't care about robustness
        statement = 'INSERT INTO ' + 
            self.table_name + ' (' + 
            ', '.join(keys) + ') VALUES (' +
            ', '.join(values) + ');'
