import os,sys
import random
from datetime import datetime
from svn_stash_register import svn_stash,HOME_DIR,CURRENT_DIR,SVN_STASH_DIR,COMMAND_DEFAULT,TARGET_FILE_DEFAULT

def execute_stash_push(target_file,filename_list):
	stash = svn_stash()
	stash.push(target_file,filename_list)		
	stash.write()

def execute_stash_pop(target_file,filename_list):
	#obtain last stash pop
	stash = svn_stash()
	stash.load("171669737844967379750928809658126056317")
	stash.pop()

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