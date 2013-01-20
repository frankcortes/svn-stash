import os,sys
import random

HOME_DIR = os.path.expanduser("~")
SVN_STASH_DIR= HOME_DIR + "/.svn-stash"
COMMAND_DEFAULT="push"
TARGET_FILE_DEFAULT="all"

def create_stash_dir_if_any():
	if not os.path.exists(SVN_STASH_DIR):
		os.makedirs(SVN_STASH_DIR)

def execute_stash_push(target_file,filename_list):
	create_stash_dir_if_any()
	random_key = random.getrandbits(128)
	#execute stash_push for all files
	if target_file == "all":
		for filename in filename_list:
			execute_stash_push(filename,filename_list)
	else:
		result = os.popen("svn diff " + target_file + " > " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
		result += os.popen("svn revert " + target_file).read()
		#print result

def execute_stash_pop(target_file,filename_list):
	if os.path.exists(SVN_STASH_DIR):
		if target_file == "all":
			pass
		else:
			result = os.popen("patch -p0 < " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
			result += os.popen("rm " + SVN_STASH_DIR + "/" + target_file + ".stash.patch").read()
		
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