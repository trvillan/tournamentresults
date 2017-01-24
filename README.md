# Author: Tyler Villanueva
# Date: Oct 20, 2016
# Rev 1

# Rev History:
# rev - date - author - notes
# 0 - Oct 19, 2016 - Tyler Villanueva/Udiactiy - Initial design
# 1 - Oct 20, 2019 - Tyler Villanueva - Re-design

# Revision Notes:
0 - Initial design
1 - Total re-design of the tournament.py, and tournament.sql files.
	This was done as the initial design was getting complicated
	as what was initially visioned. After comments from the Udacity
	team, it was much easier to restart from scratch rather than
	changing my code to accommodate the reviewers comments.

##Steps to run
1. copy tournament.py, tournament.sql, and tournament_test.py into the folder vagrant/tournament folder
2. SSH into the virtual machine using Vagrant SSH
3. From the vagrant/tournament folder in the shell, run *psql -f tournament.sql* to build the tables and view
4. From that some folder, run *python tournament_test.py* to test the schema and api