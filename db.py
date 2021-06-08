import os
import sqlite3

from datetime import datetime
from datetime import timedelta
## database code
cwd = os.getcwd()
DB_NAME = "schedule.db"
def make_connection():
  con = None
  try:
    con = sqlite3.connect(os.path.join(cwd, DB_NAME))
  except sqlite3.Error as e:
    print(e)
  return con
  
def edit_entry(con, dt_object, task):
  cur = con.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS Schedules (
    id       INTEGER PRIMARY KEY,
    year     INTEGER NOT NULL,
    month    INTEGER NOT NULL,
    day      INTEGER NOT NULL,
    hour     INTEGER NOT NULL,
    minute   INTEGER NOT NULL,
    task     TEXT NOT NULL
  );""")

  cur.execute("INSERT INTO Schedules(year, month, day, hour, minute, task) VALUES(?,?,?,?,?,?)", (dt_object.year,dt_object.month, dt_object.day, dt_object.hour, dt_object.minute, task))
  return

def row_to_strp(row):
  if len(row) != 7:
    raise ValueError("The given row is not properly formatted")
  year = row[1]
  month = row[2]
  day = row[3]
  hour = row[4]
  minute = row[5]
  return datetime.strp(f"{year}-{month}-{day} {hour}:{minute}", "%YYYY-%mm-%DD %HH:%MM")

# def has_conflicts(dt_object):
#   con = make_connection()
#   with con:
#     cur = con.cursor()
#     for row in cur.execute("SELECT * FROM Schedules ORDER BY year, month, day, hour minute;"):
#       row_dt = row_to_strp(row)
#       if (dt_object - row_dt).days <= -1:
#         return True
#       elif ()
      