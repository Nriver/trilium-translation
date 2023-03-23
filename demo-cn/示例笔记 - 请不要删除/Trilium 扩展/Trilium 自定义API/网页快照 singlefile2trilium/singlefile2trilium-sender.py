#!/usr/bin/python3

# HowTo:
#  1- Put this file somewhere on your computer (needs python3).
#  2- Change `BASEDIR` and `TRILIUM_URL` vars as needed.
#  3- Make it run at session startup as a daemon
#       (https://smallbusiness.chron.com/run-command-startup-linux-27796.html)

import os
import pathlib
import time
import requests

BASEDIR = "~/下载"
TRILIUM_URL = "http://127.0.0.1:37840/custom/singlefile2trilium"
SECRET_PASSWORD = '你的密码'

path = pathlib.Path(BASEDIR).expanduser().absolute()

assert path.is_dir()
os.chdir(path)
mtime = path.stat().st_mtime

def log(msg):
    print(msg)

    if msg.startswith("[-] "):
        icon = "dialog-error"
    else:
        icon = "dialog-information"
    os.system("notify-send `hostname` %r --icon=%s" % (msg[4:], icon))

while True:
    time.sleep(0.3)
    new_mtime = path.stat().st_mtime

    if new_mtime <= mtime:
        continue

    for fname in os.listdir():
        if not fname.endswith(".html"):
            continue
        if not os.path.isfile(fname):
            continue
        if os.stat(fname).st_mtime <= mtime:
            continue

        with open(fname) as fd:
            head = fd.read(4096)

        idx = head.find("Page saved with SingleFile")
        if idx == -1:
            continue

        url = None
        title = None
        for line in head.splitlines():
            line = line.strip()
            if url is None and line.startswith("url: "):
                url = line[5:]
            elif line.startswith("title: "):
                title = line[7:]

        if url is None:
            continue
        if title is None:
            title = fname[:-5] # filename without '.html' suffix

        with open(fname) as fd:
            content = fd.read()

        try:
            resp = requests.post(TRILIUM_URL,
                    json={
                        "secret": SECRET_PASSWORD,
                        "title": title,
                        "url": url,
                        "content": content
                        }
                    )
            # remove file if transfer succeeded
            os.unlink(fname)
            log("[+] moved %r to trilium" % fname)
        except:
            log("[-] failed moving %r to trilium" % fname)

        mtime = new_mtime