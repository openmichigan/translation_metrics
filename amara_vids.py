from bs4 import BeautifulSoup as bsoup 
import json, requests, re, datetime, urllib



class AmaraAccount(object):
	def __init__(self, username):
		self.username = username
		self.base = "http://www.amara.org/en/profiles/videos/%s/" % (self.username)

	def num_acct_pages(self):
		"""This should return an integer that is the number of pages of vids in the account"""
		#print self.base #debug
		try:
			sp = bsoup(requests.get(self.base).text)
			#print sp #debug
			num = sp.find('a',href='?page=last').text
			return int(num)
		except:
			return 2 # if there's only one page, there's no 'last' -- should only go through 1 (range(1,1))

	def get_links(self):
		r = requests.get("%s?page=last" % (self.base)).text
		# <a rel="next" href="?page=last">15</a>
		#rp = requests.get(self.base).text
		soup = bsoup(r)
		# this no longer... gets links, because that happened in merge resolve, so that needs fixing TODO TODO


		# try:
		# 	numpgs = soup.find('a', href='?page=last').text # want the a where the href is ?page=last, the inner text, turned to int, yay html
		# 	return int(numpgs)
		# except:
		# 	return 2 # only want it to go through 1, so that will make the range work


class RelevantVideos(object):
	"""Aggregates together information from a bunch of AmaraAccount objects"""
	def __init__(self,acct_1=None,acct_2=None,acct_3=None): # each acct should be a var holding an AmaraAcct obj
		self.ids = {} # initialize with empty dict
		self.vid_patt = re.compile(r"/videos/([a-zA-Z0-9]{12})")
		self.coincidental_links = ["openmichigan"] # add more as necessary, seems unlikely
		self.acctobjs = []
		if acct_1 is not None:
			self.acctobjs.append(acct_1)
		if acct_2 is not None:
			self.acctobjs.append(acct_2)
		if acct_3 is not None:
			self.acctobjs.append(acct_3)
		# might later have a method to add another acct, now (04/2014) might only need 2 or 3
		for ob in self.acctobjs:
			ob.get_links()
		self.manage_links()

	def manage_lastpage_links(self):
		for ab in self.acctobjs:
			ab.get_links()
			for l in ab.links:
				test = re.search(self.vid_patt,l['href'])
				if test is not None:
					eyedee = test.groups()[0]
					if eyedee not in self.ids:
						self.ids[eyedee] = 1 # entering it into dict
					else:
						continue
				else:
					continue

	def manage_remainder_links(self):
		for ak in self.acctobjs:
			for i in range(1,ak.num_acct_pages()):
				burl = ak.base + "?page={}".format(i)
				rb = requests.get(burl).text
				sp = bsoup(rb)
				lks = sp.findAll('a')
				for l in lks:
					tst = re.search(self.vid_patt, l['href'])
					if tst is not None:
						ed = tst.groups()[0]
						if ed not in self.ids:
							self.ids[ed] = 1
						else: continue
					else:
						continue

	def manage_links(self): # aggregate
		self.manage_lastpage_links()
		self.manage_remainder_links()

	def write_file(self):
		"""Write txt file with video ids if necessary -- or use list in object"""
		now = str(datetime.datetime.now())
		fname = "OM_amara_ids_{}.txt".format(now[:10]) # to instance variablize or not to instance variablize
		f = open(fname, "w")
		for k in self.ids:
			if k not in self.coincidental_links: 
				f.write(k+"\n") # write the id to a file
		f.close()


if __name__ == '__main__':

	# testing testing

	a = AmaraAccount("openmichigan.video")
	k = AmaraAccount("kludewig")
	print a.username
	print a.base
	print a.num_acct_pages()

	foo = RelevantVideos(a,k)
	#bar = RelevantVideos(k)

	foo.manage_links()
	print foo.ids


# if __name__ == '__main__':
# 	am = AmaraAccount('openmichigan.video')
# 	am.get_links() # this is important, should do this in relvids
# 	print am.num_acct_pages()
# 	at = RelevantVideos(am)
# 	at.manage_lastpage_links()
# 	print at.ids

