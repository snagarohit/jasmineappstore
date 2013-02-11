
###################################################################################
# Ventrillo Status Repeating App which speaks the status requested by its friends #
###################################################################################

import json
import re
import random
import environment
import interaction

#Credits
#	- Naga Rohit S <snagarohit@gmail.com>

####################
# Public Functions #
####################

#Identifies the app in a unique id.
app_id = "ventrillo"

#In any lib_* file, "check" function checks if the post/news item is of the app's corresponding post
def check(post):
	matchObj = re.search(r"#[Vv][eE][nN][tT][rR][iI][lL][lL][oO]",post['message'])
	if matchObj:
		if re.search(r'(#[jJ][aA][sS][mM][iI][nN][eE]|#[jJ][aA][sS][mM][iI][nN][eE] [lL][aA][bB])',post['message']):
			return True
		else:
			return False
	return False

#After confirming that the message/status corresponds to the current app using the "check" function above, "execute" function
#is called to do the actual work

def execute(post):
	#Stripping ventrillo app markers from the status
	status = re.sub(r'\s*(#[jJ][aA][sS][mM][iI][nN][eE]|#[jJ][aA][sS][mM][iI][nN][eE] [lL][aA][bB])\s*','',post['message'])
	status = re.sub(r'\s*#[Vv][eE][nN][tT][rR][iI][lL][lL][oO]\s*','',status)
	#Get the user name for the post
	user_name = post['name']
	first_name = user_name.split()[0]+" "+user_name.split()[1][0] #It'll be like "Naga R" for "Naga Rohit"
	final_status = status+"\n\nvia "+first_name
	
	interaction.update(final_status,None,environment.my_id) #Updating Status
	
	return_comment = return_random_affirmative() #Comment on the post
	return return_comment
	
	
######################
# Internal Functions #
######################

#Returns a random affirmative
def return_random_affirmative():
	ans_list = ['Status copied and updated :)','Done!','Roger that!', 'Sir, Yes, Sir!','Aye.. Aye.. Captain :D','Got that!','Okay :)', 'As you say!',"Okay, I'll say that."]
	ans = random.choice(ans_list)
	
	return ans
