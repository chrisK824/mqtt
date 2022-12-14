import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists cpu ;
create table cpu (
  seq integer primary key autoincrement,
  Timestamp text,
  Value float
);

drop table if exists netDownloadBandwidth ;
create table netDownloadBandwidth (
  seq integer primary key autoincrement,
  Timestamp text,
  Value float
);

drop table if exists netUploadBandwidth ;
create table netUploadBandwidth (
  seq integer primary key autoincrement,
  Timestamp text,
  Value float
);

drop table if exists ram ;
create table ram (
  seq integer primary key autoincrement,
  Timestamp text,
  Value float
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
