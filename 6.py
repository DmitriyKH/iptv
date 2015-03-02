#!/usr/bin/python
class AA:
	def __init__(self,name):
		self.m_id=0
		self.m_name=name

import re
g_a=[AA("sss"),AA("zxzxc"),AA("675675"),AA("1"),AA("2"),AA("3")]
g_b=[]
try:
	f=open("2.txt","r")
	l=f.readlines()
	f.close()
except:
	print ("ERROR:File not found")


l = map(lambda x:re.sub("[\n\r]","",x),l)


for z in g_a:
	z.m_id =(z.m_name in l)

g_a =sorted (g_a,key = lambda x:x.m_id,reverse=True)

for i in g_a:
	print i.m_name + str(i.m_id)


