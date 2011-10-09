# This module is used by LIPP and LideGW
#
# @@@ Coded by p4t0k @@@
#
# e-mail: p4t0kk@gmail.com
#
#

import re

class myparser:
	"""nastavi implicitni hodnoty promennym a vola getvalues, ktera se pokusi ziskat informace o uzivateli"""
	def __init__(self,nick):
		self.version = 0.5
		self.nick = str(nick)
		self.__baseaddress = 'http://profil.lide.cz/profile.fcgi?akce=profile&user='
		self.adresa_profilu = []
		self.online = []
		self.vek = []
		self.pohlavi = []
		self.bydliste = []
		self.icq = []
		self.www = []
		self.jmeno = []
		self.telefon = []
		self.konto_zalozeno = []
		self.posledni_prihlaseni = []
		self.prochatovano = []
		self.autorizace = []
		self.pocet_zobrazeni = []
		self.stav = []
		self.zamestnani = []
		self.vzdelani = []
		self.jazyk = []
		self.vyska = []
		self.hmotnost = []
		self.postava = []
		self.barva_oci = []
		self.barva_vlasu = []
		self.povaha = []
		self.pohled_na_svet = []
		self.otevrenost = []
		self.zajmy = []
		self.sport = []
		self.literatura = []
		self.hudba = []
		self.zvire = []
		self.bydlimkde = []
		self.bydlimskym = []
		self.vztah = []
		self.hledam = []
		self.deti = []
		self.orientace = []
		self.koureni = []
		self.alkohol = []
		self.sex = []
		self.drogy = []
		self.intro_info = []
		self.unp_info = []
		self.postava_info = []
		self.povaha_info = []
		self.konicky_info = []
		self.domacnost_info = []
		self.seznameni_info = []
		self.zavislosti_info = []
		# kvuli funkci _komentar musime deklarovat self.profil a self.profile uz v konstruktoru tridy
		self.profil = ''
		self.profile = ''
		# zavolame nas parser
		self.getvalues()
		# nasazime do matice
		self.lippvars = {
			'Z\xe1kladn\xed \xfadaje': 
				[['Adresa profilu:',self.adresa_profilu],
				['On-line:',', '.join(self.online)],
				['Jm\xe9no:',self.jmeno],
				['Telefon:',self.telefon],
				['V\xeck:',self.vek],
				['Pohlav\xed:',self.pohlavi],
				['Bydli\xb9t\xec:',self.bydliste],
				['ICQ:',self.icq],
				['WWW:',self.www],
				['komentar',self.intro_info]],
			'Statistick\xe9 \xfadaje':
				[['Konto zalo\xbeeno:',self.konto_zalozeno],
				['Posledn\xed p\xf8ihl\xe1\xb9en\xed:',self.posledni_prihlaseni],
				['Prochatov\xe1no:',self.prochatovano],
				['Autorizace:',self.autorizace],
				['Profil zobrazen:',self.pocet_zobrazeni]],
			'\xdadaje na profil':
				[['Stav:',self.stav],
				['Zam\xecstn\xe1n\xed:',self.zamestnani],
				['Vzd\xecl\xe1n\xed:',self.vzdelani],
				['Jazyk:',self.jazyk],
				['komentar',self.unp_info]],
			'Postava':
				[['V\xfd\xb9ka:',self.vyska],
				['Hmotnost:',self.hmotnost],
				['Postava:',self.postava],
				['Barva o\xe8\xed:',self.barva_oci],
				['Barva vlas\xf9:',self.barva_vlasu],
				['komentar',self.postava_info]],
			'Povaha':
				[['Povaha:',self.povaha],
				['Pohled na sv\xect:',self.pohled_na_svet],
				['Otev\xf8enost:',self.otevrenost],
				['komentar',self.povaha_info]],
			'Kon\xed\xe8ky':
				[['Z\xe1jmy:',self.zajmy],
				['Sport:',self.sport],
				['Literatura:',self.literatura],
				['Hudba:',self.hudba],
				['Zv\xed\xf8e:',self.zvire],
				['komentar',self.konicky_info]],
			'Dom\xe1cnost':
				[['Bydl\xedm:',self.bydlimkde],
				['Bydl\xedm s:',self.bydlimskym],
				['komentar',self.domacnost_info]],
			'Sezn\xe1men\xed':
				[['Vztah:',self.vztah],
				['Hled\xe1m:',self.hledam],
				['D\xecti:',self.deti],
				['Sexu\xe1ln\xed orientace:',self.orientace],
				['komentar',self.seznameni_info]],
			'Z\xe1vislosti':
				[['Kou\xf8en\xed:',self.koureni],
				['Alkohol:',self.alkohol],
				['Drogy:',self.drogy],
				['Sex:',self.sex],
				['komentar',self.zavislosti_info]]
				}
	def getvalues(self):
		"""parsuje informace z profilu na lide.cz"""
		from urllib import urlopen
		# pokusime se stahnout stranku s profilem a overime, jestli uzivatel existuje
		try:
			prof = urlopen(self.__baseaddress+self.nick)
			self.profile = prof.read()
			prof.close()

		except IOError:
			print '> Chyba socketu (mozna jste za proxy, nebo prilis striktnim firewallem)'
			return 1
		try:
			# prohledame dokument jestli v nem neni ze uzivatel neexistuje :D
			if re.search(r'ivatel.*?neexistuje',self.profile):
				raise
		except:
			print '> Nick neexistuje!'
			return 0
		# orezeme stranku s profilem o \n a \t
		self.profil = re.sub('\n','',re.sub('\t','',self.profile))
		#@-> self.online
		if re.search(r'nen\xed v \xbe\xe1dn\xe9 m\xedstnosti ani jinde',self.profile):
			self.online = ['nen\xed v \xbe\xe1dn\xe9 m\xedstnosti ani jinde']
		elif re.search(r'U\xbeivatel (.*?) nechod\xed na Lide.cz',self.profile):
			print '> U\xbeivatel '+self.nick+' nechod\xed na Lide.cz'
			return 0
		elif re.search(r'na.slu\xbeb\xec.<strong>chat',self.profile):
			self.online = ['na slu\xbeb\xec chat']
		elif re.search(r'na.slu\xbeb\xec.<strong>profil',self.profile):
			self.online = ['na slu\xbeb\xec profil']
		else:
			allrooms = re.findall(r'Online:</span>(.*?)</p>', self.profil)
			ids_roomnames = re.findall(r'room_ID=(\d+)".>(.+?)</a>', allrooms[0])
			for dvojice in ids_roomnames:
				self.online.append('%s [%s]' %(dvojice[1], dvojice[0]))
		#@-> self.adresa_profilu
		self.adresa_profilu = ['http://www.lide.cz/'+self.nick]
		#@-> self.jmeno
		self.jmeno = re.findall(r'<strong>Jm\xe9no:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.vek
		self.vek = re.findall(r'([\d|\?]* let)',self.profile)
		#@-> self.pohlavi
		poh = re.findall(r'img/ico-(.{1,6}).gif',self.profile)
		if poh[0] == 'M': self.pohlavi = 'Mu\xbe'
		elif poh[0] == 'F': self.pohlavi = '\xaeena'
		else: self.pohlavi = 'nezn\xe1m\xe9'
		#@-> self.bydliste
		self.bydliste = re.findall(r'let\s+,\ (.*)\s+',self.profile)
		#@-> self.icq
		self.icq = re.findall(r'<strong>ICQ:</strong>.(.+)\s',self.profile)
		#@-> self.www
		self.www = re.findall(r'<strong>WWW:</strong>.<a href="/redir.fcgi\?(.+)".target',self.profile)
		#@-> self.telefon
		self.telefon = re.findall(r'<strong>Telefon:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.konto_zalozeno
		self.konto_zalozeno = re.findall(r'<strong>Konto.zalo\xbeeno:</strong>\s*(\d{2}\.\d{2}\.\d{4}.\d{2}:\d{2}:\d{2})\s*?(\(.*\))',self.profile)
		#@-> self.posledni_prihlaseni
		self.posledni_prihlaseni = re.findall(r'<strong>Posledn\xed.p\xf8ihl\xe1\xb9en\xed:</strong>\s*<b>(\d{2}\.\d{2}\.\d{4}.\d{2}:\d{2}:\d{2})</b>\s*?(\(.*\))',self.profile)
		#@-> self.prochatovano
		self.prochatovano = re.findall(r'<strong>Prochatov\xe1no:</strong>.(.*)\s*\(<a',self.profile)
		#@-> self.autorizace
		self.autorizace = re.findall(r'<strong>Autorizace:</strong>.(.*)</li>',self.profile)
		#@-> self.pocet_zobrazeni
		self.pocet_zobrazeni = re.findall(r'<strong>Profil zobrazen:</strong>.(.*)</li>',self.profile)
		#@-> self.stav
		self.stav = re.findall(r'<strong>stav:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.zamestnani
		self.zamestnani = re.findall(r'<strong>zam\xecstn\xe1n\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.vzdelani
		self.vzdelani = re.findall(r'<strong>vzd\xecl\xe1n\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.jazyk
		self.jazyk = re.findall(r'<strong>jazyky:</strong>(.*?)</li>',self.profil)
		#@-> self.vyska
		self.vyska = re.findall(r'<strong>v\xfd\xb9ka:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.hmotnost
		self.hmotnost = re.findall(r'<strong>hmotnost:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.postava
		self.postava = re.findall(r'<strong>postava:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.barva_oci
		self.barva_oci = re.findall(r'<strong>barva o\xe8\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.barva_vlasu
		self.barva_vlasu = re.findall(r'<strong>barva vlas\xf9:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.povaha
		self.povaha = re.findall(r'<strong>povaha:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.pohled_na_svet
		self.pohled_na_svet = re.findall(r'<strong>pohled na sv\xect:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.otevrenost
		self.otevrenost = re.findall(r'<strong>otev\xf8enost:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.zajmy
		self.zajmy = re.findall(r'<strong>z\xe1jmy:</strong>(.*?)</li>',self.profil)
		#@-> self.sport
		self.sport = re.findall(r'<strong>sport:</strong>(.*?)</li>',self.profil)
		#@-> self.literatura
		self.literatura = re.findall(r'<strong>literatura:</strong>(.*?)</li>',self.profil)
		#@-> self.hudba
		self.hudba = re.findall(r'<strong>hudba:</strong>(.*?)</li>',self.profil)
		#@-> self.zvire
		self.zvire = re.findall(r'<strong>zv\xed\xf8e:</strong>(.*?)</li>',self.profil)
		#@-> self.bydlimkde
		self.bydlimkde = re.findall(r'<strong>bydl\xedm:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.bydlimskym
		self.bydlimskym = re.findall(r'<strong>bydl\xedm s:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.vztah
		self.vztah = re.findall(r'<strong>vztah:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.hledam
		self.hledam = re.findall(r'<strong>hled\xe1m:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.deti
		self.deti = re.findall(r'<strong>d\xecti:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.orientace
		self.orientace = re.findall(r'<strong>sexu\xe1ln\xed orientace:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.koureni
		self.koureni = re.findall(r'<strong>kou\xf8en\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.alkohol
		self.alkohol = re.findall(r'<strong>alkohol:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.drogy
		self.drogy = re.findall(r'<strong>drogy:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.sex
		self.sex = re.findall(r'<strong>sex:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.intro_info
		self.intro_info = re.findall(r'<p class="introduction">(.*?)</p>',self.profile)
		#@-> self.unp_info
		self.unp_info = self._komentar('.daje.na.profil')
		#@-> self.postava_info
		self.postava_info = self._komentar('Postava')
		#@-> self.povaha_info
		self.povaha_info = self._komentar('Povaha')
		#@-> self.konicky_info
		self.konicky_info = self._komentar('Kon..ky')
		#@-> self.domacnost_info
		self.domacnost_info = self._komentar('Dom.cnost')
		#@-> self.seznameni_info
		self.seznameni_info = self._komentar('Sezn.men')
		#@-> self.zavislosti_info
		self.zavislosti_info = re.findall(r'<h3>Z.vislosti.*?<p>(.+?)</p><div id="adPRclanek"',self.profil)
	def _komentar(self,regexp):
		"""parsuje nektere komentarove promenne (to jsou vsechny promenne s suffixem _info)"""
		try:
			return re.findall(r'<p>(.+?)</p>', re.findall(r'<h3>'+regexp+'.+?<[h/][3d]', self.profile, re.S)[0], re.S)
		except:
			return False
