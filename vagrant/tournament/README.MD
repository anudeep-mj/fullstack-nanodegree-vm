# Tournament Database

Implementation of database design for swiss-system tournament. Contains the required functions to register players,
register matches, delete players, delete matches, report players standings and make swiss pairings.

### Prerequisites

```
python latest version installed.
postgres latest version installed.
Python modules needed:
- psycopg2
- bleach

```

### How to run the code.

```
1. Download the zip.
2. Extract the zip.
3. Go to the extracted folder in the terminal.
4. Run the sql file to create the tables and views. To do this, go to the tournament folder and run the command, "psql -f tournament.sql".
This will create the database tournament and the tables within. To connect to the database you can use the command, "psql tournament" and check out the table descriptions using the command, "\d+ playerlist", "\d+ matchlist"

5. Run the test file, tournament_test.py to run the same code which contains tests and usage of the functions.
```