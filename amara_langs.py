import requests, json
from itertools import groupby
import amara_vids as av



stf = open("iana_subtag_registry.txt").read()
langlist = stf.split("\%\%")
codelangs = {}


#lpairs = [codelangs[x] = get_lang() for x in lls]


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
		# need map of langs to codes (English language names for primary audience) -- for now, manually filled in as needed
		# TODO use API request, or build a better map.
		self.lang_map = {"en":"English","es":"Spanish","id":"Indonesian","zh-tw":"Mandarin Chinese (traditional)","zh-cn":"Mandarin Chinese (simplified)","swa":"Swahili","fr":"French","it":"Italian","vi":"Vietnamese","ru":"Russian","ro":"Romanian","lg":"Luganda","pt":"Portuguese","pt-br":"Brazilian Portuguese","ar":"Arabic"}

	def get_info(self):
		for i in self.vid_ids:
			#print i # debug
			try:
				t = json.loads(requests.get(self.baseurl.format(i)).text)
				self.total_langs += int(t["meta"]["total_count"])
				for ob in t["objects"]:
					if ob["language_code"]:
						if ob["language_code"] in self.langs:
							self.langs[ob["language_code"]] += 1
						else:
							self.langs[ob["language_code"]] = 1
					if ob["name"] != "english": # using for non-english languages, primary use case
						self.lang_names.append(ob["name"])
			except Exception, e:
				print "There was an error -- \n",e
				print "Occurred in",self.baseurl.format(i)
				continue


	def get_non_english_langs(self):
		self.non_eng_langs = []
		self.total_transls = 0 # maybe not necessary, TODO consider
		for k in self.langs:
			if k != "en":
				self.total_transls += self.langs[k]
				#print self.langs[k]
				self.non_eng_langs.append(k)

	def __str__(self):
		self.get_info()
		self.get_non_english_langs()
		s = """
Number of total languages including English: {}
Total non-English translations: {}
Languages:\n
""".format(len(self.langs.keys()),self.total_transls)
		for l in sorted(self.langs.keys(), key=lambda x: self.langs[x], reverse=True):
			s += "- {} {}\n".format(self.langs[l],self.lang_map[l]) # better: parse iana registry
		return s

if __name__ == '__main__':

	om_acct = av.AmaraAccount("openmichigan.video")
	kath_acct = av.AmaraAccount("kludewig")

	relvs = av.RelevantVideos(om_acct,kath_acct)

	total_info = AmaraInfoSet(relvs)
	#total_info.get_info()
	#total_info.get_non_english_langs() # will this work without?
	#print total_info.lang_names
	print total_info
