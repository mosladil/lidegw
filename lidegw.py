#! /bin/env python
# -*- coding: utf-8 -*-
#
# IRC brana na webchat lide.cz
#	diky niz se lze pripojit na lide.cz
#	pres IRC klienta (xchat,irssi,mIRC)
#	je mozne pouziti eggdropa a jinych
#	jiz hotovyh botu.
#
# Puvodni autor tohoto projektu je gimper,
#	Michal Danicek
#	Czech Republic
#	gimperek@gmail.com
# v soucasnosti se o aktualizace a rozsirovani brany staraji:
#	p4t0k
#	p4t0Kk@gmail.com
#	http://vypnuto.ic.cz/
#	
#	Trancelius
#	trancelis@centrum.cz
#	http://elatio.wz.cz/
#
# Provoz:
#	Je zapotrebi python, nejlepe ve verzi 2.3 nebo novejsi
#	
#	na POSIX-like systemech (Linux, BSD, ...):
#		$ python lidegw
#
#	na Windows (98, 2000, XP)
#	je nutne stahnout a nainstalovat http://www.python.org/
#	nasledne spustit python s parametrem 'lidegw'
#
# Lide.cz posila text v kodovani iso-8859-2, takze si to nastavte v klientovi.
#
# Nastaveni irssi pro UTF-8 terminal:
# /set recode_out_default_charset iso-8859-2
# /set term_charset UTF-8
# /set recode_fallback iso-8859-2
#
# Prikazy lidegw:
#	/quote set idler (cislo > 250 | 0) [ v sekundach ] 	- nastavi udrzovac
#	/quote set girls_highlighting (0|1) [ bool ] 		- zapne/vypne zvyrazneni holek
#	/quote set rewrite_protocols (0|1) [ bool ]		- zapne/vypne prepisovani protokolu (napr. http -> h77p)
#	/quote set idler_str (string) [ idler string ]		- zmeni retezec idleru
#	/quote ison (nick) [ hledany nick ] 			- Zjisti zda je nick online, pokud se nic nevypise, tak neni online
#	/ison nick						- totez
#	/list 							- vypise seznam mistnosti
#	/list [cast nazvu]					- vyhleda mistnosti s odpovidajici casti nazvu
#	/quote set ascii (0|1|2|3)				- filtr diakritiky, 0 = vypnout; 1 = filtrovat vse; 2 = filtrovat pouze odchozi; 3 = filtrovat pouze prichozi
#	/quote set timer CISLO					- nastavi prodlevu mezi obnovenim textu (refresh) v sekundach
#	/quote set crypto 1 KLIC				- zapne backend a nastavi klic, text k sifrovani musi zacinat teckou, k desifrovani dvema
#	/quote set crypto 0					- vypne crypto
#	/quote set charset SADA					- nastavi znakovou sadu (pro ASCII, ISON, WHOIS, ...). Realne bude fungovat asi jen iso-8859-2 (latin2), cp1250 a utf-8
#	/quote set smiles 0|1 [ bool ]				- 0 = bezne orezavani; 1 = bude vypisovat jen :CISLO: (vhodne pro roboty)
#	/whois <nick>						- vypise informace z profilu uzivatele nick
#	/info <room_id>						- vypise statistiky mistnosti a celkovy nachatovany cas mistnosti room_id
#	/quote set urls 0|1					- vypne|zapne upravu URL na ochcani trapne cenzury nepornografickych linku na Lide.cz
#	/quote set charset CHARSET				- nastavi znakovou sadu na strane klienta, 0 vypne
#
# ------------------ CHANGELOG -------------------
# lidegw-36: (deltaflyer4747)
# Drobná oprava parsingu textu z lide.cz (top.a3 > top.a4) / bug znemoznoval cteni prichozich zprav
# lidegw-35: (deltaflyer4747)
# Oprava charsetu i pro TOPIC mistnosti
# lidegw-34: (deltaflyer4747)
#	nahrazeni ´ -> ' kvuli konverzi znakovych sad
#	hack pro nevalidni klienty typu Miranda (co neposilaji dvojtecku pred datovou casti)
# lidegw-33:
#	upraven parser systemovych zprav, aby se nenechal splest vhodne zvolenym username
#	duplex recode mezi libovolnou znakovou sadou a iso-8859-2. Ovlivnuje to commandline parametr --charset=NECO, kde NECO je znakova sada podporovana systemem (napr. utf-8, iso-8859-2, windows-1250) a /quote prikaz. Volba --utf8-lipp už není.
#	drobná oprava metody Lide.unsmilize
#	pridana funkce "/quote set rewrite_protocols", kterou se da zapnout (resp. vypnout) prepisovani protokolu v adrese
# lidegw-32:
#	pridan opraveny modul lipparser (p4t0k)
#	ziskavani last_ID bylo dano do try bloku, stejnym zpusobem byl osetren IndexError ve funkci fromArray (p4t0k)
# lidegw-31:
#	posledni, uspesny pokus. Bylo to promennou 'last' v GET requestu.
#	opraven filtr vstupniho textu, <b> uz neztucni text
#	opravena serie chyb zpusobena predchozi opravou filtru :))
#	pridana volba urls - uprava URL na ochcani trapne cenzury nepornografickych linku na Lide.cz
# lidegw-30:
#	dalsi zoufaly pokus o opraveni oslepujiciho bugu - dynamicky se menici cookies a nahodne cislo za URI
# lidegw-29:
#	/info uz nevyzaduje parametr - bere si aktualni rid, ale zustava, ze mu ho muzete dat explicitne (p4t0k)
#	Doplnena re.findall funkce parsujici jmeno mistnosti + pridani tohoto jmena do topicu mistnosti (p4t0k)
# lidegw-28:
#	Opraven bug ve vlakne co handluje vstup z IRC klienta + par malych (mozna bezvyznamnych) zmen v Collectoru (p4t0k)
#	Opraven bug s mezerou v hesle (trancelius, diky nocturne.op.15 za upozorneni)
#	Opraven bug (snad) s neexistujici referenci na room.hashid_part (p4t0k)
# lidegw-27: (trancelius)
#	Novy crypto subsystem zalozeny na kombinaci symetricke XOR sifry a base64, mel by zvladat libovolne znaky
#	Novy ASCII filtr zalozeny na vnitrnich funkcich pythonu, je potreba nastavit charset terminalu (/quote set charset utf-8 treba)
#	Charset je defaultne iso-8859-2, prepinacem --utf-8 se forcne UTF-8. Nahrazuje to prepinac --utf8-lipp, protoze to ma vliv i na dalsi veci.
#	Charset nastaveny pres /quote set ma vliv i na ison, whois a dalsi.
# lidegw-26:
#	aktualizace k lidecz-20060926 (trancelius)
# lidegw-25:
#	aktualizace k lidecz-20060913 (trancelius)
# lidegw-24:
#	/info reaguje na --utf8-lipp a pridava vypis stalych spravcu (trancelius)
# lidegw-23:
#	ISON pouziva lipp
#	maska ma misto hashe uzitecnejsi informace
# lidegw-22:
#	opraven bug s obcasnym opakovanim prijateho (asi i odeslaneho) textu (trancelius)
#	opraven event parser, aby prijimal vsechny JOIN/PART udalosti (trancelius)
#	pridan switch --utf8-lipp pro vystupni unicode kodovani u lipparseru (trancelius)
#	osetreni zapisu lockfile na ruznych OS (p4t0k)
# lidegw-21: (trancelius)
#	novy vlaknovy kod
#	opraveno vicenasobne posilani textu v PM, pokud je odesilatel ve vice mistnostech
#	opraveno vicenasobne cteni textu z mistnosti
#	pridan --debug, monitoruje cinnost vlaken (kdyby se neco zamotalo)
#	text brany preveden do unicode
#	experimentalni uprava idleru, ktera strida dva stringy (kvuli lide.cz flood protection)
#	online registrace kvuli pocitani uzivatelu
#	opraven mode parser (lidegw uz nepreda +h nekomu, kdo ho odchodem ztratil)
#	 - metody getOP a getOPs jsem sloucil do jedne, updOPs, ktera je updatuje najednou a primo
#
### Milestone: version 2.0 ###
#
# lidegw-r20: Nova featura /info - vypisuje statistiku mistnosti - prochatovany cas. (p4t0k)
# lidegw-r19: Opraven bug ve vicenasobnem pripojovani do mistnosti - napr. /join 732368,552433 kvuli nemu driv neslo (p4t0k)
# lidegw-r18: Opraven bug ve funkci trancecode() && pridan cas a datum k vypisu pripojeni/odpojeni klienta k lidegw (p4t0k)
# lidegw-r17: Lepsi parser sys.zprav (trancelius)
# lidegw-r16: Pridana podpora odesilani i velmi dlouhych useku textu (trancelius)
#             TOPIC spravne prevadi html entity na znaky (trancelius)
# lidegw-r15: Moznost zmeny orezavani smajliku (trancelius)
# lidegw-r14: Dodelano zacleneni lippu (p4t0k); potrebna uprava modulu lipparser [i main.py u lippu] (trancelius)
# lidegw-r13: Opraven bug v idleru a prepsan mechanismus slucovani idler_str retezce (p4t0k)
# lidegw-r12: Pokusne zacleneni lide.cz profile parseru (lipp) (modul p4t0k, zacleneni trancelius)
# lidegw-r11: Rozsirena podpora MODE prikazu, konkretne pridani +h, -o a -h. (trancelius)
#             Vsechny neparsovane systemove zpravy se zobrazuji jako NOTICE (trancelius)
# lidegw-r10: Opraven idler, uz by mel pocitat spravne (trancelius)
# lidegw-r09: Opraveno posilani duvodu u kicku (trancelius)
# lidegw-r08: Opravy text_filter(), /me uz zase funguje (trancelius)
# lidegw-r07: Pridana podpora sifrovani, viz prikazy (trancelius)
#             Opraven TOPIC (trancelius)
#             Pri vstupu do mistnosti se vypise jeji URL (trancelius)
# lidegw-r06: Konecne spravne chovani OPu, half-OPu a vseho mozneho predavani (trancelius)
#             Nastavitelna frekvence aktializace (trancelius)
# lidegw-r05: Nova 'dokumentace' a 'motd' (trancelius)
#             Opravena komunikace s lide.cz, nenacital se cas mistnosti (trancelius)
# lidegw-r04: Pridan filtr diakritiky, viz prikazy (trancelius)
# lidegw-r03: Opraven problem se smajliky (p4t0k)
#             Predelany user flagy (trancelius)
#             Opraveno logovani na lide.cz (trancelius)
#             Odstraneni modulu ClientCookie (trancelius)
#             Pri prihlaseni se vypise URL hlavni stranky s prihlasenym uzivatelem (trancelius)
# lidegw-r01: Castecne prepsani "WELCOME MESSAGE" (p4t0k)
#             Uhlazeni vypinani lidegw [pomoci ctrl+c, ctrl+d] (p4t0k)
#
# Beta testeri: vsichni uzivatele lidegw jsou vlastne testery, dekujeme vam

import copy, md5, os, re, socket, string, sys, threading, time, urllib, urllib2, random
traceback = None
lipparser = None
rtime = None
import traceback
try:
	import lipparser
except:
	print "Chybi lipparser, nebude fungovat WHOIS, ISON a dalsi."

try:
	import rtime
except:
	print "Chybi rtime, nebude fungovat INFO."

def log(text, level = 0):
	if debug or level == 1:
		print "[%s] %s" % (time.strftime('%Y/%m/%d %H:%M:%S'), text)

version_ = "lidegw-36"
girls_lighting = 1
rewrite_proto = 1
idler_str = ["\xc2", "\xc3"]
if "--debug" in sys.argv:
	import traceback
	debug = True # tisknout vše
else:
	debug = False # tisknout jen něco

if "--port=" in ' '.join(sys.argv):
	PORT = int(re.findall("--port=(\d+)", ' '.join(sys.argv))[0])
else:
	PORT = 13801

CHARSET = "iso-8859-2" # trochu jako makro... :D
for arg in sys.argv:
	if "--charset=" in arg:
		CHARSET = arg.replace("--charset=", "").lower()
		try:
			"test".encode(CHARSET)
		except LookupError:
			log("!!! Znakovou sadu %s system nepodporuje, fallback na iso-8859-2" %(CHARSET), 1)
			CHARSET = "iso-8859-2"
		break

#is_on = []
#is_data = {}

class world:
	vlakna = []
	collector = None
	
# <skládka>
world.welcome = ''':%s 001 %s :
   
Vitam te na %s
   
Lide.cz <-> IRC brana, verze %s
(cc) Gimper, p4t0k, Trancelius
   
 *** all your base are belong to us ***
   
MiniHelp:
   
Pro vypsani vsech stalych mistnosti napiste /list
Pro vypsani jen urciteho roomu napiste /list <nazev>
Do mistnosti vstupte pomoci /join <#ID_mistnosti>
Informace o uzivateli vypisete prikazem /whois <nick> // tato funkce vyzaduje modul lipparser
   
Lide.cz ticket: %s
Lide.cz hash: %s
Pri vstupu do mistnosti ti bude vypsana jeji URL, ale nejdriv je potreba pouzit ticket.
(stejne to asi nebude fungovat)
   
>>> Enjoy :)
   
   
''' # ty prazdny radky maji mezery schvalne kvuli IRC klientum, aby je neignorovali
# </skládka>

def fromArray(array, key):
	for item in array:
		if item[0].upper() == key.upper():
			try:
				return item[1]
			except(IndexError):
				if traceback:
					traceback.print_exc()
				print "[??] Hodnota promenne item je %s.\n[!!] Podejte prosim bug-report. ;)" % (item)

# zaregistrujeme lidegw, at je trochu prehled o siri uzivatelske zakladny (na serveru se ulozi md5 ip adresy)
#if os.name in ('posix', 'mac'):
	#savedir = os.getenv("HOME")
#elif os.name == 'nt' and os.getenv("HOMEPATH"):
	#if os.getenv("HOMESHARE"):
		#savedir = os.getenv("HOMESHARE") + os.getenv("HOMEPATH")
	#else:
		#savedir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
#else:
	#savedir = os.path.dirname(sys.argv[0])

#reg_file = os.path.join(savedir, ".lidegw_registered")

# hehe, hadejte proc :))
#if (not os.path.exists(reg_file) and "--no-reg" not in sys.argv) or "--reg" in sys.argv:
	#reg_r = urllib.urlopen("http://elatio.wz.cz/rpc/rpc_register.php")
	#reg_d = reg_r.read()
	#if "registered_ok" in reg_d:
		#log("Registrovanych uzivatelu: %s" %(len(reg_d.strip().split("\n"))), 1)
		#try:
			#open(reg_file, "w")
		#except(IOError): pass

class Collector(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True
		log("collector, init")
	def run(self):
		log("collector, start")
		while self.running:
			vlaken = len(world.vlakna)
			for vlakno in world.vlakna:
				if not vlakno.isAlive() and vlakno._Thread__started:
					world.vlakna.remove(vlakno)
					log("collector, purging %s" %(vlakno))
					del vlakno
					vlaken -= 1
			log("collector, all clear (%s threads)" %(vlaken))
			time.sleep(5)
		
		# shutdown
		for vlakno in world.vlakna:
			vlakno.running = False # shodim zbytek vlaken, aby se to vubec vyplo
		log("collector, shutdown")
	def start_threads(self):
		try:
			for vlakno in world.vlakna:
				if not vlakno._Thread__started:
					vlakno.start()
		except:
			log("Vlakno odmita startovat, pravdepodobne dosla pamet.", 1)

class RedirectHandler(urllib2.HTTPRedirectHandler):
	"""Volano jen pri loginu."""
	def http_error_302(self, req, fp, code, msg, headers):
		try:
			return (headers.getheader("Location"), re.findall("ds=(.+);path", headers.getheader("Set-cookie"))[0])
		except(TypeError):
			pass

class msg:
	"""Struktura zpravy"""
	text 		= ""
	nick		= ""
	target		= ""
	type		= -1

class room:
	"""Struktura mistnosti"""
	room 		= ""
	room_name	= ""
	last 		=  0
	ops		=  0
	op		=  0
	users		= []
	idler_str	= None # kazda mistnost ma svoji instanci, aby se zajistilo spravny stridani
	c1time		= ""   #
	c2time		= ""   # kazda mistnost ma vlastni
	last_idle	=  0
	hashid_text	= "" # pouziva se pri odeslani zprav
	hashid_part	= "" # pouziva se pri opusteni roomu

class lide:
	"""Struktura spojeni uzivatele"""
	user		= ""
	nick		= ""
	passwd		= ""
	auth		= ""
	s		= ""
	ERROR		= ""
	room		=  0
	logged		=  0
	kernel		=  0
	idle_interval	=  0
	rooms		= []
	mainurl 	= "http://chat.lide.cz/index.fcgi"
	loginurl	= "https://login.seznam.cz/loginProcess"
	profile 	= "http://profil.lide.cz/profile.fcgi"
	room_url	= "http://chat.lide.cz/room.fcgi"
	me		= "lide.cz"

class Lide:
	"""Trida spojeni uzivatele"""
	def __init__(self, mySocket, myAdress):
		self.socket = mySocket
		self.adress = myAdress
		self.kernel = copy.deepcopy(lide())
		self.connection = True
		# TODO: presunout nasledujici primo do classy lide
		#self.kernel.urlopen = urllib2.urlopen
		self.kernel.opener = urllib2.build_opener(RedirectHandler())#, urllib2.HTTPHandler(debuglevel=1))
		self.kernel.urlopen = self.kernel.opener.open
		self.kernel.logged = False
		self.kernel.rooms = []
		self.kernel.girls_highlighting = girls_lighting
		self.kernel.rewrite_protocols = rewrite_proto
		self.kernel.idler_str = idler_str
		self.kernel.sex = ""
		self.kernel.asciionly = 0
		self.kernel.timer = 6
		self.kernel.crypto = 0
		self.kernel.cryptokey = None
		self.kernel.smiles = 0
		self.kernel.urls = 1
		self.kernel.hashid = "" # pouziva se pri logoutu
		self.kernel.randomnumber = 1234 # vystrel do tmy
		self.kernel.charset = CHARSET
		
	def info(self, text, type = "099"):
		"""Metoda pro komunikaci systemovych hlaseni smerem k ircclientu. Nepovinny parametr 'type' obsahuje IRC kod odeslane zpravy."""
		self.socket.send(":%s %s %s %s\n" %(self.kernel.me, type, self.kernel.nick, text))
	
	def updateCookie(self):
		self.kernel.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; cs; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7'),
						('Cookie', 'ds=%s' %(self.kernel.auth))]
	
	def login(self):
		"""Metoda logovani na lide.cz"""
		pole = {
			'username': self.kernel.nick,
			'password': self.kernel.passwd,
			'domain': "seznam.cz", # zatim to stačí takhle
			'remember': "1",
			'serviceId': "lide",
			'disableSSL': "0",
			'forceSSL': "0",
			'lang': "cz",
			'template': "html",
			'lang': "cz",
			'loggedURL': "http://www.lide.cz/",
			'loginFormIsSSL': "1",
		}
		params = urllib.urlencode(pole).replace('%3A',':')
		try:
			self.updateCookie()
			data = self.kernel.urlopen(self.kernel.loginurl, params).read()
			self.kernel.ticket = re.findall('url=(http://[^"]+)"', data)[0]
			url, self.kernel.auth = self.kernel.urlopen(self.kernel.ticket)
			self.updateCookie()
			#self.kernel.opener.addheaders.append()
							#('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; cs; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7'),
							#('Accept', 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
							#('Accept-Language', 'cs,en-us;q=0.7,en;q=0.3'),
							#('Accept-Charset', 'ISO-8859-2,utf-8;q=0.7,*;q=0.7'),
							#('Keep-Alive', '300'),
							#('Connection', 'keep-alive'),
							#('Referer', 'http://chat.lide.cz/room.fcgi?akce=menu_top&auth=&room_ID=732368'),
							#('Accept-Encoding', 'gzip,deflate'),
							#]
			
			# ještě hashid
			data = self.kernel.urlopen("http://chat.lide.cz"+url).read()
			self.kernel.hashid = re.findall('hashId=(\d+)"', data)[0]
		except:
			self.kernel.ERROR = ":%s %s\n" %(self.kernel.me, "ERROR: Can't login to lide.cz")
			raise
	
	def listRooms(self):
		"""Metoda pro /list - vypis mistnosti"""
		try:
			r = self.kernel.urlopen("%s?akce=rooms" %(self.kernel.mainurl))
		except:
			raise

		s = r.read()

		s = str.join('',s.splitlines())

		s = s.replace('\t','')

		s = s.replace('<tr class="row1">','<tr class="row1">\n')
		s = s.replace('<tr class="row0">','<tr class="row0">\n')
		s = s.replace('</tr>','</tr>\n')

		data = re.findall(r'<td class="right w">(.+)<td class="center"><strong><a href="room.fcgi.+auth=.*room_ID=(.+)">(.+)</a></strong><div>st.+l.+stnost.+<td class="center w">(.+)</td></tr>',s)

		return data
	
	def setGirlsPrefix(self):
		"""Metoda posle zmenu kanalum"""
		for croom in self.kernel.rooms:
			croom.users = self.getChannelUsers(croom.room)
			s = ""
			for user in croom.users:
				s = "%s%s%s " %(s, self.isOP(user, croom), user[0] )
				
				self.socket.send(":%s 352 %s #%s %s %s %s %s H%s :0 %s user\n" %(self.kernel.me, self.kernel.nick, croom.room, self.hash(user[0],"",2), self.hash(user[0],"",1), self.kernel.me, user[0], self.isOP(user,croom), self.kernel.me) )
				print "================="
				print ":%s 352 %s #%s %s %s %s %s H%s :0 %s user\n" %(self.kernel.me, self.kernel.nick, croom.room, self.hash(user[0],"",2), self.hash(user[0],"",1), self.kernel.me, user[0], self.isOP(user,croom), self.kernel.me)
				print ":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, croom.room, s)
				print ":%s 366 %s #%s :End of /NAMES list.\n" %(self.kernel.me, self.kernel.nick, croom.room)
				print "--------------"
			
			self.socket.send(":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, croom.room, s) )
			self.socket.send(":%s 366 %s #%s :End of /NAMES list.\n" %(self.kernel.me, self.kernel.nick, croom.room) )
	
	def getWhois(self, nick):
		"""getWhois metoda"""
		if not lipparser:
			return False
		lipp = lipparser.myparser(nick)
		output = []
		for chapter in ['Z\xe1kladn\xed \xfadaje','Statistick\xe9 \xfadaje','\xdadaje na profil','Postava','Povaha','Kon\xed\xe8ky','Dom\xe1cnost','Sezn\xe1men\xed','Z\xe1vislosti']:
			switch = 0
			for item in lipp.lippvars[chapter]:
				if item[1]:
					if switch == 0:
						output.append("[\002%s\002]" %(chapter))
						switch = 1
					if item[0] == 'komentar':
						output.append(item[1][0])
						break
					elif type(item[1]) == str:
						output.append(item[0]+" "+item[1])
					elif type(item[1]) == list:
						if type(item[1][0]) == str:
							output.append(item[0]+" "+item[1][0])
						elif type(item[1][0]) in [list, tuple]:
							output.append(item[0]+" "+' '.join(item[1][0]))
		if self.kernel.charset != "iso-8859-2":
			utf = []
			for line in output:
				utf.append(line.decode("iso-8859-2").encode(self.kernel.charset))
			return utf
		else:
			return output

	
	def getInfo(self,rid = None):
		"""getInfo metoda - importuje modul rtime a dale zpracovava casy mistnosti"""
		if rtime:
			s = ""
			if not rid:
				rid = self.kernel.room.room
			# zavolame modul rtime.py 
			rt_info = rtime.rt_main(rid, self.kernel.auth)
			if type(rt_info) == list:
				if self.kernel.charset != "iso-8859-2":
					utf = []
					for line in rt_info:
						utf.append(line.decode("iso-8859-2").encode(self.kernel.charset))
					rt_info = utf
				for line in rt_info:
					s += ":NOTICE %s\n" % (line)
				#s += ":%s 318 %s %s :End of /INFO list.\n\n" % (self.kernel.me, self.kernel.nick, `rid`)
			else:
				s += ":%s 323 %s :%s\n" %(self.kernel.me, self.kernel.nick, rt_info)
			self.socket.send(s)
		else:
			return None
	
	def joinit(self,Aroom):
		"""\
		joinit metoda - vysle pozadavek metode self.kernel.urlopen (ta je jen 'volanim' urllib.urlopen), ktera vrati stanku s mistnosti
		nebo s informaci o neexistenci mistnosti. Navratova hodnota metody joinit je True v pripade uspechu, False == neuspech
		"""
		
		try:
			r = self.kernel.urlopen("%s?room_ID=%s" %(self.kernel.room_url, Aroom))
		except:
			return False
		
		s = r.read()
		kick = re.findall('<p><P>Vstup odm.tnut kv.li vykopnut.. N.vrat je mo.n. za <span class="red">(\d+?)</span> minut.</P> <P>Byl jste vykopnut spr.vcem <span class="red">(.+?)</span></P> <P>Vzkazuje V.m: <span class="red">(.*?)</span></P></p>', s)
		if "stnost neexistuje" not in s and not kick:
			myRoom		= room()
			myRoom.room	= Aroom
			myRoom.last	= "0"
			myRoom.ops 	= []
			myRoom.op	= ""
			myRoom.idler_str= self.kernel.idler_str
			try:
				myRoom.c1time	= re.findall(r'cfg.c1time = "(\d+)";', s)[0]
			except:
				pass
			try:
				myRoom.room_name = re.findall(r'<HEAD>\n <TITLE>(.+) -.+?</TITLE>\n</HEAD>', s)[0]
			except:
				pass
			
			self.kernel.room = myRoom
			
			return True
		elif kick:
			k = kick[0]
			self.socket.send(":%s 474 %s #%s :Cannot join channel (+b)\n" %(self.kernel.me, self.kernel.nick, Aroom))
			self.info("ERROR :Vstup zakazan na %s minut. %s ti vzkazuje: %s" %(k[0], k[1], k[2]), "474")
			return False
		else:
			striped = re.findall(r'<p><P>.+</P></p>', s)
			
			if len(striped) > 0:
				self.socket.send(":%s 323 %s :%s\n" %(self.kernel.me, self.kernel.nick, re.sub(r'<.*?>', '', striped[0])))
				
				return False
			
			self.info("Nemohu vstoupit do mistnosti %s - mistnost neexistuje!" %(Aroom), "474")
			
			return False
	
	def part(self,room):
		"""Part metoda"""
		for croom in self.kernel.rooms:
			if croom.room == room:
				s = self.kernel.urlopen("%s?akce=odejit&room_ID=%s&hashId=%s" %(self.kernel.room_url, croom.room, croom.hashid_part))
				self.kernel.rooms.remove(croom)
		self.socket.send(":%s PART #%s :\n" %(self.hash(self.kernel.nick,""), room))
		
		return True
	
	def ascii(self, text, charset = None):
		"""Orizne diakritiku, vrati pure-ascii text"""
		try:
			import unicodedata
			
			if not charset:
				charset = self.kernel.charset
			return unicodedata.normalize('NFKD', text.decode(charset)).encode('ascii', 'ignore')
		except:
			return text
	
	def xor64(self, text):
		"""Crypto funkce, 'text' ignoruje, '.text' zakoduje klicem, '..text' klicem dekoduje."""
		try:
			import base64
			
			if len(text) < 2 or text[0] != ".":
				raise
			if text[0:2] == ".." and text[2] != ".":
				encode = False
				text = base64.b64decode(text[2:])
			else:
				encode = True
			output = []
			for i in range(len(text)):
				s = text[i]
				p = self.kernel.cryptokey[i%len(self.kernel.cryptokey)]
				output.append(chr(ord(s) ^ ord(p)))
			
			if encode:
				return "..%s" %(base64.b64encode(''.join(output)))
			else:
				return "\002%s\002" %(''.join(output))
		except:
			return text
	
	def recode(self, text, odkud):
		"""Recoduje text z/na self.kernel.charset, podle hodnoty odkud. Odkud = 1 je text z chatu, 0 z IRC. Znak \xc2 musíme zachovat."""
		try:
			if odkud == 1:
				return text.decode("iso-8859-2").encode(self.kernel.charset)
			else:
				text = text.replace("\xc2", "\xc3\x82")
				return text.decode(self.kernel.charset).encode("iso-8859-2")
		except:
			return text
		
	
	def text_filter(self, text, odkud = None):
		"""Obecny filtr textu, podle nastavenych hodnot si vola jednotlive dilci filtry. Nepovinny parametr 'odkud' indikuje, odkud je metoda volana (rozhoduje se podle toho ascii filtr). Odkud 1 je IN a 0 je OUT.
		Veskery text prochazi prave tudy."""
		# prioritni filtry
		text = self.unsmilize(text)
		text = text.lstrip(" ")
		if odkud == 1:
			text = text.replace("<b>", "\002")
			text = text.replace("</b>", "\002")
			text = self.striphtml(text)
			text = text.replace("\xc2", "\x01")
			if self.kernel.rewrite_protocols == 1:
				text = text.replace("h77p://", "http://")
				text = text.replace("f7p://", "ftp://")
		else:
			# zjistim, jak se rekne ´ v charsetu klienta a nahradim to ascii znakem 0x27 (lide.cz to stejne prevedou zpatky na ´)
			text = text.replace("´".decode("utf-8").encode(self.kernel.charset), "'")
			text = text.replace("\x01", "\xc2")
			if self.kernel.rewrite_protocols == 1:
				text = text.replace("http://", "h77p://")
				text = text.replace("ftp://", "f7p://")
		# ascii cast
		if self.kernel.asciionly == 1 or (self.kernel.asciionly == 2 and odkud == 0) or (self.kernel.asciionly == 3 and odkud == 1):
			if odkud == 1: # text z chatu
				text = self.ascii(text, "iso-8859-2") # chat je vzdycky latin2
			else: # text z IRC
				text = self.ascii(text)
		
		#if self.kernel.charset not in ["latin2", "iso-8859-2", "iso8859-2"]: # je jinej než na chatu
			#try:
				#text = self.recode(text, odkud)
			#except:
				#pass # :)
		
		
		
		# crypto
		if self.kernel.crypto:
			text = self.xor64(text)
		return text
	
	def sendText(self, text, room):
		"""Metoda posilani textu"""
		# workaround :)) najdem si room objekt kvuli r'c.time'
		room = room.replace("#", "")
		for croom in self.kernel.rooms:
			if croom.room == room:
				# našli jsme
				break
		
		if self.kernel.charset not in ["latin2", "iso-8859-2", "iso8859-2"]:
			text = self.recode(text, 0)
			
		try:
			croom.c2time = re.findall('<INPUT TYPE="hidden" NAME="c2time" VALUE="(\d+)" />', s)[0]
			croom.hashid_text = re.findall('<input type="hidden" name="hashId" value="(\d+)" />', s)[0]
		except:
			log("!!! c2time/hashId", 1)
		
		pole = {
			'akce': "text",
			'room_ID': room,
			'text': text,
			'send': "2",
			'skin': "",
			'nechat': "1",
			'c2time': croom.c2time,
			'last_ID': "0",
			'ID_to': "0",
			'mysub': "OK",
			'hashId': croom.hashid_text,
		}
		params = urllib.urlencode(pole).replace('%3A',':')

		try:
			s = self.kernel.urlopen("%s?%s" %(self.kernel.room_url, croom.c1time), params).read()
			# tímhle si nejsem moc jistej UPDATE: jde to :o)
			return True
		except:
			if traceback:
				traceback.print_exc()
			return False
	
	def getTextHashId(self, room):
		"""Ziska hashId pro posilani textu (vola se jen po vstupu do mistnosti)"""
		try:
			page = self.kernel.urlopen("%s?akce=text&room_ID=%s&skin=&m=1" %(self.kernel.room_url, room.room)).read()
			return re.findall('<input type="hidden" name="hashId" value="(\d+)" />', page)[0]
		except IndexError:
			log("Chyba v Lide.getTextHashId", 1)
			return room.hashid_text
	
	def getRoomHashId(self, room):
		"""Ziska hashId pro odchod z mistnosti (vola se jen po vstupu do mistnosti)"""
		try:
			page = self.kernel.urlopen("%s?akce=info&room_ID=%s" %(self.kernel.room_url, room.room)).read()
			return re.findall('hashId=(\d+)"', page)[0]
		except IndexError:
			log("Chyba v Lide.getRoomHashId", 1)
			return room.hashid_part
	
	def updOPs(self, room):
		"""Metoda pro obnoveni seznamu OPs a halfops, predava se ji room objekt, ne room ID"""
		try:
			r = self.kernel.urlopen("%s?akce=info_room&room_ID=%s" %(self.kernel.mainurl, room.room))
		except:
			return False
		
		r_data = r.read()
		half = re.findall("<a href=\"http://profil.lide.cz/profile.fcgi\?akce=profile&user=.+&auth=\" target=\"_blank\">(.+)</a>", r_data)
		OPs = re.findall("profile.fcgi.+auth=.+user=(.+).+akce=profile", r_data)
		
		if half:
			room.op = half[0] # chceme tam string
		else:
			room.op = ""
		room.ops = OPs
		
		return True
	
	def hash(self,nick,room,type=0):
		"""Metoda pro vytvoreni masky"""
		
		# mask nick!nick@sex.lide.cz
		sex = fromArray(self.kernel.room.users, nick)
		if sex == "F":
			sex = "girls"
		else:
			sex = "boys"
		if type == 0:
			#return "%s!%s@%s.%sIP.%s" %(nick, vy[0:9], vy[0:9], vy[10:15].upper(),self.kernel.me)
			return "%s!%s@%s.lide.cz" %(nick, nick, sex)
		elif type == 1:
			#return "%s.%sIP.%s" %(vy[0:9], vy[10:15].upper(), self.kernel.me)
			return "%s.lide.cz" %(sex)
		elif type == 2:
			#return vy[0:9]
			return nick
		else:
			return False
	
	def isOP(self,user,room,i = 0):
		"""Metoda zjistuje, zda je uzivatel OP, SS, GIRL"""
		self.kernel.sex = ""
		for sop in room.ops:
			if sop.upper().strip(" ") == user[0].upper().strip(" "):
					return "@"
		if len(room.op) > 0:
			if room.op.upper().strip(" ") == user[0].upper().strip(" ") :
				return "%"
		if (user[1] == "F" ) and self.kernel.girls_highlighting == 1:
			return "+"
		
		return ""
	
	def isON(self, nicks):
		"""Metoda zjisti, zda je uzivatel online a kde"""
		if not lipparser:
			return False
		online = []
		#print nicks
		for nick in nicks:
			p = lipparser.myparser(nick)
			if p.online and p.online[0] != 'nen\xed v \xbe\xe1dn\xe9 m\xedstnosti ani jinde':
				online.append(nick)
		
		self.socket.send(":%s 303 %s :%s\n" %(self.kernel.me, self.kernel.nick, ' '.join(online)))
	
	def isJoined(self,room):
		"""Metoda zjisti, zda jsem jiz v mistnosti"""
		for croom in self.kernel.rooms:
			if room == croom.room:
				return True
		return False
	
	def getTopic(self,room):
		"""Metoda pro zjisteni popisu mistnosti"""
		try:
			r = self.kernel.urlopen("%s?akce=info_room&room_ID=%s" %(self.kernel.mainurl, room))
			rawtext = re.findall(r'<td align="right" width="120"><strong>Popis:</strong></td>\n[^<>]*<td>([^<>]*)</td>', r.read())
			return self.text_filter(rawtext[0]).strip()
		except:
			return False
		
	
	def getSex(self,nick,room):
		"""Metoda zjisti pohlavi uzivatele"""
		for croom in self.kernel.rooms:
			if croom.room == room:
				croom.users = self.getChannelUsers(room)
				for u in croom.users:
					if u[0].upper() == nick.upper():
						return u
		return ("","")
	
	def getChannelUsers(self,room):
		"""Metoda ke zjisteni uzivatelu v mistnosti"""
		try:
			r = self.kernel.urlopen("%s?akce=menu_users&room_ID=%s" %(self.kernel.room_url, room))
		except:
			return "0"
		return re.findall(r"seluser\(.*,'(.*)','(.*)'\)\">.*</A>[^<]",r.read())
	
	def striphtml(self,text):
		"""Metoda prevede HTML odkazy a nektere entity na plaintext"""
		text = text.replace("&lt;","<")
		text = text.replace("&amp;","&")
		text = text.replace("\\\\","\\")

		crx = re.compile('(<[^>]*?href=")[^>]*("\s*>)', re.IGNORECASE )
		text = crx.sub(r'\1\2', text)

		text = re.sub(r'<a href="">',"",text)
		text = text.replace('</a>','')

		return text
	
	def unsmilize(self,text):
		"""Metoda prevede graficke smajliky na text"""
		if self.kernel.smiles == 0:
			replace = "\002\\2\002{\\1}"
		else:
			replace = ":\\1:"
		return re.sub('<img src="http://im.lide.cz/smile/(.+?).gif" alt="(.+?)" height="15" width="15" />', replace, text)
	
	old = []
	def msgDoPushq(self,text,ignore):
		"""Metoda naplni pole prijatych zprav"""
		new = []
		#m = msg()
		o_m = ""
		nop = re.findall(r"top.a4[(](.*),(.*),'(.*)','(.*)',(.*),(.*),(.*),(.*),(.*),'(.*)'.*[)];", text)
		w = 0
		for cnop in nop:
			# osetreni lide.cz posilani pres m, do vsech mistnosti
			# NOTE: Je to k něčemu ?
			for i in ignore:
				if i == cnop[3]+cnop[2]:
					w = 1
					break
				w = 0
			m = msg() # Legenda Magna est exanima... wohoo !! :D
			if len(cnop) >= 8 and cnop[2] not in idler_str and w != 1:
				try:
					if cnop[1].replace("'","") in ["", "cls"] and cnop[3] == '':
						t = cnop[2].replace("'","")
						#print t
						#print t.__repr__()
						if "vstoupil do" in t or "vstoupila do" in t:
							if "vstoupila do" in t:
								m.nick = "F"
							else:
								m.nick = "M"
							
							m.type = 1
							m.target = re.findall(r'<b>(.*)</b>',t.replace(" ",""))[0]
						elif ("opustil m" in t or "opustila m" in t) or ("mem odstran" in t):
							
							m.type = 2
							m.target = re.findall(r'<b>(.*)</b>',t)[0]
							if t.find("opustil") != -1:
								m.text = "Odesel"
							else:
								m.text = "Neaktivni"
						elif "Nelze ps" in t or " nen" in t:
							m.type = 0
							m.text = self.text_filter("System: %s" %t[10:], 1)
						elif "byl vykopnut" in t or "byla vykopnuta" in t:
							m.type = 6
							try:
								(m.target,m.nick,m.text) = re.findall(r"<b>(.*)</b>.*<b>(.*)</b>. D.vod: (.+)",t)[0]
							except:
								(m.target,m.nick) = re.findall(r"<b>(.*)</b>.*<b>(.*)</b>",t)[0]
								m.text = ""
						elif "edal funkci u" in t or "edala funkci u" in t:
							m.type = 7
							(m.nick,m.target) = re.findall(r'<b>(.+)</b>.*<b>(.+)</b>',t)[0]
						elif " byl vybr" in t:
							m.type = 8
							m.target = re.findall(r"<b>(.*)</b>",t)[0]
						else:
							log(cnop[2], 1)
							m.type = 0
							m.text = self.text_filter("System: %s" %t[10:], 1)
					else:
						# filtry
						msgtext = self.text_filter(cnop[2], 1)
						
						if cnop[4] == "''" and cnop[3].lower() != self.kernel.nick.lower():
							m.type = 5
							m.text = msgtext
							m.nick = cnop[3]
						elif cnop[3].replace("'","").lower() != self.kernel.nick.lower():
							m.type = 3
							m.text = msgtext
							m.nick = cnop[3]
							if m.text.find("Notice:") != -1:
								m.type = 4
								m.text = msgtext.replace("Notice:","")
								m.nick = cnop[3]
								if m.text.find("\x01PING ") != -1:
									m.type = 3
				except:
					m.type = -1
			# NOTE: K čemu je o_m ? Díky tomu lidegw špatně přijímala join/part události.
			#if (m.type != -1) and ((m.nick+m.text+str(m.type)) != o_m):
			if (m.type != -1):
				m.nick = m.nick.replace("'","")
				o_m = m.nick+m.text+str(m.type)
				new.append(copy.deepcopy(m))
		old = []
		return new
	
	def parseIRCData(self,data,msgtime):
		"""Metoda parsuje data z IRC klienta"""
		#
		# rozdelim na jednotlivy casti
		#
		if data == "":
			self.connection = False
			return 2
		# vytvorim pole z commandu
		if data.find("\r\n") != -1:
			irccmd = string.split(data,"\r\n")
		else :
			irccmd = string.split(data,"\n")
		# necham vypsat prikaz, abych vedel jaky prikaz zpusobil chybu
		log("irccmd, %s" % (irccmd))
		# cykluju
		for cmd_array in irccmd:
			# rozdelim jednotlivy pole na cmd[X]
			cmd = string.split(cmd_array.strip() ," ")

			# pokud neni fake ;)
			if len(cmd) > 0:
				#
				# ----- NICK -----
				#
				if cmd[0] == "NICK":
					self.kernel.nick = cmd[1]
				#
				# ----- PASS -----
				#
				elif cmd[0] == "PASS":
					self.kernel.passwd = ' '.join(cmd[1:])
				#
				# ----- USER -----
				#
				elif cmd[0] == "USER":
					# ostatni info
					self.kernel.user = cmd[1]
				#
				# ----- JOIN -----
				#
				elif cmd[0].upper() == "JOIN":
					# protoze mne irc klient posila '#'+rid tak odstranim vsechny '#' zleva 
					striped_ = cmd[1].replace('#','')
					# pokusim se vstoupit do mistnosti
					splited = string.split(striped_,",")
					for striped in splited:
						if self.isJoined(striped) == 1:
							log("ircc, %s already joined" %(striped))
							continue
						if self.joinit(striped):
							log("ircc, joined #%s" %(striped))
							# natahnu si hashIdy
							self.kernel.room.hashid_text = self.getTextHashId(self.kernel.room)
							self.kernel.room.hashid_part = self.getRoomHashId(self.kernel.room)
							
							# zjistim vsechny uzivatele na kanalu
							self.kernel.room.users = self.getChannelUsers(striped)
							# updatuju OPy
							self.updOPs(self.kernel.room)
							# irc klientovi poslu muj vstup a nastavim topic
							self.isOP((self.kernel.nick, None), self.kernel.room) # naplnit sex :D
							self.socket.send(":%s JOIN #%s\n" %(self.hash(self.kernel.nick, striped), striped ))
							# topic
							try:
								topic = self.getTopic(striped).decode("iso-8859-2").encode(self.kernel.charset)
							except:
								topic = "Chyba - Nemohu ziskat popis mistnosti, asi nejsi uspesne prihlasen."
							
							self.socket.send(":%s 332 %s #%s :[%s] %s\n" %(self.kernel.me, self.kernel.nick, striped, self.kernel.room.room_name, topic))
							# poslu www adresu
							self.socket.send(":%s 421 %s URL mistnosti: %s\n" %(self.kernel.me, self.kernel.nick, "http://chat.lide.cz/room.fcgi?room_ID=%s" %(striped)))
							# priradim uzivatele kanalu
							s = ""
							i = 0
							for user in self.kernel.room.users:
								s = "%s%s%s " %(s,self.isOP(user,self.kernel.room), user[0])
								i = i + 1
								
								if i == 40:
									self.socket.send(":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, striped, s))
									s = ""
									i = 0
							
							if s.find(self.kernel.nick) == -1:
								s = "%s%s%s " %(s,self.isOP((self.kernel.nick,""),self.kernel.room),self.kernel.nick) 
											
							self.socket.send(":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, striped, s) )
								
							self.socket.send(":%s 366 %s #%s :End of /NAMES list.\n" %(self.kernel.me, self.kernel.nick, striped) )	
							# nakonec pridelim mistnost
							self.kernel.rooms.append(self.kernel.room)

				#
				# ----- PING -----
				#
				elif cmd[0].upper() == "PING" :

					if len(cmd) >= 2 :
						self.socket.send(":%s PONG :%s\n" %(self.kernel.me, cmd[1]) )
					else :
						self.socket.send(":%s PONG %s\n" %(self.kernel.me, self.kernel.me) )

				#
				# ----- PART -----
				#
				elif cmd[0].upper() == "PART" :
					# sptripnu vsechny '#' od zacatku
					striped = cmd[1].lstrip('#')
					# pokusim se odejit z mistnosti
					reason = ""
					if len(cmd) >= 3:
						for i in range(2,len(cmd)):
							reason = "%s %s" %(reason, cmd[i])
						self.sendText(reason[2:],striped)
					
					self.part(striped)
					# pokud nejsem v zadne mistnosti ukoncim vlakno pro zachytavani zprav
				#
				# ----- LIST -----
				#
				elif cmd[0].upper() == "LIST" :
					#	(chname,rid) =
					# ziskame seznam mistnosti
					rooms = self.listRooms()
					# pokud vypisujeme vsechny mistnosti
					if len(cmd) == 1:
						# a vypiseme je IRC klintovi
						for room in rooms:
							# pokud se najde minimalne nachatovana doba tak ji taky vypiseme	
							if room[0].find("title=") != -1 :
								msgtime = re.findall(r'.+title="(.+)".+',room[0])[0]
								#msgtime = msgtime.split('  ')
								self.socket.send(":%s 322 %s #%s %s :%s [ %s ]\n" %(self.kernel.me, self.kernel.nick, room[1], room[3], room[2], msgtime) )
							else :
								self.socket.send(":%s 322 %s #%s %s :%s\n" %(self.kernel.me, self.kernel.nick, room[1], room[3], room[2]) )
					# pokud hledame se specifckym nazvem
					elif len(cmd) == 2:
						for room in rooms:
							if room[2].upper().find(cmd[1].upper()) != -1 :
								if room[0].find("title=") != -1 :
									msgtime = re.findall(r'.+title="(.+)".+',room[0])[0]
									#msgtime = msgtime.split('  ')
									self.socket.send(":%s 322 %s #%s %s :%s [ %s ]\n" %(self.kernel.me, self.kernel.nick, room[1], room[3], room[2], msgtime) )
								else :
									self.socket.send(":%s 322 %s #%s %s :%s\n" %(self.kernel.me, self.kernel.nick, room[1], room[3],room[2]) )
					# nakonec vypiseme konec /LIST(u)
					self.socket.send(":%s 323 %s :End of /LIST\n" %(self.kernel.me, self.kernel.nick) )

				#
				# ----- PRIVMSG -----
				#
				elif (cmd[0].upper() == "PRIVMSG" or cmd[0].upper() == "NOTICE") and len(cmd[2]) > 0:
					# pokud je to zprava do kanalu
					cmd[2] = cmd[2].replace("\x01","\xc2")
					
					if cmd[0] == "NOTICE":
						cmd[2] = ":Notice: %s" %cmd[2][1:]

					if cmd[1][0] == "#":
						isPM = False
					else:
						isPM = True
					
					# popelnicovi klienti ignoruji RFC a neposilaji dvojtecku
					if not cmd[2].startswith(":"):
						cmd[2] = ":%s" %(cmd[2])
					
					text = ' '.join(cmd[2:])[1:]
					
					# filtry
					text = self.text_filter(text, 0)
					
					if (text.find("VERSION") !=-1) and (len(text) > 20):
						text = text + version_
					# pokud to je PRIVMSG to user

					elif cmd[2].find("PING") == 2:
						text = "/m %s \xc2PING %s" %(cmd[1], cmd[3].replace("\x01","\xc2") )
					
					elif cmd[2].find("PONG") == 2:
						text = "/m %s \xc2PONG %s" %(cmd[1], cmd[3].replace("\x01","\xc2") )
						log(text, 1)
					# narezeme text na 350B oddily
					msg_len = 350
					delimiter = "..."
					# odecteme pocet bytu delimiteru od delky zpravy
					msg_len = msg_len - len(delimiter)
					if len(text) > msg_len:
						texts = []
						i = 0
						while True:
							chunk = text[i:i+msg_len]
							i += msg_len
							if len(chunk) == msg_len:
								texts.append(chunk+delimiter)
							else:
								if chunk:
									texts.append(chunk)
								break
					else:
						texts = [text]
					for text in texts:
						if len(text) > 0:
							if isPM:
								text = "/m %s %s" %(cmd[1], text)
								room = self.kernel.rooms[0] # irc klient neposila u PM room puvodu, tak to poslem z prvni
								if not self.sendText(text, room.room):
									self.info("ERROR :!!! Neodeslano: %s" %(text))
							else:
								if not self.sendText(text, cmd[1]):
									log("Error while posting message.", 1)
								else:
									# update idler
									for room in self.kernel.rooms:
										if room.room == cmd[1][1:]:
											room.last_idle = time.time()
				#
				# ----- MODE -----
				#
				elif cmd[0].upper() == "MODE":
					if len(cmd) >= 4:
						if cmd[2] == "+o" or cmd[2] == "+h":
							self.sendText("/admin %s" %(cmd[3]), cmd[1].lstrip("#"))
						elif cmd[2] == "-o" or cmd[2] == "-h":
							self.sendText("/admin %s" %(self.kernel.nick), cmd[1].lstrip("#"))
				#
				# ----- NAMES -----
				#
				elif cmd[0].upper() == "NAMES" and len(cmd) == 2:
					striped = cmd[1].lstrip('#')
					for room in self.kernel.rooms:
						if striped == room.room:
							s = ""
							room.users = self.getChannelUsers(room.room)
							i = 0
							for user in room.users:
								
								i = i + 1
								s = "%s%s%s " %(s, self.isOP(user, room), user[0] )
								
								if (i == 40 ):
									self.socket.send(":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, striped, s) )
									s = ""
									i = 0
							
							#if s.find(self.kernel.nick) == -1:
							s = "%s%s%s " %(s,self.isOP((self.kernel.nick,""),room),self.kernel.nick)
														
							self.socket.send(":%s 353 %s = #%s :%s\n" %(self.kernel.me, self.kernel.nick, striped, s) )
							self.socket.send(":%s 366 %s #%s :End of /NAMES list.\n" %(self.kernel.me, self.kernel.nick, striped) )					
							return 1

					self.socket.send(":%s 403 %s #%s :No such channel\n" %(self.kernel.me, self.kernel.nick, striped) )
				#
				# ----- QUIT -----
				#
				elif cmd[0].upper() == "QUIT":
					for room in self.kernel.rooms:
						self.part(room.room)
					self.connection = False
				#
				# ----- AWAY -----
				#
				elif cmd[0].upper() == "AWAY" :
				    self.socket.send(":%s 305 :You are no longer marked as being away\n" %self.kernel.nick )

				#
				# ----- SET -----
				#
				elif cmd[0].upper() == "SET" and len(cmd) >= 2:
					send = False
					if cmd[1].upper() == "IDLER":
						try:
							num = int(cmd[2])
							if num > 250 or num == 0:
								self.kernel.idle_interval = num
								if num:
									message = "Idle interval nastaven na %s sekund." %(num)
								else:
									message = "Idler deaktivovan"
							else:
								message = "Idle interval musi byt vetsi nez 250"
						except:
							message = "Parametr musi byt cislo."
						send = True
					elif cmd[1].upper() == "GIRLS_HIGHLIGHTING":
						if len(cmd[2]) == 1:
							try:
								num = int(cmd[2])
							except:
								self.socket.send(":%s 421 %s Hodnota musi byt 1 nebo 0!\n" %(self.kernel.me, self.kernel.nick))
							if num == 0 or num == 1:
								self.kernel.girls_highlighting = num
								self.setGirlsPrefix()
								if num == 0:
									 self.socket.send(":%s 421 %s Zvyrazneni slecen vypnuto :)\n" %(self.kernel.me, self.kernel.nick))
								else:
									 self.socket.send(":%s 421 %s Zvyrazneni slecen zapnuto :)\n" %(self.kernel.me, self.kernel.nick))
							else:
								self.socket.send(":%s 421 %s Hodnota musi byt 1 nebo 0!\n" %(self.kernel.me, self.kernel.nick))
					elif cmd[1].upper() == "REWRITE_PROTOCOLS":
						if len(cmd[2]) == 1:
							try:
								num = int(cmd[2])
								if num == 0 or num == 1:
									self.kernel.rewrite_protocols = num
									if num == 0:
										 self.socket.send(":%s 421 %s Prepisovani protokolu vypnuto.\n" %(self.kernel.me, self.kernel.nick))
									else:
										 self.socket.send(":%s 421 %s Prepisovani protokolu zapnuto.\n" %(self.kernel.me, self.kernel.nick))
								else: raise
							except:
								self.socket.send(":%s 421 %s Hodnota musi byt 1 nebo 0!\n" %(self.kernel.me, self.kernel.nick))
					
					elif cmd[1].upper() == "IDLER_STR":
						idler = ' '.join(cmd[2:])
						if "|" not in idler:
							self.kernel.idler_str = [idler, idler]
							message = "Zprava jednoducheho idleru zmenena na: %s" %(idler)
						else:
							idler_sliced = idler.split("|", 1) # max. na dva kousky
							self.kernel.idler_str = [idler_sliced[0], idler_sliced[1]]
							message = "Zprava dvojiteho idleru zmenena na: [%s|%s]" %(idler_sliced[0], idler_sliced[1])
						for room in self.kernel.rooms:
							room.idler_str = self.kernel.idler_str
						
						send = True
						
					### Orezavani diakritiky
					elif cmd[1].upper() == "ASCII":
						try:
							num = int(cmd[2])
							if num not in [0, 1, 2, 3]:
								raise
							self.kernel.asciionly = num
							if self.kernel.asciionly == 0:
								message = "Filtr diakritiky deaktivovan."
							elif self.kernel.asciionly == 1:
								message = "Filtr diakritiky aktivovan a nastaven na veskerou komunikaci."
							elif self.kernel.asciionly == 2:
								message = "Filtr diakritiky aktivovan a nastaven na odchozi komunikaci."
							elif self.kernel.asciionly == 3:
								message = "Filtr diakritiky aktivovan a nastaven na prichozi komunikaci."
						except:
							message = "SET ASCII cislo - nastaveni filtru diakritiky: 0 = vypnout; 1 = filtrovat vse; 2 = filtrovat pouze odchozi; 3 = filtrovat pouze prichozi"
						send = True
					elif cmd[1].upper() == "TIMER":
						try:
							num = int(cmd[2])
							self.kernel.timer = num
							message = "Prodleva mezi aktualizacemi nastavena na %s sekund." %(num)
						except:
							message = "SET TIMER cislo - nastaveni prodlevy mezi aktializaci chatu, aktualni hodnota: %s" %(self.kernel.timer)
						send = True
					elif cmd[1].upper() == "CRYPTO":
						try:
							num = int(cmd[2])
							self.kernel.crypto = num
							if num == 1:
								self.kernel.cryptokey = ' '.join(cmd[3:])
								message = "Zapinam crypto backend, klic: %s" %(self.kernel.cryptokey)
							elif num == 0:
								message = "Vypinam crypto"
							else:
								raise
						except:
							message = "Crypto backend k sifrovani textu. /quote set crypto 1 KLIC = zapne backend a nastavi klic; /quote set crypto 0 to vypne. Text k sifrovani musi zacinat teckou, k desifrovani dvema."
						send = True
					elif cmd[1].upper() == "SMILES":
						try:
							num = int(cmd[2])
							if num in [0, 1]:
								self.kernel.smiles = num
							else:
								raise
							if num == 1:
								message = "Orezavam smailiky bot-friendly"
							elif num == 0:
								message = "Orezavam smajliky defaultne"
						except:
							message = "0 = bezne orezavani smailiku; 1 = bude vypisovat jen :CISLO: (vhodne pro roboty)"
						send = True
					elif cmd[1].upper() == "URLS":
						try:
							num = int(cmd[2])
							if num in [0, 1]:
								self.kernel.urls = num
							else:
								raise
							if num == 1:
								message = "Menim http odkazy na h77p a zpet"
							elif num == 0:
								message = "Ignoruju http odkazy"
						except:
							message = "1 = bude menit http odkazy na h77p a naopak; 0 = odkazum nic neudela"
						send = True
					elif cmd[1].upper() == "CHARSET":
						try:
							charset = cmd[2].lower()
							try:
								self.kernel.charset = charset
								message = "Znakova sada nastavena na %s" %(charset)
								
								"test".encode(charset)
							except LookupError:
								message = "Znakova sada %s neni podporovana systemem, na kterem bezi lidegw." %(charset)
							
						except:
							message = "Nastavi znakovou sadu pro komunikaci s klientem. Aktualni znakova sada je %s" %(self.kernel.charset)
						send = True
					else:
						self.socket.send(":%s 421 %s SET->%s :Unknown command.\n" %(self.kernel.me, self.kernel.nick, cmd[1]) )
					if send and message:
						self.socket.send(":%s 421 %s %s\n" %(self.kernel.me, self.kernel.nick, message))

				#
				# ----- LideCmd -----
				#
				# TODO: pokud se najde zpusob, jak posilat RID v /quote prikazu, tak tohle dodelame :D
				#elif cmd[0].upper() == "LIDECMD" and len(cmd) >= 2:
				#	if cmd[1].upper() == "CLS":
				#		self.sendText("/cls", cmd[1].lstrip('#'))
				#	elif cmd[1].upper() == "UNKICK" and len(cmd) >= 3:
				#		self.sendText("/unkick " + cmd[2], cmd[1].lstrip('#'))

				#
				# ----- WHO -----
				#
				elif cmd[0].upper() == "WHO" and len(cmd) == 2 :
					if cmd[1][0] == "#" :
						striped = cmd[1].lstrip('#')
                   				for room in self.kernel.rooms:

							if room.room == striped:
								room.users = self.getChannelUsers(room.room)

								for user in room.users:
									self.socket.send(":%s 352 %s #%s %s %s %s %s H%s :0 %s user\n" %(self.kernel.me, self.kernel.nick, striped, self.hash(user[0],"",2), self.hash(user[0],"",1), self.kernel.me, user[0], self.isOP(user,self.kernel.room), self.kernel.me) )
					else:
						log(cmd[1].find('#'), 1)
					self.socket.send(":%s 315 %s %s :End of /WHO list.\n" %(self.kernel.me, self.kernel.nick, cmd[1]) )
				#
				# ----- WHOIS -----
				#
				elif cmd[0].upper() == "WHOIS" and len(cmd) >= 2:
					#for c in cmd[1:]
					c = cmd[1]
					s = ""
					try:
						d = self.getWhois(c)
					except:
						return 0

					for line in d:
						s = s + ":NOTICE %s\n" %(line)
						# konec listu
					s = s + ":%s 318 %s %s :End of /WHOIS list.\n" %(self.kernel.me, self.kernel.nick, c)
					self.socket.send(s)
				#
				# ----- INFO -----
				#
				elif cmd[0].upper() == "INFO":
					if len(cmd) >= 2:
						rid = cmd[1]
						self.getInfo(rid)
					else:
						self.getInfo()
				#
				# ----- ISON -----
				#
				elif cmd[0].upper() == "ISON" and len(cmd) >= 2:
					print cmd
					if cmd[1][0] == ":":
						cmd[1] = cmd[1][1:] # odstranění tečky
					self.isON(cmd[1:])
				
				#
				# ----- KICK -----
				#
				elif cmd[0].upper() == "KICK" and len(cmd) >= 2:
					if len(cmd) == 3:
						self.sendText("/kick "+cmd[2], cmd[1].lstrip('#')) # nick, room
					elif len(cmd) > 3:
						reason = ' '.join(cmd[3:])[1:] # dvojtecku nechceme
						self.sendText("/kick %s %s" %(cmd[2], reason), cmd[1].lstrip('#')) # nick, room
				#
				# ----- OTHER -----
				#
				else :
					if cmd[0] != "":
						self.socket.send(":%s 421 %s :%s Unknown command!\n" %(self.kernel.me, self.kernel.nick, cmd[0]) )
						log(data, 1)

		return True

	# vraceni chybovych hlaseni
	def error(self):
		return self.kernel.ERROR

# vlakno na tahani zprav
class getMessages(threading.Thread):
	def __init__(self, inst, socket):
		threading.Thread.__init__(self)
		self.inst = inst
		#self.socket = socket
		self.running = True
		log("getm, init")
	def run(self):
		"""Metoda zpracovava pole zprav"""
		# cela procedura je cyklus
		while self.running and self.inst.connection:
			log("getm, cycle")
			if len(self.inst.kernel.rooms) == 0:
				log("getm, not joined yet")
				time.sleep(5)
				continue
			if not self.inst.connection:
				return False
			
			ignor = []
			for croom in self.inst.kernel.rooms:
				log("getm, processing %s" %(croom.room))
				try:
					# V regulernich requestech je nejaky nahodny cislo (v JS: Math.ceil(Math.random()*9999)). Napodobime to, vcetne predchoziho cisla v refereru.
					self.inst.kernel.opener.addheaders.append(('Referer', '%s?akce=win_js&room_ID=%s&last=%s&%s' %(self.inst.kernel.room_url, croom.room, croom.last, self.inst.kernel.randomnumber)))
					self.inst.kernel.randomnumber = random.randrange(0, 9999)
					r = self.inst.kernel.urlopen("%s?akce=win_js&room_ID=%s&auth=&last=%s&%s" %(self.inst.kernel.room_url, croom.room, croom.last, self.inst.kernel.randomnumber))
					# takže :D budem tady číhat na cookie se změnou haška, pokud bude, tak ji chytneme a přijmeme za vlastní.
					# Pokud ne, tak budem dělat že se nic nestalo. Ale ona stejně přijde. -TT
					try:
						self.inst.kernel.auth = re.findall("ds=(.+);path", r.headers.getheader("Set-cookie"))[0]
						self.inst.updateCookie()
						log("getm, updated cookie")
					except:
						if traceback:
							traceback.print_exc()
				except:
					if traceback:
						traceback.print_exc()
					self.inst.socket.send("ERROR :Timeout while getting messages.\n")
					break
				
				s = r.read()
				# debug: ukladame do logu
				if debug:
					temp_log = open("lidegw:lidecz-input.log", "a")
					temp_log.write("%s\n--------\n" %(s))
					temp_log.close()
					del temp_log
				
				if re.search(r'<META HTTP-EQUIV="Refresh" CONTENT="1; URL=room.fcgi\?akce=out.+">', s):
					try:
						rt = self.inst.kernel.urlopen(self.inst.kernel.room_url+"?akce=out&room_ID=%s&hashId=%s" %(croom.room, room.hashid_part))
						rt = rt.read()
						
					except:
						if traceback:
							traceback.print_exc()
						self.inst.socket.send("ERROR :Timeout while outdoing room.\n") 
						self.inst.part(croom.room)
						break
					
					try:
						#adm = re.findall(r'<p><P>Vstup.+<P>.+"warn">(.+)</span>.+<P>(.+)<span.+</P></p>',rt)[0]
						#kick = re.findall('<p><P>Vstup odm.tnut kv.li vykopnut.. N.vrat je mo.n. za <span class="red">(\d+?)</span> minut.</P> <P>Byl jste vykopnut spr.vcem <span class="red">(.+?)</span></P> <P>Vzkazuje V.m: <span class="red">(.+?)</span></P></p>', s)
					
						#if len(adm) == 2 :
							#self.inst.socket.send(":%s KICK #%s %s :%s\n" %( self.inst.hash(adm[0],croom.room), croom.room, self.inst.kernel.nick, adm[1]) )
							#self.inst.part(croom.room)
							#break
						#else:
							#adm = re.findall(r'<p><P>.+</P></p>',rt)
							#self.inst.socket.send(":%s KICK #%s %s :%s\n" %(self.inst.kernel.me, croom.room, self.inst.kernel.nick, re.sub('<.*?>','',adm)) )
							#self.inst.part(croom.room)
							#break
						kick_s = self.inst.kernel.urlopen("%s?room_ID=%s" %(self.inst.kernel.room_url, croom.room)).read()
						kick = re.findall('<p><P>Vstup odm.tnut kv.li vykopnut.. N.vrat je mo.n. za <span class="red">(\d+?)</span> minut.</P> <P>Byl jste vykopnut spr.vcem <span class="red">(.+?)</span></P> <P>Vzkazuje V.m: <span class="red">(.*?)</span></P></p>', kick_s)[0]
						if len(kick) == 3:
							self.inst.socket.send(":%s KICK #%s %s :%s\n" %(self.inst.hash(kick[1], croom.room), croom.room, self.inst.kernel.nick, "Doba: %s; Duvod: %s" %(kick[0], kick[2])))
							self.inst.part(croom.room)
						else:
							raise # nebo by to mohlo mit i jinej pocet nez tri ? Ukaze az cas...
					except:
						self.inst.socket.send(":%s KICK #%s %s :Byl jsi vyhozen pro neaktivitu.\n" %(self.inst.kernel.me, croom.room, self.inst.kernel.nick) )
						self.inst.part(croom.room)
						break
				
				pattren = re.compile("top.a4[(](.+),'.+','(.+)','(.+)','',.+,.+,.+,'','(.+)'.+")
				
				#datos = re.findall(pattren,s)
				
				if int(croom.last) > 0:
				#if True: # škoda
					#
					# ------ [ MAIN MESSAGE LOOP ] -----
					#
					for cmsg in self.inst.msgDoPushq(s, ignor):
						tosend = ""
						if True:
							if cmsg.type == 0:
								tosend = ":%s NOTICE #%s :%s\n" %(self.inst.kernel.me, croom.room, cmsg.text)
							elif cmsg.type == 1:
								# tahle cast prida usera do kernel.rooms, kvuli sexum v hashi
								pair_updated = False
								for pair_id in range(len(self.inst.kernel.room.users)):
									pair = self.inst.kernel.room.users[pair_id]
									if pair[0].upper() == cmsg.target.upper():
										#print pair, "->", (cmsg.target, cmsg.nick)
										self.inst.kernel.room.users[pair_id] = (cmsg.target, cmsg.nick)
										pair_updated = True
								if not pair_updated:
									self.inst.kernel.room.users.append((cmsg.target, cmsg.nick))
								
								tosend = ":%s JOIN #%s\n" %(self.inst.hash(cmsg.target,""), croom.room)
								pretend = self.inst.isOP((cmsg.target,cmsg.nick),croom)
								
								if pretend == "@":
									tosend = tosend + ":%s MODE #%s +o %s\n" %(self.inst.kernel.me, croom.room, cmsg.target)
								elif pretend == "+":
									tosend = tosend + ":%s MODE #%s +v %s\n" %(self.inst.kernel.me, croom.room, cmsg.target)
								elif pretend == "%":
									tosend = tosend + ":%s MODE #%s +h %s\n" %(self.inst.kernel.me, croom.room, cmsg.target)
							elif cmsg.type == 2:
								# aktualizuju seznam OP
								self.inst.updOPs(croom)
								tosend = ":%s PART #%s :%s\n" %(self.inst.hash(cmsg.target,""), croom.room, cmsg.text)
							elif cmsg.type == 3:
								tosend = ":%s PRIVMSG %s :%s\n" %(self.inst.hash(cmsg.nick,""), cmsg.nick, cmsg.text)
								ignor.append(cmsg.nick+cmsg.text)
							elif cmsg.type == 4:
								tosend = ":%s NOTICE %s :%s\n" %(self.inst.hash(cmsg.nick,""), self.inst.kernel.nick, cmsg.text)
							elif cmsg.type == 5:
								tosend = ":%s PRIVMSG #%s :%s\n" %(self.inst.hash(cmsg.nick,""), croom.room, cmsg.text)
							elif cmsg.type == 6:
								tosend = ":%s KICK #%s %s :%s\n" %(self.inst.hash(cmsg.nick,""), croom.room, cmsg.target, cmsg.text)
							elif cmsg.type == 7:
								tosend = ":%s MODE #%s +h %s\n" %(cmsg.nick, croom.room, cmsg.target)
								# odstranime staryho half-opa
								if croom.op:
									self.inst.socket.send(":%s MODE #%s -h %s\n" %(cmsg.nick, croom.room, croom.op))
								# aktualizujem seznam OPs
								self.inst.updOPs(croom)
							elif cmsg.type == 8:
								tosend = ":%s MODE #%s +h %s\n" %(self.inst.kernel.me, croom.room, cmsg.target)
						if tosend:
							if self.inst.kernel.charset not in ["latin2", "iso-8859-2", "iso8859-2"]:
								tosend = self.inst.recode(tosend, 1)
							self.inst.socket.send(tosend)
							old = []
					#
					# ------ LAST LINE -----
					#
					try:
						croom.last = re.findall("last_ID=(\d+)", s)[-1]
					except(IndexError):
						# nekdy se asi nepodari ziskat stranku, tak to proste prejdeme, jako ze se nic nestalo
						# chyba bude pocitam na strane lide.cz (pretizenost serveru)
						if traceback:
							traceback.print_exc()

					# idler
					myTime = time.time()
					if (myTime - croom.last_idle) >= self.inst.kernel.idle_interval and self.inst.kernel.idle_interval != 0:
						self.inst.socket.send(":%s NOTICE #%s :Idler - [ %s ]\n" %(self.inst.kernel.me, croom.room, md5.new(str(myTime)).hexdigest()))
						croom.last_idle = myTime
						self.inst.sendText(croom.idler_str[0], croom.room)
						croom.idler_str = [croom.idler_str[1], croom.idler_str[0]] # prohodime idler
				else:
					croom.last = re.findall("last_ID=(\d+)", s)[-1]
			time.sleep(self.inst.kernel.timer)
		log("getm, shutdown")

# vlakno pro klienty
class IRCClient(threading.Thread):
	def __init__(self, socket, address):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address
		self.running = True
		log("ircc, init")
	def run(self):
		log("ircc, start")
		log("Nove spojeni z %s" %(self.address[0]), 1)
		
		myInst = Lide(self.socket, self.address[0])
		
		while self.running:
			log("ircc, cycle")
			myTime = int(time.time())
			
			try:
				ircdata = myInst.socket.recv(2**13)
				if (myInst.parseIRCData(ircdata,myTime) == 2):
					return 0
			except:
				log("Spojeni s %s zavreno." %(self.address[0]), 1)
				if traceback:
					traceback.print_exc()
				myInst.connection = False
				for room in myInst.kernel.rooms:
					myInst.part(room.room)
				log("ircc, shutdown")
				return False
			
			# pokud neni nick "" (nastaven defaultne) tak uz sem dostal i heslo
			if myInst.kernel.nick != "" and not myInst.kernel.logged:
				log("ircc, attempting login")
				try:
					# pokusim se zalogovat do systemu
					myInst.login()
					myInst.kernel.logged = True
					log("ircc, login succeeded")
					# WELCOME MESSAGE
					myInst.socket.send(world.welcome %(myInst.kernel.me, myInst.kernel.nick, myInst.socket.getsockname()[0], version_, myInst.kernel.ticket, myInst.kernel.auth))
					# End of MOTD
					myInst.socket.send(":%s 376 %s :End of MOTD\n" %(myInst.kernel.me, myInst.kernel.nick))
					# messages
					world.vlakna.append(getMessages(myInst, self.socket))
					world.collector.start_threads()
				
				except:
					# pokud se vyskytne chyba tak ji vypisu
					log("ircc, login failed")
					if traceback:
						traceback.print_exc()
					try:
						myInst.socket.send(myInst.error())
					except:
						pass
					# zavru spojeni s klientem
					myInst.socket.close()
					# ukoncim vlakno pro spojeni
					myInst.connecteion = 0
					return False
		log("ircc, shutdown")

# vytvorim socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# a nasloucham na portu PORT

s.bind(('', PORT))
s.listen(50)

# nahodime kolektor, pokud uz nebezi
if not world.collector:
	world.collector = Collector()
	world.collector.start()

log("Lidegw %s, nasloucham na portu %s" %(version_, PORT), 1)

# main LOOP() ;))
while world.collector.running:
	try:
		# prijimam vsechna spojeni
		connection, address = s.accept()
		
		# po pripojeni hodim vlakno do zasobniku, pokud mam misto
		if len(world.vlakna) <= 378: # limit threading je 380, ale my chceme na kazdy spojeni 2 vlakna
			world.vlakna.append(IRCClient(connection, address))
		else:
			connection.close()
			log("Vlaknovy prostor zaplnen, odmitam dalsi spojeni. (TODO: fork())")
		
		world.collector.start_threads()
		
	except(KeyboardInterrupt, EOFError):
		world.collector.running = False
		s.close()
		log("Vypinam...", 1)
		break