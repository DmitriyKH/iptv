#!/usr/bin/python
# -*- coding: utf-8
import pickle
import sys
import re
class URL:
	def __init__(self):
		self.m_url=""
		self.m_count=0


class Chanel:
	def __init__(self):
		self.m_name=''
		self.m_url=[URL()]
		self.m_group=''
		self.m_id=0

g_base_name_file="base.db"
g_Base = [Chanel()]

def loadBase():
	try:
		f=open(g_base_name_file,"rb")
		g_Base=pickle.load(f)
		f.close()
		print ("Base Loaded")
	except:
		print "empty"

def saveBase():
	try:
		f=open(g_base_name_file,"wb")
		pickle.dump(g_Base,f)
		f.close()
	except:
		print ("ERROR: Dont save Base")

def scan():
	load=True
	try:
		if sys.argv[2]=="new":
			load=False
	except:
		pass
	if load:
		loadBase()
	
	try:
		name="1.m3u"
		f=open(name,"r")
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
				name = s[1] 
				print("%d:%s url:%s" % (n,name,url))
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
	mode="scan"
	try:
		if sys.argv[1] =="scan":
			mode="scan"
	except:
		pass 	
	if mode=="scan":
		scan()

main()	

#a=[AA()]
#a[0].m_name='name'
#a[0].m_url.append('http://127.0.0.1')
#a[0].m_group='default'

#f=open('tt.txt',"wb")

#pickle.dump(a,f)
#f.close()


