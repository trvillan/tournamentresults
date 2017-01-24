#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# File: tournament.py
# Author: Tyler Villanueva (Udacity with function definitions)
# Date: Oct 20, 2016
# Rev 1

# Rev History:
# rev - date - author - notes
# 0 - ? - Tyler Villanueva/Udiactiy - Initial design
# 1 - Oct 20, 2016 - Tyler Villanueva - Re-design

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM results")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM players")
    playerCount = cursor.fetchone()[0]
    conn.close()
    return playerCount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (p_name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM standings")
    playerStands = cursor.fetchall()
    conn.close()
    return playerStands


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results VALUES (%s, %s, true)",
                   (winner, loser))
    cursor.execute("INSERT INTO results VALUES (%s, %s, false)",
                   (loser, winner))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # get a list that only includes id and name from our standings view
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id,p_name FROM standings")
    pair = cursor.fetchall()
    conn.close()
    # because the rules state that players should never match up more than once
    # we use playedCount to check that and build out a list of pairings
    # that hopefully includes everyone but has no repeat matches between rounds
    hasPartner = []
    pairsList = []
    pairLen = len(pair)
    for index, player1 in enumerate(pair):
        if not index in hasPartner:
            for index2 in range(index, pairLen):
                if playedCount(player1[0], pair[index2][0]) == 0:
                                hasPartner.extend([index, index2])
                    pairsList.append((player1[0], player1[1],
                        pair[index2][0], pair[index2][1]))
                    break
    return pairsList


def playedCount(player1, player2):
    """Checks if the players have already been matched to avoid
    multiple pairings of the same players, which is against Swiss
    tournament rules (and database schema restrictions).  It will
    return early with a 1 if player1 and player2 are the same id

    Ars:
      player1: the id of the player looking for an opponent
      player2: the id of the potential opponent

    Returns:
      numberPlayed: A number representing the count of times these
      opponenets have previously played (Expected to be 0 or 1)
    """
    if player1 == player2:
        # Early return when trying to match against themselves
        return 1
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT Count(id) AS CountOfid FROM results
        WHERE id = %s and opponent = %s""", (player1, player2))
    numberPlayed = cursor.fetchone()[0]
    conn.close()
    return numberPlayed
