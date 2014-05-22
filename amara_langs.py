import requests, json
from itertools import groupby
import amara_vids as av


# parse iana subtag (language code) registry
stf = open("iana_subtag_registry.txt").read()
langlist = stf.split("%%")
codelangs = {}

separated = [x.strip().split("\n") for x in langlist]
for si in separated:
	for term in si:
		if term.startswith("Subtag:"):
			codelangs[term.split(":")[1].strip().rstrip()] = si[2].split(":")[1].strip().rstrip()


# remainder: objects, code using the objects
class AmaraInfoSet(object):
	"""Gets metrics for videos/translations, writes json"""
	def __init__(self,relvid): #relvid should be a RelevantVideos instance
		relvid.manage_links()
		self.baseurl = "http://www.amara.org/api2/partners/videos/{}/languages/?format=json" # structured for .format arg
		self.vid_ids = relvid.ids.keys()
		#print self.vid_ids
		self.total_langs = 0
		self.lang_names = []
		self.langs = {}
		self.get_info()
		self.get_non_english_langs()
		self.lang_map = codelangs # created in py file, above
		self.lang_map['swa'] = "Swahili" # because of a multiple version problem, see error correction
		self.lang_map['zh'] = "Chinese" # same deal, let's see TODO

	def get_info(self):
		for i in self.vid_ids:
			#print i # debug
			# TODO: use coincidental_urls for actual use. for now, no harm done.
			try:
				t = json.loads(requests.get(self.baseurl.format(i)).text)
				self.total_langs += int(t["meta"]["total_count"])
				for ob in t["objects"]:
					if ob["language_code"]:
						if ob["language_code"] in self.langs:
							self.langs[ob["language_code"]] += 1
						else:
							self.langs[ob["language_code"]] = 1 # TODO missing zh somewhere?? why?
					if ob["name"] != "english": # using for non-english languages, primary use case
						self.lang_names.append(ob["name"])
			except Exception, e:
				#print "There was an error -- \n",e
				#print "Occurred in",self.baseurl.format(i)
				## console printing no longer useful here, just exception handling
				continue


	def get_non_english_langs(self):
		self.non_eng_langs = []
		self.total_transls = 0 # maybe not necessary, TODO consider
		for k in self.langs:
			if k != "en":
				self.total_transls += self.langs[k]
				#print self.langs[k]
				self.non_eng_langs.append(k)

	def prep_info(self):
		self.get_info()
		self.get_non_english_langs()
		self.langsnums = {}
		lks = []
		# appending all the correct language code keys to lks list
		for k in self.langs.keys():
			if "-" in k:
				k = k.split("-")[0]
			lks.append(k.replace("-","").strip().rstrip())
		# constructing reference dict
		for i in lks:
			if i in self.lang_map and i in self.langs:
				if self.lang_map[i] in self.langsnums:
					self.langsnums[self.lang_map[i]] += self.langs[i]
				else:
					self.langsnums[self.lang_map[i]] = self.langs[i]
			else:
				print "ERROR FOUND - cannot decode language code: {}\n".format(i) # good place for error? TODO
# TODO make sure numbers, once combined, are really correct
# TODO sort properly

	def __str__(self):
		self.prep_info()
		s = """
Number of total languages including English: {}
Total non-English translations: {}
Languages:\n
""".format(len(self.langs.keys()),self.total_transls)
		# for l in sorted(self.langs.keys(), key=lambda x: self.langs[x], reverse=True):
		# 	if "-" in l:
		# 		l = [x.replace("-","").strip().rstrip() for x in l.split("-")][0] # for pt-br etc, want just pt (for example)
		# 	try:
		# 		s += "- {} {}\n".format(self.langs[l],self.lang_map[l]) # better: parse iana registry
		# 	except:
		# 		s += "cannot decode language code: {}\n".format(l) # better: parse iana registry
		for l in self.langsnums:
			s += "- {} {}\n".format(self.langsnums[l], l)
		return s

if __name__ == '__main__':

	om_acct = av.AmaraAccount("openmichigan.video")
	kath_acct = av.AmaraAccount("kludewig")

	relvs = av.RelevantVideos(om_acct,kath_acct)

	total_info = AmaraInfoSet(relvs)
	#total_info.get_info()
	#total_info.get_non_english_langs() # will this work without?
	#print total_info.lang_names
	print total_info # here's where write to json file -- but want it depending on course??
