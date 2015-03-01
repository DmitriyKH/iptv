#!/usr/bin/python
# -*- coding: utf-8
import pickle
import sys
import re
import time
import vlc

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
g_playlist_name="edem.m3u"
g_Base = []
g_NoNameChanels=[]
g_flag=""

def loadBase():
	global g_Base
	try:
		f=open(g_base_name_file,"rb")
		g_Base=pickle.load(f)
		f.close()
		print ("Base Loaded")
	except:
		print ("empty")

def saveBase():
	global g_Base
	global g_NoNameList
	try:
		f=open(g_base_name_file,"wb")
		pickle.dump(g_Base,f)
		f.close()
	except:
		print ("ERROR: Dont save Base")

def addToBase(name,url):
	global g_Base
	global g_NoNameChanels

	if re.match(r"\s{1,}", name):
		print "!!!!! emptu name:" + url
		if not(url in g_NoNameChanels):
			g_NoNameChanels.append(url)
		return
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
				name = name.replace("\n","")
				name = name.replace("\r","")
				url = url.replace("\n","")
				url = url.replace("\r","")
				print("%d:%s url:%s" % (n,name,url))

				addToBase(name,url)
			elif re.match(r"#EXT-X-",i):
				print("ERROR: find new tag %s", i)
			n+=1
	except:
		print ("ERROR: File %s not exist" % g_playlist_name)

	if len(g_Base) > 0:
		saveBase()

def validate():
	global g_Base
	i = vlc.Instance()
	p = i.media_player_new()
#	p.set_mrl("http://en356.edem.tv/iptv/LYB72PLY6GB4KR/102/index.m3u8")
#	p.play()
#	time.sleep(5)	
#	p.set_mrl("http://en356.edem.tv/iptv/LYB72PLY6GB4KR/107/index.m3u8")
#	p.play()
#	time.sleep(5)
#	return	
	loadBase()
	
	for i in g_Base:
		for url in i.m_url:
			print url.m_url
			if not(re.match("rtmp:",url.m_url)):
				p.set_mrl(url.m_url)
				p.play()
				time.sleep(1)
				url.m_count=p.is_playing()
				print "play: "+str(p.is_playing())+" state: "+ str(p.get_state())
				p.stop()
	saveBase()

def genM3u():
	global g_Base
	loadBase()
	try:
		f = open("valid.m3u","w")
		f.write("#EXTM3U\n")
		for i in g_Base:
			for url in i.m_url:
				if url.m_count:
					f.write("#EXTINF:-1,"+i.m_name+"\n")
					f.write(url.m_url +"\n")
		f.close()
	except:
		print("ERROR: ")

def main():
	print ("******************************")
	print ("IPTV chanal validater ")
	print ("params: scan заполнение базы по mзu листам")
	print ("example:")
	print ("	lnx>$2.py scan")

	global g_flag
	global g_playlist_name

	mode="gen"

	try:
		if sys.argv[1] =="scan":
			mode="scan"
			if sys.argv[2]=='new':
				g_flag="new"
			else:
				g_playlist_name = sys.argv[2]		
		elif sys.argv[1] =="validate":
			mode="validate"
		elif sys.argv[1] =="gen":
			mode="gen"
	except:		
		pass 	
	if mode=="scan":
		scan()
	elif mode=="validate":
		validate()
	elif mode=="gen":
		genM3u()


main()	

