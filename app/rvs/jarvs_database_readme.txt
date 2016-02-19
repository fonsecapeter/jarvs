to make database:
TERMINAL
pfonseca@peterinstance:~$ sqlite3 RVS.db

SQLite version 3.8.2 2013-12-06 14:53:30
Enter ".help" for instructions
Enter SQL statements terminated with a ";"

sqlite> CREATE TABLE Preferences
		(
		USERNAME TEXT NOT NULL,
		USEREMAIL TEXT NOT NULL,
		USERCOLOR TEXT NOT NULL,
		JARVSCOLOR TEXT NOT NULL,
		BACKGROUNDCOLOR TEXT NOT NULL
		);

sqlite> CREATE TABLE Attendings
		(
		ID INT PRIMARY KEY NOT NULL,
		FNAME TEXT NOT NULL,
		LNAME TEXT NOT NULL,
		DIRNAME TEXT NOT NULL,
		EMAIL TEXT NOT NULL
		);

to crud Preferences:
PYTHON
>>> import dataset

>>> db = dataset.connect('sqlite:///RVS.db')
>>> table = db['Preferences']

>>> table.insert(dict(USERNAME='Peter', USEREMAIL='peter.nfonseca@gmail.com', USERCOLOR='white', JARVSCOLOR='"#e29d36"', BACKGROUNDCOLOR='"#333333"'))

1

to crud Attendings:
BACK TO SAME PYTHON

>>> table = db['Attendings']
>>> table.insert(dict(ID='0', FNAME='Elaine', LNAME='Benes', DIRNAME='/Benes,Elaine/', EMAIL='elaine.benes@fakemail.com'))

1

>>> table.insert(dict(ID='1', FNAME='George', LNAME='Costanza', DIRNAME='/Costanza,George/', EMAIL='george.costanza@fakemail.com'))

2

>>> table.insert(dict(ID='2', FNAME='Peter', LNAME='Fonseca', DIRNAME='/Fonseca,Peter/', EMAIL='peter.fonseca@fakemail.com'))
3
>>> table.insert(dict(ID='3', FNAME='Julius', LNAME='Hibbert', DIRNAME='/Hibbert,Julius/', EMAIL='julius.hibbert@fakemail.com'))
4
>>> table.insert(dict(ID='4', FNAME='Clark', LNAME='Kent', DIRNAME='/Kent,Clark/', EMAIL='super.man@fakemail.com'))
5
>>> table.insert(dict(ID='5', FNAME='Cosmo', LNAME='Kramer', DIRNAME='/Kramer,Cosmo/', EMAIL='ass.man@fakemail.com'))
6
>>> table.insert(dict(ID='6', FNAME='Elizabeth', LNAME='Lemon', DIRNAME='/Lemon,Elizabeth/', EMAIL='the.lizard@fakemail.com'))
7
>>> table.insert(dict(ID='7', FNAME='Lex', LNAME='Luthor', DIRNAME='/Lex,Luthor/', EMAIL='kryptonite@fakemail.com'))
8
>>> table.insert(dict(ID='8', FNAME='Nick', LNAME='Riviera', DIRNAME='/Riviera,Nick/', EMAIL='nick.riviera@fakemail.com'))
9
>>> table.insert(dict(ID='9', FNAME='Jerry', LNAME='Seinfeld', DIRNAME='/Seinfeld,Jerry/', EMAIL='jerry.seinfeld@fakemail.com'))
10
>>> table.insert(dict(ID='10', FNAME='Bob', LNAME='Vance', DIRNAME='/Vance,Bob/', EMAIL='vance.refridgeration@fakemail.com'))
11
>>> table.insert(dict(ID='11', FNAME='Art', LNAME='Vandalay', DIRNAME='/Vandalay,Art/', EMAIL='art.vandalay@fakemail.com'))
12


>>> table.update(dict(ID='7', DIRNAME='/Luthor,Lex/'), ['ID'])

to check back in same sqlite:
SQLITE3

# could have makde update with sql
sqlite> UPDATE Attendings
   ...> SET DIRLNAME = "/Luthor,Lex/"
   ...> WHERE ID = 7;

sqlite> SELECT * FROM Attendings;

0|Elaine|Benes|/Benes,Elaine/|elaine.benes@fakemail.com
1|George|Costanza|/Costanza,George/|george.costanza@fakemail.com
2|Peter|Fonseca|/Fonseca,Peter/|peter.fonseca@fakemail.com
3|Julius|Hibbert|/Hibbert,Julius/|julius.hibbert@fakemail.com
4|Clark|Kent|/Kent,Clark/|super.man@fakemail.com
5|Cosmo|Kramer|/Kramer,Cosmo/|ass.man@fakemail.com
6|Elizabeth|Lemon|/Lemon,Elizabeth/|the.lizard@fakemail.com
7|Lex|Luthor|/Luthor,Lex/|kryptonite@fakemail.com
8|Nick|Riviera|/Riviera,Nick/|nick.riviera@fakemail.com
9|Jerry|Seinfeld|/Seinfeld,Jerry/|jerry.seinfeld@fakemail.com
10|Bob|Vance|/Vance,Bob/|vance.refridgeration@fakemail.com
11|Art|Vandalay|/Vandalay,Art/|art.vandalay@fakemail.com

sqlite> SELECT * FROM Preferences;

Peter|peter.nfonseca@gmail.com|white|"#e29d36"|"#333333"|

# for beter view
sqlite> .mode column
sqlite> .header on
sqlite> .width 2 20 18 40 26
sqlite> SELECT * FROM Attendings;
ID  FNAME                 LNAME               DIRNAME                                   EMAIL                     
--  --------------------  ------------------  ----------------------------------------  --------------------------
0   Elaine                Benes               /Benes,Elaine/                            elaine.benes@fakemail.com 
1   George                Costanza            /Costanza,George/                         george.costanza@fakemail.c
2   Peter                 Fonseca             /Fonseca,Peter/                           peter.fonseca@fakemail.com
3   Julius                Hibbert             /Hibbert,Julius/                          julius.hibbert@fakemail.co
4   Clark                 Kent                /Kent,Clark/                              super.man@fakemail.com    
5   Cosmo                 Kramer              /Kramer,Cosmo/                            ass.man@fakemail.com      
6   Elizabeth             Lemon               /Lemon,Elizabeth/                         the.lizard@fakemail.com   
7   Lex                   Luthor              /Luthor,Lex/                              kryptonite@fakemail.com   
8   Nick                  Riviera             /Riviera,Nick/                            nick.riviera@fakemail.com 
9   Jerry                 Seinfeld            /Seinfeld,Jerry/                          jerry.seinfeld@fakemail.co
10  Bob                   Vance               /Vance,Bob/                               vance.refridgeration@fakem
11  Art                   Vandalay            /Vandalay,Art/                            art.vandalay@fakemail.com 


GET DATA IN BASH
#!/bin/bash
# fetch data from RVS.db
# adapted from andreaolivato.tumblr.com/post/133473114/using-sqlite3-in-bash
# also has info on making and cruding tables/db's

# get all the data
LIST=`sqlite3 RVS.db "SELECT * FROM Attendings"`;

echo "ID > FNAME > LNAME > DIRNAME > EMAIL"

# for each row...
for ROW in $LIST; do
	# parse data (sqlite returns a pip separated string by default)
	ID=`echo $ROW | awk '{split($0,a,"|"); print a[1]}'`
	FNAME=`echo $ROW | awk '{split($0,a,"|"); print a[2]}'`
	LNAME=`echo $ROW | awk '{split($0,a,"|"); print a[3]}'`
	DIRNAME=`echo $ROW | awk '{split($0,a,"|"); print a[4]}'`
	EMAIL=`echo $ROW | awk '{split($0,a,"|"); print a[5]}'`

	# print the data
	echo -e $ID" > "$FNAME" > "$LNAME" > "DIRNAME" > "EMAIL;
done

#!/bin/bash
# fetch data from RVS.db
# adapted from andreaolivato.tumblr.com/post/133473114/using-sqlite3-in-bash
# also has info on making and cruding tables/db's

# get all the data
LIST=`sqlite3 RVS.db "SELECT * FROM Attendings"`

echo "ID > FNAME > LNAME > DIRNAME > EMAIL"

# for each row...
for ROW in $LIST; do
	# parse data (sqlite returns a pip separated string by default)
	ID=`echo $ROW | awk '{split($0,a,"|"); print a[1]}'`
	FNAME=`echo $ROW | awk '{split($0,a,"|"); print a[2]}'`
	LNAME=`echo $ROW | awk '{split($0,a,"|"); print a[3]}'`
	DIRNAME=`echo $ROW | awk '{split($0,a,"|"); print a[4]}'`
	EMAIL=`echo $ROW | awk '{split($0,a,"|"); print a[5]}'`

	# print the data
	echo $ID" > "$FNAME" > "$LNAME" > "DIRNAME" > "EMAIL
done





### Correct way to update!
>>> table.insert(dict(ID='7', FNAME='Lex', LNAME='Luthor', DIRNAME='/Lex,Luthor/', EMAIL='kryptonite@fakemail.com'))

>>> table.update(dict(ID='7', DIRNAME='/Luthor,Lex/'), ['ID'])

# locating column is first and last