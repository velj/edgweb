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

            if restartedgame == 1:
         variables = RequestContext(request,{
        'head_tite': 'edgWEB_restarted',
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
        'scoreslistFULL': None
        })