from rest_framework import serializers

from andyverseapi.models import AndyVerseUser, MovieReview, Message


class AndyVerseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AndyVerseUser
        fields = ('__all__')
        
        
class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = ('__all__')
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')