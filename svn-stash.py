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
		self.files = [] #list of files
		self.timestamp = datetime.now() #time of creation
		self.key = random.getrandbits(128) #unique identifier

	def push(self,target_file,filename_list):
		create_stash_dir_if_any()
		if target_file == "all":
			for filename in filename_list:
				self.push(filename,filename_list)
		else:
			self.files.append(target_file)
			result = os.popen("svn diff " + target_file + " > " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
			result += os.popen("svn revert " + target_file).read()
			print "push " + target_file

	def pop(self):
		if os.path.exists(SVN_STASH_DIR):
			for target_file in self.files:
				self.files.remove(target_file)
				result = os.popen("patch -p0 < " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
				result += os.popen("rm " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
				print "pop " + target_file

	def write(self):
		#Create register
		#Dado un stash nuevo, escribir en el final del registro un nuevo stash con directory bla bla
		#Create file for svn stash
		try:
			current_dir = SVN_STASH_DIR + "/" + str(self.key)
   			with open(current_dir,"w") as f:
   				content = " ".join(self.files)
   				f.writelines(content)
   				f.close()
		except IOError as e:
   			print 'randFile not localized.'



#Auxiliar functions

#Create stash directory
def create_stash_dir_if_any():
	if not os.path.exists(SVN_STASH_DIR):
		os.makedirs(SVN_STASH_DIR)

def execute_stash_push(target_file,filename_list):
	stash = svn_stash()
	stash.push(target_file,filename_list)		
	stash.write()

def execute_stash_pop(target_file,filename_list):
	#obtain last stash pop
	pass

#Parser order and file of the command
def execute_svn_stash(command,target_file,filename_list):
	print command+","+target_file
	if command == "push":
		execute_stash_push(target_file,filename_list)
	elif command == "pop":
		execute_stash_pop(target_file,filename_list)
	elif command == "list":
		pass
	elif command == "clear":
		pass
	elif command == "show":
		pass

#obtain the svn status files
def obtain_svn_status_files():
	status_files = [] 
	status_list = os.popen('svn st').read()
	status_list = status_list.split("\n")
	for line in status_list:
		words = line.split()
		if len(words) > 1:
			(status,filename) = line.split()
			if status == "M":
				status_files.append(filename)
	print "status_files: ",status_files
	return status_files

def main(args):
	command = COMMAND_DEFAULT
	if len(args)>1:
		command = args[1]
	
	target_file = TARGET_FILE_DEFAULT
	if len(args)>2:
		target_file = args[2]
	
	filename_list = obtain_svn_status_files()
	execute_svn_stash(command,target_file,filename_list)


if __name__ == '__main__':
    main(sys.argv)