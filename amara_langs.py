import requests, json
from itertools import groupby
import amara_vids as av
import datetime
import sys


# remainder: objects, code using the objects
class AmaraInfoSet(object):
	"""Object gets/stores metrics for videos/translations across whatever boundary/set specified by account(s) chosen"""
	def __init__(self,relv): #relvid should be a RelevantVideos instance
		# manage and create langmap -- parse iana subtag (language code) registry
		stf = open("iana_subtag_registry.txt").read()
		langlist = stf.split("%%")
		codelangs = {}

		separated = [x.strip().split("\n") for x in langlist]
		for si in separated:
			for term in si:
				if term.startswith("Subtag:"):
					codelangs[term.split(":")[1].strip().rstrip()] = si[2].split(":")[1].strip().rstrip()
		relvid = relv
		relvid.manage_links()
		self.baseurl = "http://www.amara.org/api2/partners/videos/{}/languages/?format=json" # structured for .format arg
		self.vid_ids = relvid.ids.keys()
		self.flag = False
		self.total_indiv_subtitles = 0
		self.lang_names = []
		self.langs = {}
		self.get_non_english_langs()
		self.lang_map = codelangs # created dict above
		self.lang_map['swa'] = "Swahili" # because of a multiple version problem, see error correction
		self.lang_map['zh'] = "Chinese" # same thing
		self.lang_map['zhx'] = "Chinese" # same thing

	def get_info(self):
		#print self.lang_map
		self.flag = True # notes that get info has been run on this instance
		now = datetime.datetime.now()
		# open csv file and write videoid-language pairs to it
		ft = open("video_ids_langs_{}.csv".format(now), "w")
		ft.write("Video ID,Language Translation\n")
		for i in self.vid_ids:
			if i != "openmichigan":
				try:
					t = json.loads(requests.get(self.baseurl.format(i)).text)
					self.total_indiv_subtitles += int(t["meta"]["total_count"]) # weird number TODO check
					for ob in t["objects"]:
						if ob["language_code"]:
							#print ob["language_code"] # DEBUG
							lc = ob["language_code"]
							if "-" in lc:
								lc = lc.split("-")[0].replace("-","").strip().rstrip()
							if self.lang_map[lc] in self.langs:
								self.langs[self.lang_map[lc]] += 1
							else:
								self.langs[self.lang_map[lc]] = 1
							ft.write("{}\t{}\n".format(i,self.lang_map[lc]))
						if ob["name"] != "english": # using for non-english languages, primary use case
							self.lang_names.append(ob["name"]) 

				except Exception, e:
					print "Exception raised - {}".format(e)
					print "Looking at video: {}".format(i)
					continue

	def get_total_subtitles(self):
		"""Gets and returns the number of total non-English subtitles extant in this InfoSet"""
		tot = 0
		for i in self.langs:
			if "en" not in i:
				tot += self.langs[i]
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

	def __str__(self):
		"""Provides print-to-console representation of InfoSet"""
		if not self.flag:
			self.get_info()
		s = """
Number of total languages including English: {}
Total non-English translations: {}
Languages:\n
""".format(len(self.langs.keys()),self.total_transls) #len([x for x in self.langs.keys() if "english" not in x.lower()])
		for l in sorted(self.langs.keys(),key=lambda x:self.langs[x]):
			s += "- {} {}\n".format(self.langs[l], l)
		return s
	
	def __repr__(self):
		# TODO: return some form of structured non-C/TSV data. JSON?
		pass

	def write_tsv(self):
		#self.get_info()
		if not self.flag:
			self.get_info()
		now = str(datetime.datetime.now())
		f = open("amara_info_{}.csv".format(now), "w") # creates csv file dated with current date/time
		f.write("Language Name\tNumber of Subtitles\n")
		f.write("Total Subtitles (Including English),{}\n".format(self.total_indiv_subtitles))
		f.write("Total Non-English Subtitles,{}\n".format(int(self.get_total_subtitles()))) # TODO add the total number of non-English subtitles
		for l in sorted(self.langs.keys(),key=lambda x:self.langs[x]):
			f.write("{},{}\n".format(l,self.langs[l]))

if __name__ == '__main__':

	# access accounts to be used and save in AmaraAccount instances
	if len(sys.argv) == 1:
		om_acct = av.AmaraAccount("openmichigan.video")
		addl_acct = av.AmaraAccount("kludewig")
		accounts = [om_acct,addl_acct]
	else:
		accounts = []
		for item in sys.argv[1:]:
			accounts.append(item)
	# get relevant videos from the account objects
	relvs = av.RelevantVideos(*accounts)
	# create an AmaraInfoSet instance and write file/print information to console
	total_info = AmaraInfoSet(relvs)
	# print information to console
	print total_info 
	# write aggregate file
	total_info.write_tsv()

