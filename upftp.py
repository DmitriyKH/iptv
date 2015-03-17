#!/usr/bin/python
import ftplib

name = "1.m3u"
ftp = ftplib.FTP("ftp.byethost7.com","b7_15986450","tuzikpuzik",timeout=5)
ftp.cwd("/htdocs")
f=open(name,"r")
ftp.storlines("STOR " + name,f)
f.close()
ftp.dir()
ftp.close()

