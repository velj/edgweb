from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from polls.models import Choice, Poll, Players, CourseMaster, Rounds, Scores
from django.forms.widgets import TextInput

class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username',max_length=30)
	firstname = forms.CharField(label='First Name',max_length=30)
	lastname = forms.CharField(label='Last Name',max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label='Password (Again)',
		widget=forms.PasswordInput()
	)
	
	def clean_username(self):
		username=self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
		 raise forms.ValidationError('Username can only be alpha characters.')
		try:
		 User.objects.get(username=username)
		except ObjectDoesNotExist:
		 return username
		raise forms.ValidationError('Username already taken')
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match')

##class to create a dropdown list of all the courses available
class MyForm(forms.Form):
    #MY_CHOICES = (('1', 'Option 1'),('2', 'Option 2'),('3', 'Option 3'),)
    #MY_CHOICES = CourseMaster.objects.all()
    courses = [] 
    c = CourseMaster.objects.all()
    #for p in CourseMaster.objects.raw('SELECT * FROM polls_coursemaster'):
    for p in c:
    	courseslist = {}
    	courseslist = (p.courseID,p)
    	courses.append(courseslist)  
    my_choice_field = forms.ChoiceField(choices=courses)
    #class to create a dropdown list of all the courses available
class addplayersForm(forms.Form):
    #MY_CHOICES = (('1', 'Option 1'),('2', 'Option 2'),('3', 'Option 3'),)
    #MY_CHOICES = Players.objects.all()
    courses = [] 
    c = Players.objects.all()
    #this is for reference: for p in CourseMaster.objects.raw('SELECT * FROM polls_coursemaster'):
    #i dont think this is actually doing anything???????
    for p in c:
    	courseslist = {}
    	courseslist = (p.id,p)
    	courses.append(courseslist)  

    #gets all the players in the players table for the checkboxes
    my_choice_field = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'checkboxes'}),queryset=Players.objects.all()) 



class NumberInput(TextInput):
    input_type = 'tel'
    #Usage
	#widgets = (
	#    'number_field': NumberInput(attrs={'min': '0', 'max': '10', 'step': '1'}),

	#)

class addFriendForm(forms.Form):
	#Search box for username to add a friend
    username = forms.CharField(label='Username',max_length=30)

    
