from django.urls import path
from . import views

app_name = 'stadium_tracker'


urlpatterns = [
    path('', views.GamesSeenListView.as_view(), name='gamesseen_list'),
    path('<int:pk>', views.GamesSeenDetailView.as_view(), name='gamesseen_detail'),
    path('new', views.GamesSeenCreate.as_view(), name='gamesseen_new'),
    path('edit/<int:pk>', views.GamesSeenUpdate.as_view(), name='gamesseen_edit'),
    path('delete/<int:pk>', views.GamesSeenDelete.as_view(), name='gamesseen_delete'),
]