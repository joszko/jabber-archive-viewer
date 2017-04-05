import urllib.request
import os
import sqlite3
import glob
import time
import tkinter as tk

from tkinterhtml import HtmlFrame

root = tk.Tk()
root.title("Jabber Archive Viewer")
profile = os.environ['USERPROFILE']
path = r'\AppData\Local\Cisco\Unified Communications\Jabber\CSF\History'

os.chdir(profile + path)

# os.chdir(r'C:\Users\u8008701\Desktop\test')

time_formatting = '<span style="font-family:Segoe UI;color:#000000;font-size:10pt;font-weight:normal;font-style' \
                  ':normal;text-decoration:none;"> '

for file in glob.glob("*.db"):
    conn = sqlite3.connect(file)
    cur = conn.cursor()
    cur.execute("SELECT date, payload, sender FROM history_message ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()

    with open('archive.html', 'wb') as html:
        for row in rows:
            time_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(int(row[0] / 1000000)))
            message = row[1].replace('<div>', '').replace('</div>', '')
            sender = time_formatting + ' ' + row[2] + ' </span>'
            full_line = '<div>' + time_formatting + time_string + ': </span> ' + sender + ' - ' + message + '</div>' + '\n '
            html.write(full_line.encode('UTF-16'))

frame = HtmlFrame(root, horizontal_scrollbar="auto")
frame.grid(sticky=tk.NSEW)

# url = r'C:\Users\u8008701\Desktop\test\test.html'
url = profile + path + '\\' + 'archive.html'
print(url)
frame.set_content(urllib.request.urlopen(r'file:///' + url).read().decode('utf-16'))
# print(frame.html.cget("zoom"))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()
