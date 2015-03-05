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

g_noname_base_file="noname.db"
g_base_name_file="base.db"
g_playlist_name=["edem.m3u"]
g_Base = []
g_NoNameChanels=[]

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

def saveNoNameChanel():
	global g_NoNameChanels
	try:
		f=open(g_noname_base_file,"wb")
		pickle.dump(g_NoNameChanels,f)
		f.close()
	except:
		print ("ERROR: Dont save NoNameBase")

def loadNoNameChanel():
	global g_NoNameChanels
	try:
		f=open(g_noname_base_file,"rb")
		g_NoNameChanels=pickle.load(f)
		f.close()
	except:
		print ("ERROR: Dont load NoNameBase")

def find(url,base):
	for i in base:
		if i.m_url==url:
			return True
	return False 

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
			if not(find(url, a.m_url)):				
				a.m_url.append(URL(url))
			return
	b = Chanel()
	b.m_name = name
	b.m_url=[URL(url)]
	g_Base.append(b)
	print ("GBase count: " + str(len(g_Base)))			

def scan():
	global g_playlist_name
	for playlist_name in g_playlist_name:
		print playlist_name
		loadBase()
		try:
			f=open(playlist_name,"r")
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
					name = re.sub("\s{1,}$","",name)
					url = re.sub("\s{1,}$","",url)
					print("%d:%s url:%s" % (n,name,url))

					addToBase(name,url)
				elif re.match(r"#EXT-X-",i):
					print("ERROR: find new tag %s", i)
				n+=1
		except:
			print ("ERROR: File %s not exist" % playlist_name)

		if len(g_Base) > 0:
			saveBase()
		if len(g_NoNameChanels) > 0:
			saveNoNameChanel()

def testUrl(p,url):
	ret=False
	print "url:" + url
	if not(re.match("rtmp:",url)):
		p.set_mrl(url)
		p.play()
		for ii in range(0,15):
			time.sleep(1)
			if p.is_playing():
				ret=True
			print str(ii)+" play:"+str(p.is_playing())+" state: "+ str(p.get_state())
			if p.get_state()==vlc.State.NothingSpecial:
				continue
			elif p.get_state()!=vlc.State.Opening:
				print p.get_state()
				break
		p.stop()
	return ret

def validate(start):
	global g_Base
	i = vlc.Instance()
	p = i.media_player_new()
	loadBase()
	n=0	
	for i in g_Base:
		for url in i.m_url:
			n+=1
			if n < start:
				continue
			url.m_count = testUrl(p, url.m_url)			
			if n%10==0:
				print "Saved: " + str(n)
				saveBase()
	saveBase()

def genM3u(priority):
	global g_Base	
	loadBase()
	pr=[]
	try:
		if priority!="":
			print ("Priority file:"+ priority)
			f=open(priority,"r")
			pr=f.readlines()
			f.close()
			pr=map(lambda x:re.sub("\s{1,}$","",x),pr)
			for i in g_Base:
				i.m_name=re.sub(r"\s{1,}$","",i.m_name)
				i.pr=(i.m_name in pr)
			g_Base= sorted(g_Base,key=lambda i:not(i.pr) ) 		
	except:
		print ("ERROR:priority file not found %s" % priority)	
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

def genNoNamePlaylist():
	global g_NoNameChanels
	validUrl=[]
	loadNoNameChanel()
	i = vlc.Instance()
	p = i.media_player_new()
	for url in g_NoNameChanels:
		if testUrl(p,url):
			validUrl.append(url)
	f=open("noname.m3u","w")
	f.write("#EXTM3U\n")
	for url in validUrl:
			f.write(url+"\n")
	f.close()

def genList(flag):
	loadBase()
	global g_Base
	for i in g_Base:
		for url in i.m_url:
			if flag=="":
				print("valid:%d name:\"%s\" url:\"%s\" " % (url.m_count, i.m_name, url.m_url))
			elif flag=="name":
				print i.m_name
				break
			elif flag=="valid":
				if url.m_count:
					print i.m_name
					break	

def main():
	print ("******************************")
	print ("IPTV chanal validater ")
	print ("params: scan заполнение базы по mзu листам")
	print ("example:")
	print ("	lnx>$2.py scan")

	global g_playlist_name

	mode=""
	start = 0
	priority=""
	flag =""
	try:
		if sys.argv[1] =="scan":
			mode="scan"
			g_playlist_name=[]
			for i in range (2,len(sys.argv)):
				g_playlist_name.append(sys.argv[i])
		elif sys.argv[1] =="validate":
			mode="validate"
			start = int(sys.argv[2])
			print start
		elif sys.argv[1] =="gen":
			mode="gen"
			priority=sys.argv[2]
		elif sys.argv[1] =="genNoName":
			mode="genNoName"
		elif sys.argv[1]=="list":
			mode = "list"
			flag = sys.argv[2]
	except:		
		pass 	
	if mode=="scan":
		scan()
	elif mode=="validate":
		validate(start)
	elif mode=="gen":
		genM3u(priority)
	elif mode=="genNoName":
		genNoNamePlaylist()
	elif mode=="list":
		genList(flag)


main()

