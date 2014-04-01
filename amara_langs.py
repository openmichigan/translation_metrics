import requests, json
from itertools import groupby

## http://www.amara.org/api2/partners/videos/7AO3TZh2WGOK/languages/?format=json

baseurl = "http://www.amara.org/api2/partners/videos/{}/languages/?format=json" # needs videoid

f = open("OM_amara_ids_2013-12-18.txt", "r") # regularly need to run other file, open correct file (easy if run today, etc, date)
ids = [x.strip() for x in f.readlines()]
lang_names = []
langs = {}
total_langs = 0
#transls = 0
for i in ids:
	t = json.loads(requests.get(baseurl.format(i)).text)
	total_langs += int(t["meta"]["total_count"])
	#transls += int(t["meta"]["total_count"])
	for ob in t["objects"]:
		if ob["language_code"]:
			if ob["language_code"] in langs:
				langs[ob["language_code"]] += 1
			else:
				langs[ob["language_code"]] = 1
		if ob["name"] != "english":
			lang_names.append(ob["name"])

			#langs.get(ob["language_code"],0) + 1
			# if ob["language_code"] == "en":
			# 	transls -= 1


## here's stuff where I was printing data ad-hoc-ily

print "lang dict",langs

print "number of total languages including english:", total_langs

non_eng_langs = []
total_transls = 0
for k in langs:
	if k != "en":
		total_transls += langs[k]
		non_eng_langs.append(k)

print "total non-english translations", total_transls
print
print "list of language codes:\n"
for i in non_eng_langs: print i
print 
print "list of language names:"
# for i in set(lang_names):
# 	print i
print
for k in langs:
	print k, langs[k]
print
lnms = set(sorted(lang_names))
print lnms
amts = [len(list(group)) for key,group in groupby(lnms)]
print amts
tog = zip(set(lnms),amts)
print tog
# print
# for k,y in sorted(tog,key=lambda x: x[1],reverse=True):
# 	print k,y

# here's where we should return formatted data


