#!/usr/bin/env python
""" tournament.py -- implementation of a Swiss-system tournament
"""


import psycopg2


def connect(database_name='tournament'):
    """ Connect to the PostgreSQL database.  Returns a database connection.

        Args:
            database_name - String, name of database.  Default is "tournament"

        Returns:
            conn - instance, database connection object.
            cur - instance, database cursor
    """

    try:
        conn = psycopg2.connect('dbname={}'.format(database_name))
        cur = conn.cursor()
        return conn, cur
    except:
        print 'Can not connect to database'


def deleteMatches():
    """Remove all the match records from the database."""

    conn, cur = connect()
    cur.execute('''DELETE FROM matches;''')
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""

    conn, cur = connect()
    cur.execute('''DELETE FROM players;''')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn, cur = connect()
    cur.execute('''SELECT COUNT(player_id) FROM players;''')
    result = cur.fetchone()
    conn.close()
    return result[0] # Retuns the first index from tuple

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's first name and last name (need not be unique).
    """

    conn, cur = connect()
    cur.execute('INSERT INTO players (name) values (%s)', (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their point records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, points, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches the number of matches the player has played
    """

    conn, cur = connect()
    cur.execute('SELECT * FROM standings;') # Uses view to keep code cleaner
    results = cur.fetchall()
    conn.close()
    return results

def reportMatch(winner, loser, tie=False):
    """Records the outcome of a single match between two players.  If there
        Is no tie, the winner recieves 3 points and the loser receives 0
        points.   If there is a tie, both players receive 1 point.  points
        are recorded in the points table.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tied:  Bool, True if there was tie.  Defaults to False
    """

    conn, cur = connect()

    cur.execute('INSERT INTO matches (winner, loser, tied)'
                'VALUES (%s, %s, %s)', (winner, loser, tied))
    conn.commit()
    conn.close()


def reportBye(player_id):
    """ Records a bye when there is an odd number of registrants during
        a pairing.  When a player receives a bye, 3 points is added to
        the points table with their ID.  The player's ID is also added to
        the byes table to keep track of the fact that they have received a
        bye.

        Args:
            player_id - Integer, ID of the player receiving a bye
    """
    conn, cur = connect()
    cur.execute('INSERT INTO matches (winner, tied)'
                'VALUES (%s, False)', (player_id,))
    conn.commit()
    conn.close()

def checkPreviousBye(player_id):
    """ Recieves a player ID and checks to see if that player has previously
        received a bye.  Returns True if the player has had a bye, otherwise
        returns false.

        Args:
            player_id - Int, a player's unique id.

        Returns:
            Boolean, True if player has had a bye, otherwise False.
    """

    conn, cur = connect()
    # Check to see if the player is already in the byes table
    cur.execute('SELECT winner FROM matches WHERE winner = %s '
                'and loser IS NULL', (player_id,))
    result = cur.fetchone()
    conn.close()
    if result is None:  # if the id is not found, return "False"
        return False
    else:
        return True     # Otherwise, return "True"


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

    pairings = []  # Create list to store pairings in during itteration
    standings = playerStandings()   # Get the current standings.
    # Loop through the current standings.  On each loop, pop the last
    # player in the list, then loop through the remaining players looking
    # for a plyer tha has played the same number of matches and has the same
    # number of wins.  End when there are no more players in the list.

    # Check to see if there is an odd number of players.  If so, find a player
    # who has not received a bye, yet.
    if len(standings) % 2 != 0:
        for index, player in enumerate(standings):
            if not checkPreviousBye(player[0]):
                reportBye(player[0])    # Give them a bye
                del standings[index]    # Delete them from the list
                break

    while standings:
        player1 = standings.pop()
        player2 = ''
        score = player1[2]
        while player2 == '':
            for index, player in enumerate(standings):
                if player[2] == score and player[3] == player1[3]:
                    if player[3] == standings[index][3]:
                        player2 = standings.pop(index)
                        break
            score += 1

        # Add the pairs to the pairings list as tuples.
        pairings.append((player1[0], player1[1],
                        player2[0], player2[1]))

    return pairings  # Return list of pairings
