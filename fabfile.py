from fabric.api import local

def deploy():
# local('pip freeze > requirements.txt')
 local('sudo git add .')
 print("enter your git commit comment: ")
 comment = raw_input()
 local('sudo git commit -m "%s"' % comment)
 local('sudo git push -u origin master')
# local('heroku maintenance:on')
 local('git push heroku master')
# local('heroku maintenance:off')
