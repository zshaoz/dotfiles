import arrow
import tornado.gen
import momoko
import pdb

class Store(object):

    @tornado.gen.coroutine
    def establish_database_connection(self, dbname, user, password, host, port):
        connection_string = "dbname={0} user={1} password={2} host={3} port={4}".format(dbname, user, password, host, port)
        conn = momoko.Connection(dsn=connection_string)
        conn = yield conn.connect()
        self.conn = conn

    @tornado.gen.coroutine
    def execute_sql_statement_with_fetch(self, statement):
        cursor = yield self.conn.execute(statement)
        return cursor.fetchall()

    @tornado.gen.coroutine
    def execute_sql_statement(self, statement):
        cursor = yield self.conn.execute(statement)

    @tornado.gen.coroutine
    def pg_select_all_from(self, table, conditions=[], order_by=None, sort_order="DESC", limit=None, offset=None):
        statement = "SELECT * FROM {0}\n".format(table)
        if conditions:
            statement += "WHERE "
            statement += " AND\n".join(conditions)
            statement += "\n"
        if order_by is not None:
            order_by = '"' + order_by + '"'
            statement += "ORDER BY {0} {1}\n".format(order_by, sort_order)
        if limit is not None:
            statement += "LIMIT {0}\n".format(limit)
        if offset is not None:
            statement += "OFFSET {0}\n".format(offset)
        statement += ";"
        results = yield self.execute_sql_statement_with_fetch(statement)
        return results

    @tornado.gen.coroutine
    def pg_select_columns_from(self, table, columns=[], conditions=[], order_by=None, sort_order="DESC", limit=None, offset=None):
        statement = "SELECT "
        if columns:
            statement += ", ".join(columns)
        statement += " FROM {0}\n".format(table)
        if conditions:
            statement += "WHERE "
            statement += " AND\n".join(conditions)
            statement += "\n"
        if order_by is not None:
            order_by = '"' + order_by + '"'
            statement += "ORDER BY {0} {1}\n".format(order_by, sort_order)
        if limit is not None:
            statement += "LIMIT {0}\n".format(limit)
        if offset is not None:
            statement += "OFFSET {0}\n".format(offset)
        statement += ";"
        results = yield self.execute_sql_statement_with_fetch(statement)
        return results

    @tornado.gen.coroutine
    def pg_update_all(self, table, columns=[], values=[], conditions=[]):
        statement = "UPDATE {0} SET (\n".format(table)
        statement += ",\n".join(columns)
        statement += ") "
        statement += "= (\n"
        statement += ",\n".join(values)
        statement += ") "
        if conditions:
            statement += "WHERE "
            statement += " AND\n".join(conditions)
            statement += "\n"
        statement += ";"
        results = yield self.execute_sql_statement(statement)
        return results

    @tornado.gen.coroutine
    def pg_insert_into(self, table, columns=[], values=[]):
        statement = "INSERT INTO {0} (\n".format(table)
        statement += ",\n".join(columns)
        statement += ")\n"
        statement += "VALUES (\n"
        statement += ",\n".join(values)
        statement += ");"
        results = yield self.execute_sql_statement(statement)
        return results

    @tornado.gen.coroutine
    def pg_alter_column(self, table, column, column_definition):
        statement = "ALTER TABLE {0}\n".format(table)
        statement += "ALTER COLUMN {0} TYPE {1};".format(column, column_definition)
        results = yield self.execute_sql_statement(statement)
        return results





