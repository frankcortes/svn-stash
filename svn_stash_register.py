import os,sys
import random
from datetime import datetime

HOME_DIR = os.path.expanduser("~")
CURRENT_DIR = os.path.realpath(__file__)
SVN_STASH_DIR= HOME_DIR + "/.svn-stash"
COMMAND_DEFAULT="push"
TARGET_FILE_DEFAULT="all"
STASH_REGISTER_FILENAME = ".stashed_register"

class svn_stash_register:
	"""A class to register all stashes."""
	def __init__(self):
		self.stashes = [] #list of stashes
		self.load() #load register

	def load(self):
   		try:
   			create_stash_dir_if_any()
			current_dir = SVN_STASH_DIR + "/" + STASH_REGISTER_FILENAME
			with open(current_dir,"r") as f:
				for line in f:
					content = line.rstrip()
					content = content.split(" ")
					if len(content)>0:
						self.stashes.append(content[0])
		except IOError as e:
   			print 'registerFile cannot be readed.'

   	def write(self):
 		try:
			current_dir = SVN_STASH_DIR + "/" + STASH_REGISTER_FILENAME
   			with open(current_dir,"w") as f:
   				content = []
   				for stash_id in self.stashes:
   					line = str(stash_id) + "\n"
	   				content.append(line)
   				f.writelines(content)
   				f.close()
		except IOError as e:
   			print 'registerFile cannot be created.'  

   	def obtain_last_stash(self):
   		length = len(self.stashes)
   		if length>0:
   			stash = svn_stash()
   			stash_id = self.stashes[length-1]
   			stash.load(stash_id)
   			return stash

   	def register_stash(self,stash): #stash must be a svn-stash instance
   		stash_id = stash.key
   		self.stashes.append(stash_id) 		
   		stash.write()

   	def delete_stash(self,stash):
   		stash_id = stash.key
   		self.stashes.remove(stash_id)
   		self.write()

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