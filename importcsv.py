import csv
import sys
import MySQLdb
print "POOP!"
i=0
#f = open(sys.argv[1], 'rt')
f = open("/home/eric/edgweb/edgweb/attachments/scorecard.csv", 'rt')


#accepts a list
def getholecount(alist):
	print "yay"
	print alist
	count = 0
	for hole in alist:
		if hole[0][0] == "H":
			count =1+count
	### subtrack 1 becuase 1 gets added for "H"andicap
	return count-1


#accepts a list
def getholescore(row,hole):
	if hole <= holecount:
		score= row[hole+1]
	else:
		score=0
	return score	




db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="eric", # your password
                      db="library_development") # name of the data base


# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT * FROM polls_players")

##### Get all the usernames
userlist = []
#grab users with IDs
userlistIDs= []
# print all the first cell of all the rows
for row in cur.fetchall() :
    print row[2] +" " + row[3]
    poop = row[2] +" " + row[3]
    peep = row[0]
    userlistIDs.append(peep)
    userlist.append(poop)

# Use all the SQL you like
cur.execute("SELECT * FROM polls_coursemaster")

##### get all the courses
courselist = []
courselistID = []
# print all the first cell of all the rows
for row in cur.fetchall() :
    print row[1]
    print row[0]
    poop = row[1]
    courselist.append(poop)
    courselistID.append(row[0])

#intialize the round id
roundID=0

#new round flag
newround = "TRUE"

try:
    reader = csv.reader(f)
    for row in reader:
        print row
        ### grab the coursename
        if i==0:
        	coursename = row[0]
        	### check if the coursename exists and add it if it doesnt
        	t=0
        	for courses in courselist:
        			if coursename == courses:
        				print "course is in the database"
        				coursetobeadded = "FALSE"
        				courseID=courselistID[t]
        				
        				break
        			else:
        				print "course is not in the database "
        				coursetobeadded = "TRUE"
        			t=1+t
        if coursetobeadded == "TRUE":
        	print coursename
        	cur.execute("INSERT INTO polls_coursemaster (coursename, Holes, Par, Distance) VALUES (%s,18,54,0)", coursename)
        	##commit DB changes
        	db.commit()
        	print "added %s" % cur.lastrowid
        	couseID=cur.lastrowid
        	#course is added
        	coursetobeadded = "FALSE"

        i=1

        ####get hole Count
        try:
        	### get the number of holes
        	if row[0] == "Player":
        		print "HOLECOUNT"
        		holecount=getholecount(row)
        except:
        	## dont stop on error
        	pass
        ###/hole count end
        	
        ###search playername (first value) and compare if it is in the database -- skips lines that have no values
        ##iterates to get the player ID
        z=0
        try:
        	for user in userlist:
        		if row[0] == user:
        			print "they are in the database"
        			###add the found players score to database here!!!!!!!!!!!!!!!!!!!!!!!!!!!
        			if newround == "TRUE":
        				newround="FALSE"
        				## add new round to DB [need the round ID and courseID]	
        				cur.execute("INSERT INTO polls_rounds (courseID) VALUES (%s)", courseID)
        				#commit DB changes
        				db.commit()
        				print "the course ID is:" + str(courseID)
        				roundID = cur.lastrowid
        			
        			roundtotal=  row[holecount+1]
        			print roundtotal	
        			userID = userlistIDs[z]
        			print holecount

        			#this is a test script to return each score indivituallySELECT * FROM `polls_rounds` WHERE 1
        			v=0
        			hscore=[]
        			while v <18:
        				hscore.append(getholescore(row,v))
        				print hscore
        				v=1+v
        			#INSERT INTO `polls_scores`(`id`, `ROUNDID`, `PLAYERID`, `Holes`, `Score`, `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `h7`, `h8`, `h9`, `h10`, `h11`, `h12`, `h13`, `h14`, `h15`, `h16`, `h17`, `h18`) VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7],[value-8],[value-9],[value-10],[value-11],[value-12],[value-13],[value-14],[value-15],[value-16],[value-17],[value-18],[value-19],[value-20],[value-21],[value-22],[value-23])
        			#getholescore(row,0)
        			#getholescore(row,1)
        			#getholescore(row,2)
        			#getholescore(row,3)
        			#3getholescore(row,4),getholescore(row,5),getholescore(row,6),getholescore(row,7),getholescore(row,8),getholescore(row,9),getholescore(row,10),getholescore(row,11),getholescore(row,12),getholescore(row,13),getholescore(row,14),getholescore(row,15),getholescore(row,16),getholescore(row,17)
        			cur.execute("INSERT INTO polls_scores (ROUNDID, PLAYERID, Holes, Score, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (roundID,userID,holecount,roundtotal,hscore[0],hscore[1],hscore[2],hscore[3],hscore[4],hscore[5],hscore[6],hscore[7],hscore[8],hscore[9],hscore[10],hscore[11],hscore[12],hscore[13],hscore[14],hscore[15],hscore[16],hscore[17]))
        			#commit DB changes
        			db.commit()

        		z=1+z




        except:
        	## i break here instead of skipping the line because i dont need to accoutn for penalties
        	break






        ##jump for joy!

    




finally:
    f.close()

print coursename
print userlist
print courselist
print "does the course need to be added to the database: " + coursetobeadded
print "the course ID is:" + str(courseID)
##close cursor and DB connections
cur.close()
db.close()