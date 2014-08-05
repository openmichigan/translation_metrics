import requests, json
from itertools import groupby
import amara_vids as av
import datetime


# parse iana subtag (language code) registry
stf = open("iana_subtag_registry.txt").read()
langlist = stf.split("%%")
codelangs = {}

separated = [x.strip().split("\n") for x in langlist]
for si in separated:
	for term in si:
		if term.startswith("Subtag:"):
			#print term.split(":")[1].strip().rstrip()
			#print si[2].split(":")[1].strip().rstrip()
			if "zhx" in term.split(":")[1].strip().rstrip():
				print "zhx"
				print si[2].split(":")[1].strip().rstrip()
			codelangs[term.split(":")[1].strip().rstrip()] = si[2].split(":")[1].strip().rstrip()


# remainder: objects, code using the objects
class AmaraInfoSet(object):
	"""Object gets/stores metrics for videos/translations across whatever boundary/set specified by account(s) chosen"""
	def __init__(self,relvid): #relvid should be a RelevantVideos instance
		relvid.manage_links()
		self.baseurl = "http://www.amara.org/api2/partners/videos/{}/languages/?format=json" # structured for .format arg
		self.vid_ids = relvid.ids.keys()
		#print self.vid_ids
		self.total_indiv_subtitles = 0
		self.lang_names = []
		self.langs = {}
		self.get_info()
		self.get_non_english_langs()
		self.lang_map = codelangs # created in py file, above
		self.lang_map['swa'] = "Swahili" # because of a multiple version problem, see error correction
		self.lang_map['zh'] = "Chinese" # same deal

	def get_info(self):
		for i in self.vid_ids:
			try:
				t = json.loads(requests.get(self.baseurl.format(i)).text)
				self.total_indiv_subtitles += int(t["meta"]["total_count"])
				for ob in t["objects"]:
					if ob["language_code"]:
						# if ob["language_code"] == "zh":
						# 	ob["language_code"] = "zhx" # trying to correct for inconsistency in lang codes
						if ob["language_code"] in self.langs:
							self.langs[ob["language_code"]] += 1
						else:
							self.langs[ob["language_code"]] = 1
							# if "zh" in ob["language_code"]:
							# 	print "yes zh"
					if ob["name"] != "english": # using for non-english languages, primary use case
						self.lang_names.append(ob["name"])
			except Exception, e:
				print "Exception raised - {}".format(e)
				print "Looking at video: {}".format(i)
				continue

	def get_total_subtitles(self):
		"""Gets and returns the number of total non-English subtitles extant in this InfoSet"""
		tot = 0
		for i in self.langsnums:
			if "en" not in i:
				tot += self.langsnums[i]
		return tot

	def get_non_english_langs(self):
		"""Saves a list of all languages, besides English, subtitles have been translated into"""
		self.non_eng_langs = []
		self.total_transls = 0 # maybe not necessary, TODO consider
		for k in self.langs:
			if k != "en":
				self.total_transls += self.langs[k]
				#print self.langs[k]
				self.non_eng_langs.append(k)

	def prep_info(self):
		self.get_info()
		#self.get_non_english_langs() # not necessary, but can include
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
			elif "zh" in i: # correcting for discrepancy in language code list being used
				if "Chinese" in self.langsnums:
					self.langsnums["Chinese"] += 1
				else:
					self.langsnums["Chinese"] = 1 
			else:
				print "ERROR FOUND - cannot decode language code: {}\n".format(i) 
# TODO double check number correctness

	def __str__(self):
		"""Provides print-to-console representation of InfoSet"""
		self.prep_info()
		s = """
Number of total languages including English: {}
Total non-English translations: {}
Languages:\n
""".format(len(self.langs.keys()),self.total_transls) #len([x for x in self.langs.keys() if "english" not in x.lower()])
		for l in sorted(self.langsnums.keys(),key=lambda x:self.langsnums[x]):
			s += "- {} {}\n".format(self.langsnums[l], l)
		return s
	
	def __repr__(self):
		# TODO: return some form of structured non-TSV data. JSON?
		pass

	def write_tsv(self):
		self.prep_info()
		now = str(datetime.datetime.now())
		f = open("amara_info_{}.csv".format(now), "w") # creates csv file dated with current date/time
		f.write("Language Name\tNumber of Subtitles\n")
		f.write("Total Non-English Subtitles\t{}\n".format(int(self.get_total_subtitles()))) # TODO add the total number of non-English subtitles
		for l in sorted(self.langsnums.keys(),key=lambda x:self.langsnums[x]):
			f.write("{}\t{}\n".format(l,self.langsnums[l]))

if __name__ == '__main__':
	# Code here for testing / Open.Michigan use case(s)

	# access accounts to be used and save in AmaraAccount instances -- here, Open.Michigan's
	om_acct = av.AmaraAccount("openmichigan.video")
	kath_acct = av.AmaraAccount("kludewig")
	# get relevant videos from the account objects
	relvs = av.RelevantVideos(om_acct,kath_acct)
	# create an AmaraInfoSet instance and write file/print information to console
	# not yet writing by course because of association problem, but theoretically that object inst would work
	total_info = AmaraInfoSet(relvs)
	total_info.write_tsv()
	print total_info 
