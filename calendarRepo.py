import secrets
import pyodbc

# import sqlite3
import uuid

from flask import g

import config
configInstance = config.Config()

secrets = secrets.Config()

class CalendarRepo(object):
    def __name__(self):
        return 'calendarRepo'

    def __init__(self):
        self.odbc_connection = pyodbc.connect(
            driver='{SQL Server}',
            host='tcp:' + secrets.SERVER,
            database=secrets.DATABASE,
            trusted_connection='no',
            user=secrets.USERNAME,
            password=secrets.PASSWORD)
        
        self.table_name = configInstance.TABLE_NAME

        self.cursor = self.odbc_connection.cursor()

        if self.checkTableExists() is False:
            self.createTable()
        
        self.database_name = configInstance.DATABASE_NAME

    def _init(self):
        pass

    def _del(self, self_from_caller):
        pass

    def createTable(self):
        create_table_sql = '''if not exists (select * from sysobjects where name='{0}' and xtype='U')
                            CREATE TABLE {0} (
                                            guid varchar(255),
                                            title varchar(255),
                                            year INT,
                                            month INT,
                                            day INT,
                                            hour INT,
                                            minute INT
                                            )'''.format(self.table_name)

        self.cursor.execute(create_table_sql)
        self.odbc_connection.commit()

    def insertRow(self, title, year, month, day, hour, minute):
        guid = str(uuid.uuid4())
        self.cursor.execute("""INSERT INTO calendar
                               (guid, title, year, month, day, hour, minute)
                               VALUES('{0}', '{1}', {2}, {3}, {4}, {5}, {6})
                            """.format(guid, title, year, month, day, hour, minute))
        self.odbc_connection.commit()
        return guid

    def updateRow(self, guid, title, year, month, day, hour, minute):
        self.cursor.execute("""UPDATE calendar SET
                               title = '{0}',
                               year = '{1}',
                               month = '{2}',
                               day = '{3}',
                               hour = '{4}',
                               minute = '{5}'
                               WHERE guid = '{6}';
                            """.format(title, year, month, day, hour, minute, guid))
        self.odbc_connection.commit()

    def deleteRow(self, guid):
        self.cursor.execute("""DELETE FROM calendar
                               WHERE guid = '{}';
                            """.format(guid))
        self.odbc_connection.commit()

    def getRecordsByYearAndMonth(self, year, month):
        self.cursor.execute(
            'SELECT * FROM calendar WHERE year={} AND month={}'.format(year, month))
        return self.fetchAll()

    def getRecordById(self, guid):
        self.cursor.execute(
            'SELECT * FROM calendar WHERE guid="{}"'.format(guid))
        return self.fetchAll()[0]

    def getAll(self):
        self.cursor.execute('SELECT * FROM calendar')
        return self.fetchAll()

    def checkTableExists(self):
        self.cursor.execute("select * from sysobjects where name='{0}' and xtype='U'".format(self.table_name))
        data = self.fetchAll()
        if len(data) == 0:
            print('There is no table named: {}'.format('calendar'))
            return False
        else:
            return True
    
    def fetchAll(self):
        rows = []
        for row in self.cursor:
            rows.append(list(row))
        return rows
