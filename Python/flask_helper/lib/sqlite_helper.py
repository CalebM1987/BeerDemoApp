#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     03/12/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sqlite3
import datetime
import os

__all__ = ('SQLiteBase', 'SQLiteDB')

class SQLiteBase(sqlite3.Connection):
    PRIMARY_KEY_SCHEMA = '{} INTEGER PRIMARY KEY AUTOINCREMENT'
    def __init__(self, path):
        """represents a replica stored as a SQLite database, this should ALWAYS
        be used with a context manager.  For example:

            with SQLiteReplica(r'C:\TEMP\replica.geodatabase') as con:
                print con.list_tables()
                # do other stuff

        Required:
            path -- full path to .geodatabase file (SQLite database)
        """
        self.db = path
        super(SQLiteBase, self).__init__(self.db)
        self.cursor = self.cursor()
        self.isClosed = False

    def execute(self, sql, *args):
        """Executes an SQL query.  This method must be used via a "with" statement
        to ensure the cursor connection is closed.

        Required:
            sql -- sql statement to use

        >>> with restapi.SQLiteReplica(r'C:\Temp\test.geodatabase') as db:
        >>>     # now do a cursor using with statement
        >>>     with db.execute('SELECT * FROM Some_Table') as cur:
        >>>         for row in cur.fetchall():
        >>>             print(row)
        """
        return self.cursor.execute(sql, *args)


    def __safe_cleanup(self):
        """close connection and remove temporary .geodatabase file"""
        try:
            if not self.isClosed:
                self.cursor.close()
                self.close()
                self.isClosed = True
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__safe_cleanup()

    def __del__(self):
        self.__safe_cleanup()

class SQLiteDB(SQLiteBase):

    @classmethod
    def _form_primary_key(cls, name='Id'):
        return cls.PRIMARY_KEY_SCHEMA.format(name)

    def list_tables(self, filter_esri=True):
        """returns a list of tables found within sqlite table

        Optional:
            filter_esri -- filters out all the esri specific tables (GDB_*, ST_*), default is True.  If
                False, all tables will be listed.
        """
        tables = self.execute("select name from sqlite_master where type = 'table'").fetchall()
        if filter_esri:
            return [t[0] for t in tables if not any([t[0].startswith('st_'),
                                                     t[0].startswith('GDB_'),
                                                     t[0].startswith('sqlite_')])]
        else:
            return [t[0] for t in tables]

    def list_fields(self, table_name):
        """lists fields within a table, returns a list of tuples with the following attributes:

        cid         name        type        notnull     dflt_value  pk
        ----------  ----------  ----------  ----------  ----------  ----------
        0           id          integer     99                      1
        1           name                    0                       0

        Required:
            table_name -- name of table to get field list from
        """
        return self.execute('PRAGMA table_info({})'.format(table_name)).fetchall()

    def delete_table(self, table_name):
        self.execute('DROP TABLE IF EXISTS {}'.format(table_name))

    def create_table(self, table_name, schema, overwrite=False, add_primary_key=True, primary_key_name='OID'):
        if add_primary_key:
            schema = ','.join([self._form_primary_key(primary_key_name), schema])
        if table_name in self.list_tables():
            if overwrite:
                self.delete_table(table_name)
                self.execute('''CREATE TABLE IF NOT EXISTS {t} ({s})'''.format(t=table_name, s=schema))
        else:
             self.execute('''CREATE TABLE IF NOT EXISTS {t} ({s})'''.format(t=table_name, s=schema))

        return SQLiteTable(self, table_name)

    def get_table(self, table_name):
        return SQLiteTable(self, table_name)

    def clear_rows(self, table_name):
        """clears all rows in a table

        Required:
            table_name -- name of table to clear out rows
        """
        self.execute('DELETE FROM {}'.format(table_name))
        self.execute('VACUUM')

    def raw_query(self, table_name, fields='*', where=''):
        """performs a search cursor on a table

        Required:
            db_name -- database name
            table_name -- name of table

        Optional:
            fields -- list of field names to grab, default is "*"
            where -- where clause
            schema -- schema type (default is "dbo")
        """
        if isinstance(fields, list):
            fields = ','.join(fields)

        sql = 'SELECT {} FROM {}'.format(fields, table_name)
        if where:
            where = ' WHERE ' + where
        return self.execute(sql + where or '')

    def query(self, table_name, fields='*', where=''):
        """performs a search cursor on a table

        Required:
            db_name -- database name
            table_name -- name of table

        Optional:
            fields -- list of field names to grab, default is "*"
            where -- where clause
            schema -- schema type (default is "dbo")
        """
        rows = self.raw_query(table_name, fields, where)
        isExhausted = False
        while not isExhausted:
            try:
                row = rows.fetchone()
                isExhausted = row == None
                if row:
                    yield row
            except StopIteration:
                isExhausted = True

    def __repr__(self):
        return '<SQLite Database: "{}">'.format(os.path.basename(self.db))


class SQLiteTable(object):
    def __init__(self, database, table_name, autocommit=True):
        self.db = database
        self.table_name = table_name
        self.autocommit = autocommit
        self.fieldCache = [f[1] for f in self.list_fields()]

    @property
    def primaryKey(self):
        try:
            return [f[1] for f in self.list_fields() if f[-1]][0]
        except IndexError:
            return None

    @property
    def editableFields(self):
        return [f[1] for f in self.list_fields() if f[1] != self.primaryKey]

    @property
    def editableFieldObjects(self):
        return [f for f in self.list_fields() if f[1] != self.primaryKey]

    @property
    def defaultValues(self):
        #return [f[-2] if f[-2] is not None else 'NULL' for f in self.editableFieldObjects]
        return [f[-2] for f in self.editableFieldObjects]

    @property
    def editableFeldIndices(self):
        return {f:i for i,f in enumerate(self.editableFields)}

    @staticmethod
    def format_date(d=None):
        if not d:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(d, datetime.datetime):
            return d.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return d

    def list_fields(self):
        fields = self.db.list_fields(self.table_name)
        self.fieldCache = [f[1] for f in fields]
        return fields

    def add_field(self, name, ftype):
        self.db.execute('ALTER TABLE {} ADD COLUMN {} {}'.format(self.table_name, name, ftype))

    def insert(self, *args, **kwargs):
        defaults = self.defaultValues
        fi = self.editableFeldIndices
        field_names = self.editableFields
        for i,arg in enumerate(args):
            defaults[i] = arg
        for f,val in kwargs.iteritems():
            if f in field_names:
                defaults[fi[f]] = val

        qs = ', '.join(['?'] * len(defaults))
        sql = 'INSERT INTO {} {} VALUES({})'.format(self.table_name, str(tuple(map(str, field_names))), qs)
        self.db.execute(sql, tuple(defaults))
        if self.autocommit:
            self.db.commit()

    def update(self, where, **kwargs):
        #updates = ['{} = {}'.format(k, "'"+ v +"'" if isinstance(v, basestring) else v) for k,v in kwargs.iteritems()]
        updates = []
        for k,v in kwargs.iteritems():
            if v is None:
                updates.append('{} = null'.format(k))
            elif isinstance(v, basestring):
                updates.append("{} = '{}'".format(k, v))
            else:
                updates.append('{} = {}'.format(k, v))
        sql = "UPDATE {} SET {} WHERE {}".format(self.table_name, ', '.join(updates), where)
        self.db.execute(sql)
        if self.autocommit:
            self.db.commit()

    def delete(self, where=''):
        """delete records

        Optional:
            where -- where clause for delete

        example. Delete everything older than a day:
            where = "date(End_Time) > date('now', '-1 days')"
        """
        if where:
            where = ' WHERE ' + where
        self.db.execute('DELETE FROM {}'.format(self.table_name) + where or '')
        if self.autocommit:
            self.db.commit()

    def raw_query(self, fields='*', where=''):
        return self.db.raw_query(self.table_name, fields, where)

    def query(self, fields='*', where=''):
        if isinstance(fields, list):
            fields = ','.join(fields)
        return self.db.query(self.table_name, fields, where)

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return '<SQLite Table "{}" from Database: "{}">'.format(self.table_name, os.path.basename(self.db.db))