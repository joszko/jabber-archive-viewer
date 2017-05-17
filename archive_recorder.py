import sqlite3
import os

# The tool records the changes in Jabber's message history and save it in separate database.
# it was created due to the limitations of Jabber's archive which is storing limited number of messages per contact.
# it can be set to run by Task Scheduler

profile = os.environ['USERPROFILE']
path = r'\AppData\Local\Cisco\Unified Communications\Jabber\CSF\History'

os.chdir(profile + path)

# os.chdir(r'C:\Users\u8008701\Desktop\test')

# checking if the file with new database exists. If yes it will add new records to the 'full_archive' database.
# if no then the file will be created with new records
if os.path.isfile('full_archive.db'):

    conn = sqlite3.connect("full_archive.db")
    cur = conn.cursor()
    cur.execute("SELECT MAX(date) from history_message")
    maxdate = cur.fetchone()
    conn.close()

    maxdate_string = str(maxdate).replace('(', '').replace(')', '').replace(',', '')

    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("SELECT * from history_message WHERE date >" + maxdate_string)
    rows = cur.fetchall()
    conn.close()

    if len(rows) > 0:
        conn = sqlite3.connect("full_archive.db")
        cur = conn.cursor()
        cur.executemany("INSERT INTO history_message (id, type, payload, date, sender, item, label) values (?,?,?,?,"
                        "?,?,?)", rows)
        conn.commit()
        conn.close()

else:
    # if the file doesn't exist - create new one and load the contents of the archive
    conn = sqlite3.connect("full_archive.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history_message (id INTEGER, type INTEGER, payload CLOB, date INTEGER, "
                "sender TEXT, item INTEGER, label INTEGER)")
    conn.commit()
    conn.close()

    conn_base = sqlite3.connect('full_archive.db')
    c = conn_base.cursor()
    c.execute('ATTACH DATABASE ? as db2', ['test.db'])
    c.execute('SELECT date, payload, sender FROM history_message')
    c.execute('INSERT INTO history_message SELECT id,type,payload,date,sender,item,label FROM db2.history_message')
    conn_base.commit()
    conn_base.close()
