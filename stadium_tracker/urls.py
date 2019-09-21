from django.urls import path
from stadium_tracker import views

app_name = 'stadium_tracker'


urlpatterns = [
    path('', views.GamesViewList.as_view(), name='game_list'),
    path('games/new', views.GameDetailCreate.as_view(), name='gamedetails_create'),
    path('venues', views.VenueList.as_view(), name='venue_list'),
    path('games/<int:pk>', views.GameDetailView.as_view(), name='gamedetails_list'),
    path('games/delete/<int:pk>', views.GameDetailDelete.as_view(), name='gamesseen_delete'),
]