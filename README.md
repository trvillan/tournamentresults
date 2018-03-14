# About:
Built a PostgreSQL relational database scheme to store the results of a game tournament. Also provided a number of queries to efficiently report the results of the tournament and determine the winner.

##Steps to run
1. copy tournament.py, tournament.sql, and tournament_test.py into the folder vagrant/tournament folder prvided from udacity.
2. SSH into the virtual machine using Vagrant SSH.
3. From the vagrant/tournament folder in the shell, run *psql -f tournament.sql* to build the tables and view
4. From that some folder, run *python tournament_test.py* to test the schema and api
