import sqlite3
import uuid

from flask import g

import config
configInstance = config.Config()

class CalendarRepo(object):
    def __name__(self):
        return 'calendarRepo'

    def __init__(self):
        self.table_name = configInstance.TABLE_NAME
        self.database_name =  configInstance.DATABASE_NAME

    def _init(self):
        self.connection = getattr(g, '_database', None)
        if self.connection is None:
            self.connection = g._database = sqlite3.connect(self.database_name)

        self.cursor = self.connection.cursor()

        if self.checkTableExists() is False:
            self.createTable()

    def _del(self, self_from_caller):
        self.connection = getattr(g, '_database', None)
        if self.connection is not None:
            self.connection.close()

    def createTable(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS {0}
                          (
                           guid UNIQUEIDENTIFIER,
                           title STRING,
                           year SHORT,
                           month SHORT,
                           day SHORT,
                           hour SHORT,
                           minute SHORT
                           )""".format(self.table_name)

        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def insertRow(self, title, year, month, day, hour, minute):
        guid = uuid.uuid4()
        self.cursor.execute("""INSERT INTO calendar
                               (guid, title, year, month, day, hour, minute)
                               VALUES('{0}', '{1}', {2}, {3}, {4}, {5}, {6})
                            """.format(guid, title, year, month, day, hour, minute))
        self.connection.commit()
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
        self.connection.commit()

    def deleteRow(self, guid):
        self.cursor.execute("""DELETE FROM calendar
                               WHERE guid = '{}';
                            """.format(guid))
        self.connection.commit()

    def getRecordsByYearAndMonth(self, year, month):
        self.cursor.execute(
            'SELECT * FROM calendar WHERE year={} AND month={}'.format(year, month))
        return self.cursor.fetchall()

    def getRecordById(self, guid):
        self.cursor.execute(
            'SELECT * FROM calendar WHERE guid="{}"'.format(guid))
        return self.cursor.fetchone()

    def getAll(self):
        self.cursor.execute('SELECT * FROM calendar')
        return self.cursor.fetchall()

    def checkTableExists(self):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(self.table_name))
        data = self.cursor.fetchall()
        if len(data) == 0:
            print('There is no table named: {}'.format('calendar'))
            return False
        else:
            return True
