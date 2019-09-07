from django.urls import path
from stadium_tracker import views

app_name = 'stadium_tracker'


urlpatterns = [
    path('', views.GamesSeenListView.as_view(), name='gamesseen_list'),
    path('games/<int:pk>', views.GamesSeenDetailView.as_view(), name='gamesseen_detail'),
    path('games/new', views.GamesSeenCreate.as_view(), name='gamesseen_new'),
    path('games/delete/<int:pk>', views.GamesSeenDelete.as_view(), name='gamesseen_delete'),
    path('venues', views.VenueList.as_view(), name= 'venue_list'),
]