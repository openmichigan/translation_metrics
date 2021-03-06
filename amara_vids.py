from bs4 import BeautifulSoup as bsoup 
import json, requests, re, datetime, urllib


class AmaraAccount(object):
	"""Represents an account on Amara.org (whose vids/subtitle translations the user is interested in)"""
	def __init__(self, username):
		self.username = username
		self.base = "http://www.amara.org/en/profiles/videos/%s/" % (self.username)

	def num_acct_pages(self):
		"""This should return an integer that is the number of pages of vids in the account"""
		try:
			sp = bsoup(requests.get(self.base).text)
			num = sp.find('a',href='?page=last').text
			return int(num)
		except:
			return 2 # if there's only one page, there's no 'last' -- should only go through 1 (range(1,1))

	def get_links(self):
		"""Assigns all vid links to self.links attribute and returns list of links"""
		r = requests.get("%s?page=last" % (self.base)).text
		soup = bsoup(r)
		lks = soup.findAll('a')
		self.links = lks
		return self.links 


class CourseWithVids(AmaraAccount): # questionable inheritance
	"""object to aggregate videos with potential translations from a a single Open.Michigan course"""
	# problem being: Open.Michigan courses do not link explicitly to the Amara link generally, even when the vids are translated -- avail through YT, diff ids
	def __init__(self,pgpath):
		sp = bsoup("http://open.umich.edu/{}".format(pgpath))
		ls = sp.findAll('a')
		vids = [x for x in ls if "amara.org" in ls['href']]
		self.links = vids
		# now this should work the same way the account objects do, so can be passed to RelevantVideos


class RelevantVideos(object):
	"""Aggregates together information from a bunch of AmaraAccount objects (assuming interest is in a few, more can be added programmatically)"""
	def __init__(self,acct_1=None,acct_2=None,acct_3=None): # each acct should be a var holding an AmaraAcct obj
		self.ids = {} # initialize with empty dict
		self.vid_patt = re.compile(r"/videos/([a-zA-Z0-9]{12})")
		self.coincidental_links = ["openmichigan"] # TODO use this; add more if necessary, seems unlikely 
		# -- there is always a link back to "openmichigan" and that is not a vid to be translated
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

	#def add_account


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
		self.write_file()

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
	# print a.username
	# print a.base
	# print a.num_acct_pages()

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

