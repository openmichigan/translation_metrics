from bs4 import BeautifulSoup as bsoup 
import json, requests, re, datetime, urllib


class AmaraAccount(object):
	def __init__(self, username):
		self.username = username
		self.base = "http://www.amara.org/en/profiles/videos/%s/" % (self.username)

	def num_acct_pages(self):
		"""This should return an integer that is the number of pages of vids in the account"""
		pass

	def get_links(self):
		r = requests.get("url%s" % "?page=last")
		soup = bsoup(r)
		self.links = soup.findall('a')


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

	def manage_lastpage_links(self):
		for ab in self.acctobjs:
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
				burl = base + "?page={}".format(i)
				rb = requests.get(burl).text
				sp = bsoup(rb)
				lks = sp.findAll('a')
				for l in lks:
					tst = re.search(patt, l['href'])
					if tst is not None:
						ed = tst.groups()[0]
						if ed not in ids:
							ids[ed] = 1
						else: continue
					else:
						continue

	def write_file(self):
		now = str(datetime.datetime.now())
		fname = "OM_amara_ids_{}.txt".format(now[:10]) # to instance variablize or not to instance variablize
		f = open(fname, "w")
		for k in self.ids:
			if k not in self.coincidental_links: 
				f.write(k+"\n") # write the id to a file
		f.close()

##### START OLD CODE, ABOVE NEW CODE

count = 15 # total amount of pages on amara acct. TODO: remove need to make sure this is right
baseurl = "http://www.amara.org/en/profiles/videos/openmichigan.video/?page=last"
base = "http://www.amara.org/en/profiles/videos/openmichigan.video/" # for iterating through pgs
kathleen_url = "http://www.amara.org/en/profiles/videos/kludewig/"
# get all videoids from a given page in ids dict
r = requests.get(baseurl).text
soup = bsoup(r)
links = soup.findAll('a')
rt = requests.get(kathleen_url).text
sp_k = bsoup(rt)
k_links = sp_k.findAll('a')
#print k_links
links = links + k_links
#links += sp.findAll('a')
# consider these vars global even though it's bad
patt = re.compile(r"/videos/([a-zA-Z0-9]{12})")
ids = {}
for l in links:
	test = re.search(patt,l['href'])
	if test is not None:
		eyedee = test.groups()[0]
		if eyedee not in ids:
			ids[eyedee] = 1 # entering it into dict
		else:
			continue
	else:
		continue

patt = re.compile(r"/videos/([a-zA-Z0-9]{12})")
for i in range(1,count):
	burl = base + "?page={}".format(i)
	rb = requests.get(burl).text
	sp = bsoup(rb)
	lks = sp.findAll('a')
	for l in lks:
		tst = re.search(patt, l['href'])
		if tst is not None:
			ed = tst.groups()[0]
			if ed not in ids:
				ids[ed] = 1
			else: continue
		else:
			continue

now = str(datetime.datetime.now())
fname = "OM_amara_ids_{}.txt".format(now[:10])
f = open(fname, "w")
for k in ids:
	if k != "openmichigan": f.write(k+"\n") # that's a semi-coincidental url, not a video id we want
f.close()

## Amara URL time
# amara_api_key = "9f3ef1370ccc01d0d1ccf8758077c429890ad0ab"
# amara_username = "openmichigan.video"

#vals = {"X_apikey":amara_api_key,"X-api-username":amara_username}

#langurl = "/api2/partners/videos/{}/languages/"

# for edi in open(fname,"r").readlines()[:1]:
# 	url = "https://staging.universalsubtitles.org/" + langurl.format(edi.strip()) #+ "?" + urllib.urlencode(vals)
# 	# now curl request with key and username and password (INSECURE)
# 	print url