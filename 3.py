#!/usr/bin/python
# -*- coding:utf-8
from HTMLParser import HTMLParser
import re
import urllib2

class A(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.str=""
		self.lnk=""
		self.base=[]
		self.body=True
		self.script=False
	def handle_data(self,data):
		if self.body and not(self.script):
			self.str+=data
#		if self.lnk and
			if re.search(u"\.m3u",data):
				self.base.append((data,self.lnk))
#			print data
#			print self.lnk
	def handle_starttag(self,tag,atr):
		if tag=="script":
			self.script=True
		if tag=="body":
			self.body=True
		if tag=="meta":
			for  i in atr:
				if i[0]=="content":
					print "!!!!!!!!!! charset:"+ i[1]
		if tag=="br":
			self.str+="\n"
		if tag=="a":
			for i in atr:
				if i[0]=="href":
					self.lnk=i[1]
#		print tag
#			print  self.lnk #atr[0][1]
	def handle_endtag(self,tag):
		if tag=="script":
			self.script=False
		if tag=="body":
			self.body=False
		if tag=="p":
			self.str+="\n"
		if tag=="a":
			self.lnk=""		
#			print tag+"1111"
			pass

#URL="http://hdbox.ws/news/43-ip-tv-kanaly.html"
URL="http://vk.com/club42797884"
z=re.split("/",URL)
BASE=z[0]+"//"+z[2]
#f=open("1.html","r")
f=urllib2.urlopen(URL)
print f.getcode()
html=f.read()
#print html
#html=html.decode('CP1251')
#html=html.decode('UTF8')
#html=re.sub("["+chr(0xd0)+chr(0xbf)+chr(0xbb)+"]","",html)
#print html
f.close()
f1=open("33.html","wb")
f1.write(html)
f1.close()

a=A()
a.feed(html)
print a.str
print a.base

z= re.split("/",'http://hdbox.ws/engine/download.php?id=35')
print z[0]+"//"+z[2]

for i in a.base:
	a=i[1]
	if re.split("/",a)[0]!="http:":
		a=BASE+a
	f=urllib2.urlopen(a)
	h=f.read()
	f.close()
	print h
