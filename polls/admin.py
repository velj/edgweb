from django.contrib import admin
from polls.models import Choice, Poll, Players, CourseMaster, Rounds, Scores

#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question', 'pub_date', 'was_published_recently')	
    list_filter = ['pub_date']	
    search_fields = ['question']
    date_hierarchy = 'pub_date'

class PlayersAdmin(admin.ModelAdmin):
    list_display = ('username', 'FirstName', 'LastName', 'Password')	
class CourseAdmin(admin.ModelAdmin):
    list_display = ('coursename', 'Holes', 'Par', 'Distance')	
class RoundsAdmin(admin.ModelAdmin):
    list_display = ('roundID','courseID')
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('roundID','playerID','Score','h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14','h15','h16','h17','h18')
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Players,PlayersAdmin)
admin.site.register(CourseMaster,CourseAdmin)
admin.site.register(Rounds,RoundsAdmin)
admin.site.register(Scores,ScoresAdmin)
