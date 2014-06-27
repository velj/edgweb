# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll, Players, CourseMaster, Rounds, Scores,Friends
from django.template import RequestContext, loader, Context
from django.http import Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.template.loader import get_template
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import connection
from polls.forms import *

def index(request):
    template = get_template('polls/index.html')
    # view snippet
    try:
        if request.POST.get('restartedgame'):
            print('Game Restarted')
            restartedgame = 1
        else:
            print('this crap sucks balls')
            restartedgame = 0
    except Exception, e:
        restartedgame=0
        print('newlogin')




    print restartedgame
    if restartedgame == 1:
         variables = RequestContext(request,{
        'head_title': 'edgWEB_restarted',
        'page_title':'edgWEB_restarted',
        'page_body': 'Game Start',
        'courselist': None,
        'form':None,
        'courseid':None,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'players': None,
        'playernames':None,
        'totalholesinround':None,
        'currentHole':None,
        'totalScores':None,
        'listy':None,
        'ScoresFull':None,
        'listy2':None,
        'gamestarted':None,
        'scoreslistFULL': None
        })
        #set the global session variable to False 
         request.session['gamestarted']  = "False"


    else:    
        variables = Context({
        	'head_title': 'edgWEB',
    	'page_title':'Welcome to eDG WEB',
    	'page_body': 'Where you can store and view DG scores',
    	'user': request.user
        })

    restartedgame = 0    

    try:
        playerstest   = request.session['players']
        print playerstest
    except Exception, e:
        print('no playertest')
    
    output= template.render(variables)
    return HttpResponse(output)    

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('../')

def user_page(request, username):
    try:
	user= User.objects.get(username=username)
    except:
	raise Http404('Requested user not found')
    
    template = get_template('polls/user_page.html')
    variables = Context({
	'username':username,
    })
    output= template.render(variables)
    return HttpResponse(output)

def settings(request):
    #try:
    #    user= User.objects.get(username=username)
    #except:
    #    raise Http404('Requested user not found')
    
    template = get_template('polls/settings.html')
    variables = Context({
    #'username':username,
    'user': request.user
    })
    output= template.render(variables)
    return HttpResponse(output)

def register_page(request):
    if request.method == 'POST':
	form = RegistrationForm(request.POST)
	if form.is_valid():
		user=User.objects.create_user(
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password1'],
			email=form.cleaned_data['email']
		)

        #Here we want to grab the user that was just created, and turn them into a Player
        LastUser = User.objects.get(username=form.cleaned_data['username'])

        #insert new user into player table

        NewPlayer = Players(id=LastUser.id,username=LastUser.username, FirstName=request.POST["firstname"], LastName=request.POST["lastname"], Password='none')
        NewPlayer.save()

        

        

        return HttpResponseRedirect('../')
    else:
	form =RegistrationForm()
    variables = RequestContext(request, {
	'form': form
    })
    return render_to_response('registration/register.html' ,variables)

def new_round(request):
    template = get_template('polls/newround.html')
    form = MyForm()
    courselist = CourseMaster.objects.all()
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'courselist': courselist,
    'form':form,
    'user': request.user
    })
    
    output= template.render(variables)
    return HttpResponse(output)
def stats(request):
    template = get_template('polls/stats.html')
    form = MyForm()
    courselist = CourseMaster.objects.all()
    statscheck = "True"
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'courselist': courselist,
    'form':form,
    'statscheck':statscheck,
    'user': request.user

    })
    
    output= template.render(variables)
    return HttpResponse(output)


def addplayers(request):
    #this draws the add players page.
    template = get_template('polls/addplayers.html')
    form = addplayersForm()
    #save the posted data to a variable and save it to a global session this is: courseid
    content = request.POST["my_choice_field"]
    request.session['courseid'] = content

    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'form':form,
    'content':content,
    'user': request.user
    })

    


    output= template.render(variables)
    return HttpResponse(output)


def statsview(request):
    # players and course already Posted
    template = get_template('polls/statsview.html')
    #get global variable courseid
    courseid=request.POST["my_choice_field"]
 
    courselist = CourseMaster.objects.all()
  
    ##get Number of holes at the course
    course_obj = CourseMaster.objects.get(courseID=courseid)
    totalholesinround=course_obj.Holes
    request.session['totalholesinround'] = totalholesinround
    coursename = course_obj

    #Get course information from the database
    #need to get the course object with the id of the course selected and then insert it into the database:
    
    ##send the course id to getSTATS function
    d = getSTATS(0,courseid)
    row=0
    col=6
    total=0
    highscore=0
    lowscore=10000

    ####gets average and total rounds, highestscore and lowest score
    ## set intital values for high and low score
    for a in d:
        d[row][col]
        total = d[row][col]  + total
        if d[row][col] >= highscore:
            highscore=d[row][col]
        if d[row][col] <= lowscore:
            lowscore = d[row][col]
        
        row = row + 1 

    averagescore = total/row
    #################################



    variables = RequestContext(request,{
            'head_tite': 'edgWEB',
        'page_title':'eDG WEB',
        'page_body': 'Game Start',
        'courselist': courselist,
        'courseid':courseid,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'totalholesinround':totalholesinround,
        'coursename':coursename,
        'highscore':highscore,
        'lowscore':lowscore,
        'averagescore':averagescore,
        'row':row
         })      


    output= template.render(variables)
    return HttpResponse(output)


####################################################################


def gamestart(request):
    # players and course already Posted
    template = get_template('polls/gamestart.html')
    #get global variable courseid
    courseid=request.session.get('courseid')
    #save the posted data to a variable and save it to a global session
    players = request.POST.getlist("my_choice_field")
    request.session['players'] = players

    #pull all available players from the games table
    form = addplayersForm()

    courselist = CourseMaster.objects.all()
    ####get player usernames
    playernames = []
    for player in players:
        playerlist = (Players.objects.get(id=player) )
        playernames.append(playerlist)
    ##get Number of holes at the course
    course_obj = CourseMaster.objects.get(courseID=courseid)
    totalholesinround=course_obj.Holes
    request.session['totalholesinround'] = totalholesinround

    ## Set Starting hole to 1
    currentHole = 1
    request.session['currentHole'] = currentHole


    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'eDG WEB',
    'page_body': 'Game Start',
    'courselist': courselist,
    'form':form,
    'courseid':courseid,
    #gets the logged int username
    'user': request.user,
    #list of all the players IDs in the round 
    'players': players,
    'playernames':playernames,
    'totalholesinround':totalholesinround,
    'currentHole':currentHole

    })
    #USED TO troubleshoot only
    print players
    #insert newround into the database
    #need to get the course object with the id of the course selected and then insert it into the database:
    if request.session.get('gamestarted') != "True":
        #Check if the round exists already first so it doesnt duplicate the round as a new one if re-POSTED
        newround_add = CourseMaster.objects.get(courseID=courseid)
        c_add=Rounds(courseID=newround_add)
        c_add.save()
        c_add.roundID
        #add the round ID to a global
        request.session['currentRoundID']  = c_add.roundID

        #set the global session variable to true 
        request.session['gamestarted']  = "True"
        
        #insert players into database for the round
        for p_add in players:
            p_add_obj = Players.objects.get(id=p_add)
            c_add_obj = Rounds.objects.get(roundID=c_add.roundID)
            s_add = Scores(playerID=p_add_obj,roundID=c_add_obj)
            s_add.save()
    else:
        print "Error"
        return HttpResponseRedirect("/polls/")

    output= template.render(variables)
    return HttpResponse(output)


####################################################################


def game(request):
   
    if request.session.get('gamestarted') == "True":
        ## increment to the next hole!  Then save it in the gobal variable
        currentHole=request.session.get('currentHole') + 1
        request.session['currentHole'] = currentHole



        # players and course already Posted
        template = get_template('polls/game.html')
        #get global variable courseid
        courseid=request.session.get('courseid')
        #save the posted data to a variable and save it to a global session
        #players = request.POST.getlist("my_choice_field")
        players = []
        players = request.session.get('players')

        #pull all available players from the games table
        form = addplayersForm()

        courselist = CourseMaster.objects.all()
        ####get player usernames
        playernames = []
        for player in players:
            playerlist = (Players.objects.get(id=player) )
            playernames.append(playerlist)
        ##get Number of holes at the course
        course_obj = CourseMaster.objects.get(courseID=courseid)
        totalholesinround=course_obj.Holes

        

        variables = RequestContext(request,{
            'head_tite': 'edgWEB',
        'page_title':'eDG WEB',
        'page_body': 'Game Start',
        'courselist': courselist,
        'form':form,
        'courseid':courseid,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'players': players,
        'playernames':playernames,
        'totalholesinround':totalholesinround,
        'currentHole':currentHole
        })

        ###### insert scores into the database
        #need to get the current roundid and the playerID and hole we are on and then insert it into the database:
        currentRoundID = request.session.get('currentRoundID')



        for playersscore in players:
            #playersPOSTEDscore = request.POST.get('velj')
            player_add_obj = Players.objects.get(id=playersscore)
            #print player_add_obj.username
            playersPOSTEDscore = request.POST.get(player_add_obj.username)
            round_add_obj = Rounds.objects.get(roundID=currentRoundID)
            addScores = Scores.objects.get(roundID=currentRoundID,playerID=playersscore)
            hole= "h"+str(currentHole-1)
            #print  request.POST.get('velj')
            #addScores.hole = 2
            setattr(addScores, hole, playersPOSTEDscore)
            addScores.save()   
            
            ####add the total scorefor each player and insert into the database
            Score = "Score"
            print  currentHole
            totalpoop = int(addScores.h1) + int(addScores.h2) + int(addScores.h3) + int(addScores.h4)+ int(addScores.h5)+ int(addScores.h6)+ int(addScores.h7)+ int(addScores.h8)+ int(addScores.h9)+ int(addScores.h10)+ int(addScores.h11)+ int(addScores.h12)+ int(addScores.h12)+ int(addScores.h14)+ int(addScores.h15)+ int(addScores.h16)+ int(addScores.h17)+ int(addScores.h18)
            setattr(addScores,Score, totalpoop )
            addScores.save() 
            #p = Scores.objects.filter(roundID=currentRoundID)
            #add = p[playersscore].h1 + p[playersscore].h2 + p[playersscore].h3 
            #Scores.objects.filter(roundID=currentRoundID,playerID=playersscore).update(Score=add)

        ######### End insert scores into the database  

       
         ####get the totalScores
        totalScores = []
        for player in players:
            scoreslist = (Scores.objects.get(roundID=currentRoundID,playerID=player))
            totalScores.append(scoreslist.Score)

                     ####get everyscore
        ScoresFull = []
        
        scoreslistFULL = (Scores.objects.filter(roundID=currentRoundID))

     
        print scoreslistFULL        
        listy = zip(playernames, totalScores)
        #print listy

        listy2 = zip(playernames, ScoresFull)
        #print listy2
        variables = RequestContext(request,{
        'head_tite': 'edgWEB',
        'page_title':'eDG WEB',
        'page_body': 'Game Start',
        'courselist': courselist,
        'form':form,
        'courseid':courseid,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'players': players,
        'playernames':playernames,
        'totalholesinround':totalholesinround,
        'currentHole':currentHole,
        'totalScores':totalScores,
        'listy':listy,
        'ScoresFull':ScoresFull,
        'listy2':listy2,
        'scoreslistFULL':scoreslistFULL
        })

        #The game has ended go the endgamepage
        ##! create endgamepage and clear session values so a noew game can start:
        if currentHole > request.session['totalholesinround']:
            ##return HttpResponseRedirect('../')
            return HttpResponseRedirect('../finalscorecard')
          

        output= template.render(variables)
        return HttpResponse(output)
    #if the game flag isnt set then just redirect to the login screen
    else:
        return HttpResponseRedirect("/polls/")

def finalscorecard(request):




    if request.session.get('gamestarted') == "True":
        ## increment to the next hole!  Then save it in the gobal variable
        currentHole=request.session.get('currentHole') + 1
        request.session['currentHole'] = currentHole

        # players and course already Posted
        template = get_template('polls/finalscorecard.html')
        #get global variable courseid
        courseid=request.session.get('courseid')
        #save the posted data to a variable and save it to a global session
        #players = request.POST.getlist("my_choice_field")
        players = []
        players = request.session.get('players')

        #pull all available players from the games table
        form = addplayersForm()

        courselist = CourseMaster.objects.all()
        ####get player usernames
        playernames = []
        for player in players:
            playerlist = (Players.objects.get(id=player) )
            playernames.append(playerlist)
        ##get Number of holes at the course
        course_obj = CourseMaster.objects.get(courseID=courseid)
        totalholesinround=course_obj.Holes

        holesrange = float(totalholesinround)

        variables = RequestContext(request,{
        'head_tite': 'edgWEB',
        'page_title':'eDG WEB',
        'page_body': 'Game Start',
        'courselist': courselist,
        'form':form,
        'courseid':courseid,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'players': players,
        'playernames':playernames,
        'holesrange':holesrange,
        'totalholesinround':totalholesinround,
        'currentHole':currentHole
        })

      
        #need to get the current roundid and the playerID and hole we are on and then insert it into the database:
        currentRoundID = request.session.get('currentRoundID')
       
         ####get the totalScores
        totalScores = []
        for player in players:
            scoreslist = (Scores.objects.get(roundID=currentRoundID,playerID=player))
            totalScores.append(scoreslist.Score)

                     ####get everyscore
        ScoresFull = []
        
        scoreslistFULL = (Scores.objects.filter(roundID=currentRoundID))

     
        print scoreslistFULL        
        listy = zip(playernames, totalScores)
        #print listy

        listy2 = zip(playernames, ScoresFull)
        #print listy2
        variables = RequestContext(request,{
        'head_tite': 'edgWEB',
        'page_title':'eDG WEB',
        'page_body': 'Game Start',
        'courselist': courselist,
        'form':form,
        'courseid':courseid,
        #gets the logged int username
        'user': request.user,
        #list of all the players IDs in the round 
        'players': players,
        'playernames':playernames,
        'totalholesinround':totalholesinround,
        'currentHole':currentHole,
        'totalScores':totalScores,
        'listy':listy,
        'ScoresFull':ScoresFull,
        'listy2':listy2,
        'scoreslistFULL':scoreslistFULL
        })
        output= template.render(variables)
        return HttpResponse(output)
    else:
        return HttpResponseRedirect("/polls/")

################################################################

#def index(request):
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #context = {'latest_poll_list': latest_poll_list}
    #return render(request, 'polls/index.html', context)
    
    ## output = ', '.join([p.question for p in latest_poll_list])
    ## return HttpResponse(output)
    ##template = loader.get_template('polls/index.html')
    ##context = RequestContext(request, {
    ##    'latest_poll_list': latest_poll_list,
    ##})
    ##return HttpResponse(template.render(context)) 


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def getSTATS(self,cid):
    courseid_obj = CourseMaster.objects.get(courseID=cid)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM `polls_rounds` inner join polls_scores on polls_rounds.roundID=polls_scores.ROUNDID Where polls_rounds.courseID = %s and polls_scores.PLAYERID=1',[courseid_obj.courseID])
    row = cursor.fetchall()
    return row
###########Settings page add and remvoe friends#####################################################

def addfriend(request):
    friendsearchresults=False
    friendadded = False
    #display the search page if a search wasnt started
    if friendsearchresults==False:
        template = get_template('polls/addfriend.html')
        form = addFriendForm()
    else:
        #a search was not posted .. redirect to mainpage
            return HttpResponseRedirect("/polls/")

    ##### Variables
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'form':form,
    'user': request.user
    })
    ##### Build Page
    output= template.render(variables)
    return HttpResponse(output)     
#Friend Pages #####################################################################################################################################################################
def friendsearch(request):
    #set some flags
    friendsearchresults=True
    found = False
    friendadded = False
    #display the search page if a search wasnt started
    if friendsearchresults==True:
        #### SEARCH FOR FRIEND#### if friend was found!
        template = get_template('polls/friendsearch.html')
        form = addFriendForm(request.POST)
        ####### see if the user exists  and verify that they arent searching for themselves.
        try:
            foundusername = User.objects.get(username=request.POST["username"]) 
            request.session['foundusername'] = foundusername
            found = True
        except Exception, e:
            foundusername = "username not found"

        #verify they cant befriends awith themselves
        if foundusername == request.user:
            foundusername="That's you sillly"
            #username was found but set it to false so the add button isnt displayed
            found = False
        ###################################################################################



    else:
        #a search was not posted .. redirect to mainpage
        return HttpResponseRedirect("/polls/")###################################################################################


    ##### Variables
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'form':form,
    'user': request.user,
    'found': found,
    'foundusername':foundusername
    })
  
    ##### Build Page
    output= template.render(variables)
    return HttpResponse(output)		

def removefriend(request):
    friendadded = False
    template = get_template('polls/removefriend.html')
    form = MyForm()
    courselist = CourseMaster.objects.all()
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'courselist': courselist,
    'form':form,
    'user': request.user
    })
    
    output= template.render(variables)
    return HttpResponse(output)     

def friendsubmit(request):

    
    try:

        fuser=request.session.get('foundusername')   
        #since friends have foreign keys to players model... must get a players object 
        user = Players.objects.get(id=request.user.id)
        friend  = Players.objects.get(id=fuser.id)
        #add the players objects to the friends table
        FriendPlayer = Friends(UserID=user, FriendUserID=friend)
        FriendPlayer.save()     
        print "Friend added"
        friendadded = True


    except Exception, e:
        print "Friend add failed"


    template = get_template('polls/friendsubmit.html')
    form = MyForm()
    courselist = CourseMaster.objects.all()
    variables = RequestContext(request,{
        'head_tite': 'edgWEB',
    'page_title':'Welcome to eDG WEB',
    'page_body': 'Where you can store and view DG scores',
    'courselist': courselist,
    'form':form,
    'friendadded':friendadded,
    'user': request.user

    })
    
    output= template.render(variables)
    return HttpResponse(output)  