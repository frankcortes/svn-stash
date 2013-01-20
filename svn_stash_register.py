import os,sys
import random
from datetime import datetime

HOME_DIR = os.path.expanduser("~")
CURRENT_DIR = os.path.realpath(__file__)
SVN_STASH_DIR= HOME_DIR + "/.svn-stash"
COMMAND_DEFAULT="push"
TARGET_FILE_DEFAULT="all"


class svn_stash:
	"""A class to contain all information about stashes."""
	def __init__(self):
		self.files = {} #dictionary of files
		self.timestamp = datetime.now() #time of creation
		self.key = random.getrandbits(128) #unique identifier

	def push(self,target_file,filename_list):
		create_stash_dir_if_any()
		if target_file == "all":
			for filename in filename_list:
				self.push(filename,filename_list)
		else:
			randkey = random.getrandbits(128) #unique identifier
			self.files[target_file] = randkey
			result = os.popen("svn diff " + target_file + " > " + SVN_STASH_DIR + "/" + str(randkey) + ".stash.patch").read()
			result += os.popen("svn revert " + target_file).read()
			print "push " + target_file

	def pop(self):
		if os.path.exists(SVN_STASH_DIR):
			for target_file in self.files:
				randkey = self.files[target_file]
				result = os.popen("patch -p0 < " + SVN_STASH_DIR + "/" + str(randkey) + ".stash.patch").read()
				result += os.popen("rm " + SVN_STASH_DIR + "/" + str(randkey) + ".stash.patch").read()
				print "pop " + target_file
			#delete the file of svn_stash
			result += os.popen("rm " + SVN_STASH_DIR + "/" + str(self.key)).read()

	def write(self):
		#Create register
		#Dado un stash nuevo, escribir en el final del registro un nuevo stash con directory bla bla
		#Create file for svn stash
		try:
			current_dir = SVN_STASH_DIR + "/" + str(self.key)
   			with open(current_dir,"w") as f:
   				content = []
   				for target_file in self.files:
   					line = target_file + " " + str(self.files[target_file]) + "\n"
	   				content.append(line)
   				f.writelines(content)
   				f.close()
		except IOError as e:
   			print 'randFile cannot be created.'
   
   	def load(self,stash_id):
   		try:
			current_dir = SVN_STASH_DIR + "/" + str(stash_id)
			with open(current_dir,"r") as f:
				for line in f:
					content = line.rstrip()
					content = content.split(" ")
					if len(content)>=2:
						self.files[content[0]] = content[1]
			self.key = stash_id
		except IOError as e:
   			print 'randFile cannot be readed.'

#Auxiliar functions

#Create stash directory
def create_stash_dir_if_any():
	if not os.path.exists(SVN_STASH_DIR):
		os.makedirs(SVN_STASH_DIR)