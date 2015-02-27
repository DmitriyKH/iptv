#!/usr/bin/python
# -*- coding: utf-8
import pickle
import sys
import re
class URL:
	def __init__(self,url):
		self.m_url=url
		self.m_count=0


class Chanel:
	def __init__(self):
		self.m_name=''
		self.m_url=[URL("")]
		self.m_group=''
		self.m_id=0


g_base_name_file="base.db"
g_playlist_name="1.m3u"
g_Base = []
g_flag=""

def loadBase():
	try:
		f=open(g_base_name_file,"rb")
		g_Base=pickle.load(f)
		f.close()
		print ("Base Loaded")
	except:
		print ("empty")

def saveBase():
	try:
		f=open(g_base_name_file,"wb")
		pickle.dump(g_Base,f)
		f.close()
	except:
		print ("ERROR: Dont save Base")

def addToBase(name,url):
	for a in g_Base:
		if a.m_name == name:
			if not(url in a.m_url):
				a.m_url.append(URL(url))
				return
	b = Chanel()
	b.m_name = name
	b.m_url=[URL(url)]
	g_Base.append(b)
	print ("GBase count: " + str(len(g_Base)))

def scan():
	global g_flag
	global g_playlist_name
	if g_flag != "new":
		loadBase()
	try:
		f=open(g_playlist_name,"r")
		l=f.readlines()
		f.close()
		n=0
		max_ = len(l) 
		while n < max_ :
			i = l[n]
			if re.match(r"#EXTINF",i):
				n+=1
				url=l[n]
				if re.match(r"#",url):
					continue
				while re.match("[\s]{1,}",url):
					n+=1
					url=l[n]
				s=re.split(",",i)
				name = s[1]			
				print("%d:%s url:%s" % (n,name,url))
				addToBase(name,url)
			elif re.match(r"#EXT-X-",i):
				print("ERROR: find new tag %s", i)
			n+=1
	except:
		print ("ERROR: File %s not exist" % name)

	if len(g_Base) > 0:
		saveBase()

def main():
	print ("******************************")
	print ("IPTV chanal validater ")
	print ("params: scan заполнение базы по mзu листам")
	print ("example:")
	print ("	lnx>$2.py scan")

	global g_flag
	global g_playlist_name

	mode="scan"

	try:
		if sys.argv[1] =="scan":
			mode="scan"
			if sys.argv[2]=='new':
				g_flag="new"
			else:
				g_playlist_name = sys.argv[2]		
	except:		
		pass 	
	if mode=="scan":
		scan()

main()	

