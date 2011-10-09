#!/bin/env python
# -*- coding: iso-8859-2 -*-
#
# @@@ Coded by p4t0k @@@
#
# e-mail: p4t0kk@gmail.com
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# %% This program is licensed under terms of the GNU GPL.
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# 2006-10-24 >>> Name of room appended to the title.
# 2006-09-08 >>> Listing of permanent OPs (listing of users is not yet available)
# 2006-04-25 >>> Project started!
#

import urllib, re, sys
def rt_main(rid, auth = None):
	"""\
	Tato funkce parsuje nachatovany cas mistnosti vcetne casu v jednotlivych dnech v tydnu. Pozaduje jediny argument rid == room id (muze byt i s pocatecnim znakem "#"), vraci seznam nebo nebo chybovy string
	"""
	rid = str(rid)
	if rid[0] == '#':
		rid = rid[1:]
	try:
		page_info = urllib.urlopen("http://chat.lide.cz/index.fcgi?akce=info_room&room_ID=%s" %(rid)).read()
		#if auth:
			#page_usrs = urllib.urlopen("http://chat.lide.cz/room.fcgi?akce=menu_users&room_ID=%s&auth=%s" %(rid, auth)).read()
	except:
		return rt_err(-1)
	try:
		rname = re.findall(r'M.stnost: <span class="red">(.+?)</span>', page_info)[0]
		tyden, celkem = re.findall("Prochatov.no:</strong></td>\n\t\t<td>\n\t{3}(.+?)\shod.+?celkem\s(.+?)\shod", page_info)[0]
		# dny v tydnu
		wdny = re.findall("<tr>\n\t<th>den</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>\n\t\n\t\t<th>(.+?)</th>", page_info)[0]
		# casy k jednotlivym dnum
		wcasy = re.findall("<tr align=\"center\">\n\t<td>hod</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ >(.+?)</td>\n\t\n\t\t<td\ class=\"red\ strong\">(.+?)</td>", page_info)[0]
		
		# operatori a uzivatele
		OPs = re.findall('akce=profile" target="_blank">([^<]+)</a>', page_info)
		#if auth:
			#users = re.findall("<SPAN onMouseOver=\"top.popup\('([^']+)'", page_usrs)
		
		mgd = []
		for x in xrange(len(wdny)):
			mgd.append(wdny[x])
			mgd.append(wcasy[x])

	except:
		return rt_err(-2)
	rt_res = []
	rt_res.append("\nMistnost \002"+rname+"\002 [#"+str(rid)+"]:\n"+(14+len(str(rid))+len(rname))*'-'+"\n")
	rt_res.append("Prochatovano: %s hod/tyden; %s celkem" % (tyden, celkem))
	rt_res.append("Operatori: %s" %(', '.join(OPs)))
	#if auth:
		#rt_res.append("Uzivatele online: %s" %(", ".join(users)))
	rt_res.append("\nStatistika:\n")
	for y in xrange(0, len(mgd), 2):
		rt_res.append("%s: %s" % (mgd[y], mgd[y+1]))
	#rt_res += "\n"
	return rt_res

def rt_err(n):
	"""vlastni error handler - vraci retezec s oznacenim chyby"""
	#TODO:	prepsat tak, aby se chyby vracely do lidegw.py a byly pod spravou funkce log()
	err_types = ("Chyba pri stahovani stranky", "Chyba pri parsovani stranky s casy.")
	# prevede zaporne cislo chyby na index seznamu chyb
	n = (abs(n) - 1)
	return '[Error] ' + err_types[n]

