########################################################################################
# SIRI (X Near Y, X:Place(ex:Restaurant,etc.) Y:Location(ex:Guwahati)) App For Jasmine #
########################################################################################

#Credits:
#	- Swathi Karri <swathi.iitg@gmail.com>
#	- Naga Rohit S <snagarohit@gmail.com>

import json
import re
import random
import environment
import interaction
import nltk
import urllib2
import urllib


####################
# Public Functions #
####################

#Identifies the app in a unique id.
app_id = "siri"

#In any lib_* file, "check" function checks if the post/news item is of the app's corresponding post
def check(post):
	#Check if it's a tagged sentence (marked for some other apps)
	if re.search(r'#[A-Za-z0-9]',post['message']):
		return False
	
	tokenized_words = nltk.word_tokenize(post['message'])
	tagged_words = nltk.pos_tag(tokenized_words)
	finalized_tagged_words = []
	tag_list = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
	#Eliminating commas, fullstops etc.
	
#	print "--------"
#	print tagged_words
#	print "--------"
	
	for tagged_word in tagged_words:
		if tagged_word[1] in tag_list:
			finalized_tagged_words.append(tagged_word)
	
	copy_finalized_tagged_words = finalized_tagged_words
	copy_finalized_tagged_words.reverse()
	tagged_string = ""
	for tagged_reverse_word in copy_finalized_tagged_words:
		tagged_string = tagged_string+" "+tagged_reverse_word[1]
	
	tagged_string = tagged_string[1:]
	match_obj = re.search(r'^(NNPS|NNP|NNS|NN|POS|\s)+IN\s(NNPS|NNP|NNS|NN|POS|\s)+',tagged_string)
	if match_obj:
		return True
	else:
		return False

#After confirming that the message/status corresponds to the current app using the "check" function above, "execute" function
#is called to do the actual work

def execute(post):
	tokenized_words = nltk.word_tokenize(post['message'])
	tagged_words = nltk.pos_tag(tokenized_words)
	finalized_tagged_words = []
	tag_list = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
	#Eliminating commas, fullstops etc.
	for tagged_word in tagged_words:
		if tagged_word[1] in tag_list:
			finalized_tagged_words.append(tagged_word)
	
	copy_finalized_tagged_words = finalized_tagged_words
	copy_finalized_tagged_words.reverse()
	tagged_string = ""
	for tagged_reverse_word in copy_finalized_tagged_words:
		tagged_string = tagged_string+" "+tagged_reverse_word[1]
	
	tagged_string = tagged_string[1:]
#	print tagged_string
	match_obj = re.search(r'^(NNPS|NNP|NNS|NN|POS|\s)+IN\s(NNPS|NNP|NNS|NN|POS|\s)+',tagged_string)
	
#	print match_obj.group()
	l = len(match_obj.group().split())
	li = copy_finalized_tagged_words[:l]
	li.reverse()
	s = ''
	for tu in li:
		s = s+" "+tu[0]
	s = s[1:] #Mattered string 
	
	t = ''
	for tu in li:
		t = t+" "+tu[1]
	t = t[1:] #Mattered tags
	
	preposition_index = 0
	for word in t.split():
		if word!='IN':
			preposition_index = preposition_index+1
		else:
			break
			
	location = s.split()[preposition_index+1:]
	thing = s.split()[:preposition_index]
	#print thing
	
	location_string = ''
	for word in location:
		location_string = location_string+' '+word
	location_string = location_string[1:]
	
	thing_string = ''
	for word in thing:
		thing_string = thing_string+' '+word
	thing_string = thing_string[1:]
	#removing possessive quotation marks
	thing_string = re.sub(r" '",'',thing_string)
#	print "Location: "+location_string+" Thing: "+thing_string
	return getinfo(location_string,thing_string)	
	
######################
# Internal Functions #
######################
def getinfo(location,place_thing):
	st = urllib.quote_plus(location)
	kword = urllib.quote_plus(place_thing)
	var1 = 'http://maps.googleapis.com/maps/api/geocode/json?address='+st+'&sensor=false'
	response = urllib2.urlopen(var1)
	the_page = response.read()
	dict1 = json.loads(the_page)
	lat = str(dict1["results"][0]["geometry"]["location"]["lat"])
	lng = str(dict1["results"][0]["geometry"]["location"]["lng"])
	var2 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat+','+lng+'&rankby=distance&keyword='+kword+'&sensor=false&key=AIzaSyCGIRblhXtc7qslfMAHBCj29VkQ6FIKVOw'
	response = urllib2.urlopen(var2)
	the_page = response.read()
	dict2 = json.loads(the_page)

	size = 0
	return_string = ''
	
	for result in dict2['results']:
		return_string = return_string+result['name']+" near "+result['vicinity']+'.\n'
		size = size+1
		if size>=4:
			break
		
	return_string = return_string[:-1]
	return return_string
