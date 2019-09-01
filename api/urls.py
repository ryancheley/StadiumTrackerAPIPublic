from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from api.views import GamesSeenList, GamesSeenDetail

schema_view = get_swagger_view(title='Games Seen API')

urlpatterns = [
    path('games/', GamesSeenList.as_view()),
    path('games/<int:pk>', GamesSeenDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view),

]