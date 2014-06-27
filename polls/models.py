from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
 
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now
    #used to set the admin page more pretty
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    #

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


#players model##################################################################################
class Players(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.username
    #playerid = models.id
    username = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50,default=0)
#Courses model##################################################################################
class CourseMaster(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.coursename
    def courseid(self):
        return self.courseID
    courseID = models.AutoField(primary_key=True,db_index=True)
    coursename = models.CharField(max_length=50)
    Holes = models.IntegerField(default=0)
    Par = models.IntegerField(default=0)
    Distance = models.IntegerField(default=0)

#Rounds model##################################################################################
class Rounds(models.Model):
  #  def __unicode__(self):  # Python 3: def __str__(self):
  #      return self.roundID
    roundID = models.AutoField(primary_key=True,null=False,unique=True)
    courseID = models.ForeignKey(CourseMaster,db_column='courseID')
    def get_roundid(self):
        return self.roundID
    def get_courseid(self):
        return self.courseID

#Rounds model##################################################################################
class Scores(models.Model):
    def __unicode__(self):
        return u'(%s) %s %s %s %s' % (self.roundID, self.playerID,self.Score,self.h1,self.h2)
    def getplayers(self):  # Python 3: def __str__(self):
        return self.PlayerID
    roundID = models.ForeignKey(Rounds,db_column='ROUNDID')
    playerID = models.ForeignKey(Players,db_column='PLAYERID')
    Holes = models.IntegerField(default=0)
    Score = models.IntegerField(default=0)
    h1 = models.IntegerField(default=0)
    h2 = models.IntegerField(default=0)
    h3 = models.IntegerField(default=0)
    h4 = models.IntegerField(default=0)
    h5 = models.IntegerField(default=0)
    h6 = models.IntegerField(default=0)
    h7 = models.IntegerField(default=0)
    h8 = models.IntegerField(default=0)
    h9 = models.IntegerField(default=0)
    h10 = models.IntegerField(default=0)
    h11 = models.IntegerField(default=0)
    h12 = models.IntegerField(default=0)
    h13 = models.IntegerField(default=0)
    h14 = models.IntegerField(default=0)
    h15 = models.IntegerField(default=0)
    h16 = models.IntegerField(default=0)
    h17 = models.IntegerField(default=0)
    h18 = models.IntegerField(default=0)
    h19 = models.IntegerField(default=0)
    h20 = models.IntegerField(default=0)
    h21 = models.IntegerField(default=0)
    h22 = models.IntegerField(default=0)
    h23 = models.IntegerField(default=0)
    h24 = models.IntegerField(default=0)
    h25 = models.IntegerField(default=0)
    h26 = models.IntegerField(default=0)
    h27 = models.IntegerField(default=0)
    h28 = models.IntegerField(default=0)
    h29 = models.IntegerField(default=0)
    h30 = models.IntegerField(default=0)
    h31 = models.IntegerField(default=0)
    h32 = models.IntegerField(default=0)
    h33 = models.IntegerField(default=0)
    h34 = models.IntegerField(default=0)
    h35 = models.IntegerField(default=0)
    h36 = models.IntegerField(default=0)
#Friends model##################################################################################
class Friends(models.Model):
  #  def __unicode__(self):  # Python 3: def __str__(self):
  #      return self.roundID
    UserID = models.ForeignKey(Players,db_column='UserID',related_name='FPUserID')
    FriendUserID = models.ForeignKey(Players,db_column='FriendUserID',related_name='FPFriendUserID')
    def get_UserID(self):
        return self.UserID
    def get_FriendUserID(self):
        return self.FriendUserID

    class Meta:
        unique_together = ("UserID", "FriendUserID")



   

