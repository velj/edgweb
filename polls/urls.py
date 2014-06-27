from django.conf.urls import patterns, url
from polls import views

urlpatterns = patterns('',
    #####################################long way
    # ex: /polls/
    # url(r'^$', views.PlayersView, name='index'),
    # ex: /polls/5/
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    #####################################shorter way with generic views
    
    url(r'^$', views.index, name='index'),
    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'logout/$', views.logout_page),
    url(r'register/$', views.register_page),
    url(r'^user/(\w+)/$', views.user_page),    
    url(r'newround/$', views.new_round),
    url(r'addplayers/$', views.addplayers),
    url(r'gamestart/$', views.gamestart),
    url(r'game/$', views.game),
    url(r'finalscorecard/$', views.finalscorecard),
    url(r'stats/$', views.stats),
    url(r'statsview/$', views.statsview),
    url(r'settings/$', views.settings),
    url(r'addfriend/$', views.addfriend),
    url(r'removefriend/$', views.removefriend),
    url(r'friendsearch/$', views.friendsearch),
    url(r'friendsubmit/$', views.friendsubmit),



    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),

)


urlpatterns += patterns(”,
(r’^static/(?P.*)$’, ‘django.views.static.serve’, {‘document_root’: settings.STATIC_ROOT}),
)
