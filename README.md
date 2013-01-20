svn-stash
==========

It's like the git stash command, but for Subversion. If you don't know git, you should read [this guide.](http://git.or.cz/course/svn.html)
Svn-stash permits you to hide the changes that you don't want to commit just now. this can be more useful in some circunstances.

Why?
----------

I love git and I think that it should be used in the new projects that WHATEVER programmer starts (If you don't think the same, 	You are welcome to discuss it with me, but you can read [the pro git book](http://git-scm.com/book) before. :) ). However, in some old projects where I'm working now the svn-to-git migration is very difficult or imposible. Git has a set of awesome commands I usually use, (like stash) that svn hasn't direct equivalent. Svn-stash is an attempt to port some of the functionalities of the git stash command to subversion.

How to Install
----------

This command only is a common python script for now. If you want to use as a regular command, you can add a alias in your .bashrc or .bash_profile file.
```bash
git clone https://github.com/frankcortes/svn-stash.git 
mv svn-stash ~/.svn-stash-command
```
add this line in .bashrc(Linux) /.bash_profile(MAC OS X): 
```bash
alias svn-stash='python ~/.svn-stash-command/svn-stash.py'
```


Documentation
----------

### push ######
This command will save all changes in a secure directory to be later recovered.
### pop ######
This command will recover all changes of the last stash.
### list ######
List all saved stashes.
### show ######
Show all changes of the files have been stashed with diff format, for each one of the stashes.
### clear ######
Delete all saved stashes.


License
------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.