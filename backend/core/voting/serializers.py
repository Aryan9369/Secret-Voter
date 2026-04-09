from rest_framework import serializers
from .models import Poll, Option, Vote
from django.utils import timezone
from django.db.models import Count


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class PollCreateSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'start_time', 'end_time', 'is_secret', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        # Assign the logged-in admin as the creator
        poll = Poll.objects.create(**validated_data)
        
        for option in options_data:
            Option.objects.create(poll=poll, **option)
        return poll

class PollListSerializer(serializers.ModelSerializer):
    # We don't show counts here to maintain secrecy logic
    options = OptionSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'start_time', 'end_time', 'is_secret', 'options', 'is_active']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'option']

    def validate(self, data):
        poll = data['poll']
        user = self.context['request'].user

        # 1. Check if poll is active
        now = timezone.now()
        if now < poll.start_time:
            raise serializers.ValidationError("This poll has not started yet.")
        if now > poll.end_time:
            raise serializers.ValidationError("This poll has ended.")

        # 2. Check if the option belongs to the poll
        if data['option'].poll != poll:
            raise serializers.ValidationError("Invalid option for this poll.")

        # 3. Check if user already voted (Database unique constraint check)
        if Vote.objects.filter(user=user, poll=poll).exists():
            raise serializers.ValidationError("You have already voted in this poll.")

        return data



class PollResultSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'question', 'is_result_revealed', 'total_votes', 'options']

    def get_options(self, obj):
        # This will return options with their respective vote counts
        options = obj.options.annotate(vote_count=Count('vote'))
        return [
            {
                "id": opt.id,
                "option_text": opt.option_text,
                "vote_count": opt.vote_count
            } for opt in options
        ]

    def get_total_votes(self, obj):
        return obj.votes.count()