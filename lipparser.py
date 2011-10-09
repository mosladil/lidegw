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
		self.registrace = []
		self.posledni_prihlaseni = []
		self.prochatovano = []
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
				[['Registrace:',self.registrace],
				['Posledn\xed p\xf8ihl\xe1\xb9en\xed:',self.posledni_prihlaseni],
				['Prochatov\xe1no:',self.prochatovano],
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
		from urllib import urlopen, pathname2url
		# osetreni nicku pro pripadne specialni znaky
		# (FIXME: lepsi by bylo rovnou vyhodit chybu, kdyby tam nejaky specialni znak byl a jeste kontrolovat, jestli nema nick vic nez 40 znaku)
		self.nick = pathname2url(self.nick)
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
		#@-> self.online - OK
		if re.search(r'U\xbeivatel (.*?) nechod\xed na Lide.cz',self.profile):
			print '> U\xbeivatel '+self.nick+' nechod\xed na Lide.cz'
			return 0
		elif re.search(r'na.slu\xbeb\xec.<strong>chat',self.profile):
			self.online = ['na slu\xbeb\xec chat']
		elif re.search(r'na.slu\xbeb\xec.<strong>profil',self.profile):
			self.online = ['na slu\xbeb\xec profil']
		elif re.search(r'Online:</span>', self.profile):
			self.online = re.findall(r'Online:</span>\s*(.*?)\s*</li>', self.profile)
			try:
				self.online[0] = re.sub(r'<.*?>', '', self.online[0])
			except IndexError:
				pass
			if re.search(r'room_ID=', self.profile):
				ids_roomnames = re.findall(r'room_ID=(\d+)".>(.+?)</a>', self.profile)
				for dvojice in ids_roomnames:
					self.online.append('%s [%s]' %(dvojice[1], dvojice[0]))
                else:
			self.online = ['informace nen\xed dostupn\xe1']
		#@-> self.adresa_profilu - OK
		self.adresa_profilu = ['http://www.lide.cz/'+self.nick]
		#@-> self.jmeno - OK
		self.jmeno = re.findall(r'<strong>Jm\xe9no:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.vek - OK
		self.vek = re.findall(r'([\d|\?]* let)',self.profile)
		#@-> self.pohlavi - OK
		poh = re.findall(r'img/common/ico-(\w{1,7}).gif',self.profile)
		try:
			if poh[0] == 'M': self.pohlavi = 'Mu\xbe'
			elif poh[0] == 'F': self.pohlavi = '\xaeena'
			else: self.pohlavi = 'nezn\xe1m\xe9'
		except IndexError:
			print self.nick
		#@-> self.bydliste - OK
		self.bydliste = re.findall(r'let\s+,\ (.*)\s+',self.profile)
		#@-> self.icq - OK
		self.icq = re.findall(r'<strong>ICQ:</strong>.(.+)\s',self.profile)
		#@-> self.www - OK
		self.www = re.findall(r'<strong>WWW:</strong>.<a href="/redir.fcgi\?(.+)".target',self.profile)
		#@-> self.telefon - OK
		self.telefon = re.findall(r'<strong>Telefon:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.registrace - OK
		self.registrace = re.findall(r'<strong>Registrace:</strong>\s*(\d{1,2}\.\d{1,2}\.\d{4})',self.profile)
		#@-> self.posledni_prihlaseni - OK
		self.posledni_prihlaseni = re.findall(r'<strong>Aktivn\xed:</strong>\s*(.+)\s*</li>',self.profile)
		#@-> self.prochatovano - OK
		self.prochatovano = re.findall(r'<strong>Prochatov\xe1no:</strong>.(.*)</li>',self.profile)
		#@-> self.pocet_zobrazeni - OK
		self.pocet_zobrazeni = re.findall(r'<strong>Profil zobrazen:</strong>.(.*)</li>',self.profile)
		#@-> self.stav - OK
		self.stav = re.findall(r'<strong>Stav:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.zamestnani - OK
		self.zamestnani = re.findall(r'<strong>Zam\xecstn\xe1n\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.vzdelani - OK
		self.vzdelani = re.findall(r'<strong>Vzd\xecl\xe1n\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.jazyk - OK
		self.jazyk = re.findall(r'<strong>Jazyky:</strong>(.*?)</li>',self.profil)
		#@-> self.vyska - OK
		self.vyska = re.findall(r'<strong>V\xfd\xb9ka:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.hmotnost - OK
		self.hmotnost = re.findall(r'<strong>Hmotnost:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.postava - OK
		self.postava = re.findall(r'<strong>Postava:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.barva_oci - OK
		self.barva_oci = re.findall(r'<strong>Barva o\xe8\xed:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.barva_vlasu - OK
		self.barva_vlasu = re.findall(r'<strong>Barva vlas\xf9:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.povaha - BUG
		self.povaha = re.findall(r'<strong>Moje povaha:</strong>(.*?)</li>',self.profil)
		# funkcni, ale slozitejsi mechanismus ziskavani seznamu povahovych rysu - mozna se nekde bude hodit, tak ho zatim nemazu
		#try:
		#	partpov = re.findall(r'<strong>Moje povaha:</strong>(.*?)</li>', self.profile, re.DOTALL)
		#	self.povaha = [', '.join(re.findall(r'\s*(.*?)[,\n]',partpov[0])[:-1])]
		#except IndexError:
		#	pass
		#@-> self.pohled_na_svet - OK
		self.pohled_na_svet = re.findall(r'<strong>Pohled na sv\xect:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.otevrenost - OK
		self.otevrenost = re.findall(r'<strong>Otev\xf8enost:</strong>\s*(.*)\s*</li>',self.profile)
		#@-> self.zajmy - OK
		self.zajmy = re.findall(r'<strong>Z\xe1jmy:</strong>(.*?)</li>',self.profil)
		#@-> self.sport - OK
		self.sport = re.findall(r'<strong>Sport:</strong>(.*?)</li>',self.profil)
		#@-> self.literatura - OK
		self.literatura = re.findall(r'<strong>Literatura:</strong>(.*?)</li>',self.profil)
		#@-> self.hudba - OK
		self.hudba = re.findall(r'<strong>Hudba:</strong>(.*?)</li>',self.profil)
		#@-> self.zvire - OK
		self.zvire = re.findall(r'<strong>Zv\xed\xf8e:</strong>(.*?)</li>',self.profil)
		#@-> self.bydlimkde
		self.bydlimkde = re.findall(r'<strong>Bydl\xedm:</strong>\s*(.*)\s*</li>',self.profile)
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
		self.unp_info = re.findall(r'<p class="introduction">(.*?)',self.profile)
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
