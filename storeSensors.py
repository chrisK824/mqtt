import json
import sqlite3

DB_Name = "IoT.db"


class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.conn.close()


def storeData(table, dataDict):
    timestamp = dataDict['timestamp']
    value = float(dataDict['val'])
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record(
        "insert into " + table + " (Timestamp, Value) values (?,?)", [timestamp, value])
    del dbObj


def payloadHandler(topic, data):
    table = topic.split('/')[-1]
    dataDict = json.loads(data)
    storeData(table, dataDict)
