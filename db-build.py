# Build initial database for blog-comp

import sqlite3

with sqlite3.connect("sports_stats.db") as connection:
    c = connection.cursor()
    #c.execute('CREATE TABLE soccer (season TEXT, player TEXT, club TEXT, competition TEXT, goals INT)')
    soccer_data = [('2014-2015', 'Sergio Aguero', 'Manchester City', 'Barclays Premier League', 20),
                   ('2014-2015', 'Harry Kane', 'Tottenham', 'Barclays Premier League', 20),
                   ('2014-2015', 'Diego Costa', 'Chelsea', 'Barclays Premier League', 19),
                   ('2014-2015', 'Charlie Austin', 'Queens Park Rangers', 'Barclays Premier League', 17),
                   ('2014-2015', 'Olivier Giroud', 'Arsenal', 'Barclays Premier League', 14),
                   ('2014-2015', 'Cristiano Ronaldo', 'Real Madrid', 'Spanish Premera Division', 39),
                   ('2014-2015', 'Lionel Messi', 'Barcelona', 'Spanish Primera Division', 35)]
    c.executemany('INSERT INTO soccer VALUES(?, ?, ?, ?, ?)', soccer_data)
