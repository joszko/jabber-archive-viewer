# viewer displays the content of Cisco Jabber's archive in the webbrowser

import os
import sqlite3
import glob
import time
import webbrowser

# getting location of the message archive database
profile = os.environ['USERPROFILE']
path = r'\AppData\Local\Cisco\Unified Communications\Jabber\CSF\History'

os.chdir(profile + path)

# os.chdir(r'C:\Users\u8008701\Desktop\test')

time_formatting = '<span style="font-family:Segoe UI;color:#000000;font-size:10pt;font-weight:bold;font-style:normal' \
                  ';text-decoration:none;"> '

date_separator_formatting = '<div><span style="font-family:Segoe ' \
                            'UI;color:#000000;font-size:12pt;font-weight:bolder;font-style:normal;text-decoration' \
                            ':none;"> '

sender_formatting = '<span style="font-family:Segoe UI;color:#000000;font-size:10pt;font-weight:bold;font-style' \
                    ':normal;text-decoration:none;"> '

header = '<!doctype html><html lang="en"><head><meta charset="utf-16"><title>Your Cisco Jabber ' \
         'Archive</title></head><body> '

footer = '</body></html>'

# checking if the 'full archive' file exists - it's being created when the archive_recorder tool is being run.
if os.path.isfile('full_archive.db'):
    file = 'full_archive.db'
else:
    file = glob.glob("*[@]*.db")

# getting the contents of the database
conn = sqlite3.connect(file)
cur = conn.cursor()
cur.execute("SELECT date, payload, sender FROM history_message ORDER BY date DESC")
rows = cur.fetchall()
conn.close()

# creating archive.html file with the date, sender and message.
# html code of the message is being modified so it will look prettier.
# this file once created will be open by web browser
with open('archive.html', 'wb') as html:
    html.write(header.encode('UTF-16'))
    date_check = None
    for row in rows:
        date_separator = date_separator_formatting + time.strftime("%a, %d %b %Y", time.localtime(int(row[0] / 1000000))) + '<span></div><hr/>'

        if date_check != time.strftime("%a, %d %b %Y", time.localtime(int(row[0] / 1000000))):
            html.write(date_separator.encode('UTF-16'))

        time_string = time.strftime("%H:%M:%S", time.localtime(int(row[0] / 1000000)))

        message = row[1].replace('<div>', '').replace('</div>', '')

        sender_string = row[2][:-19].replace('.', ' ').title()

        sender = sender_formatting + ' ' + sender_string + ' </span>'

        full_line = '<div>' + time_formatting + time_string + ' - </span> ' + sender + ' - ' + message + '</div>' + '\n '

        html.write(full_line.encode('UTF-16'))

        date_check = time.strftime("%a, %d %b %Y", time.localtime(int(row[0] / 1000000)))

    html.write(footer.encode('UTF-16'))

url = profile + path + '\\' + 'archive.html'
# url = 'archive.html'
webbrowser.open_new_tab(url)
