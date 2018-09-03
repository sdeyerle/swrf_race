from core import core
import sqlite3

conn = sqlite3.connect('swrf.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

race1 = core.Race(conn, 120)
boat1 = core.Boat(conn, 10)

race1.fetch()
boat1.fetch()
print(boat1)


