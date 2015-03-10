#!/usr/bin/python
# -*- coding:utf-8
from HTMLParser import HTMLParser
import re

class A(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.str=""
		self.lnk=""
		self.base=[]
		self.body=True
	def handle_data(self,data):
		if self.body:
			self.str+=data
#		if self.lnk and
			if re.search(u"\.m3u",data):
				self.base.append((data,self.lnk))
#			print data
#			print self.lnk
	def handle_starttag(self,tag,atr):
		if tag=="script":
			self.body=False
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
			self.body=True
		if tag=="p":
			self.str+="\n"
		if tag=="a":
			self.lnk=""		
#			print tag+"1111"
			pass

f=open("2.html","r")
html=f.read()
html=html.decode('CP1251')
f.close()

a=A()
a.feed(html)
print a.str
print a.base

z= re.split("/",'http://hdbox.ws/engine/download.php?id=35')
print z[0]+"//"+z[2]
