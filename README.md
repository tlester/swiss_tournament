# Swiss Tournament Results
This is a python application that manages Swiss Tournament pairings and rankgs.

## Features
- Player registration:  Register a player, auto assign a unique player ID.
- Automatic Pairing:  Pair players up based on randing from match to match.
- Tie handling:  Ties are handled through a point system.
- Odd number of players (byes):  Odd number of players are handled via "byes".  Players can only receive a bye once.

## Install
To install from git, run the following command:
```
git clone https://github.com/tlester/rdb-fullstack.git
cd vagrant/tournament 
```
create a postgres DB and name it "tournament".  Then run:
```
psql tournament -f tournament.sql 
```
This will build the tournament tables

## Usage / Customization

Load this module into your website or tournament application.  Read the
docstrings to get info on function usage.

.
