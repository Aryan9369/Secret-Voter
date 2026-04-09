from django.urls import path
from .views import (
    CreatePollView, ActivePollListView, 
    CastVoteView, PollResultView, RevealResultsView
)

urlpatterns = [
    path('polls/create/', CreatePollView.as_view(), name='create_poll'),
    path('polls/', ActivePollListView.as_view(), name='list_polls'),
    path('polls/vote/', CastVoteView.as_view(), name='cast_vote'),
    path('polls/<int:pk>/results/', PollResultView.as_view(), name='poll_results'),
    path('polls/<int:pk>/reveal/', RevealResultsView.as_view(), name='reveal_results'),
]