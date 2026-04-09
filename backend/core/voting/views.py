from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Poll, Option
from .serializers import PollCreateSerializer, PollListSerializer
from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll, Option, Vote
from .serializers import (
    PollCreateSerializer, PollListSerializer, 
    VoteSerializer, PollResultSerializer
)

class CreatePollView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ActivePollListView(generics.ListAPIView):
    """
    Shows all polls to users. 
    In a real app, you might filter for only 'currently active' polls.
    """
    queryset = Poll.objects.all().order_by('-created_at')
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticated]




class CastVoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RevealResultsView(APIView):
    """Admin only: Manually reveal the results of a poll"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            poll = Poll.objects.get(pk=pk)
            poll.is_result_revealed = True
            poll.save()
            return Response({"message": "Results are now public."})
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=404)

class PollResultView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        poll = self.get_object()
        user = request.user

        # Logic: Show results ONLY if:
        # 1. User is Admin
        # 2. OR Poll is not secret
        # 3. OR Admin has explicitly revealed the results
        if user.is_staff or not poll.is_secret or poll.is_result_revealed:
            return super().get(request, *args, **kwargs)
        
        return Response(
            {"message": "Results for this poll are hidden until revealed by Admin."},
            status=status.HTTP_403_FORBIDDEN
        )