from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Poll(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_polls")
    question = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Secret Mode: Results hidden until manual reveal
    is_secret = models.BooleanField(default=True)
    is_result_revealed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validation: Start time cannot be after end time
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        
    def __str__(self):
        return self.question

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.poll.question[:20]} - {self.option_text}"

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Crucial: One user can only vote once per poll
        unique_together = ('user', 'poll')

    def __str__(self):
        return f"User {self.user.id} voted on {self.poll.id}"