#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error: Database connection not successful.")

def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute("TRUNCATE TABLE matchlist CASCADE")
    db.commit()
    db.close()
    return c


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute("TRUNCATE TABLE playerlist CASCADE")
    db.commit()
    db.close()
    return c


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    c.execute("SELECT COUNT(id) FROM playerlist")
    count = c.fetchone()[0]
    db.close()
    return count;


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    name = bleach.clean(name, strip=True).strip()
    c.execute("INSERT INTO playerlist (name) VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, c = connect()
    c.execute("SELECT * FROM player_standings;")

    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    winner = bleach.clean(winner, strip=True).strip()
    loser = bleach.clean(loser, strip=True).strip()

    c.execute("SELECT EXISTS(SELECT * FROM matchlist WHERE winner=%s and loser=%s)", (winner, loser,))
    exists = c.fetchone()[0]
   
    if exists == False:
        c.execute("INSERT INTO matchlist (winner, loser) VALUES (%s, %s)", (winner, loser,))
        db.commit()
        db.close()
    else:
        print 'Error: Cannot report! These two teams have already played each other once! (Are you sure you got the right id ?)'

 
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
    db, c = connect()
    c.execute("SELECT * FROM winner_board")
    rows = c.fetchall()
    winnerBoardSize = len(rows)
    result = []

    i =0
    if i%2==0:
        while i<winnerBoardSize:
            result.append([rows[i][0], str(rows[i][1]), rows[i+1][0], str(rows[i+1][1])])
            i = i+2
    else:
        print "Error: Even number of players needed to make swiss pairings."

    db.close()
    return result
