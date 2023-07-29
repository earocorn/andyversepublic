from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class AndyVerseUser(models.Model):
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.CharField(max_length=50, unique=True, blank=False)
    uid = models.CharField(max_length=50, unique=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    profile_img = models.URLField(default='')
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created']
    

class MovieReview(models.Model):
    title = models.CharField(max_length=255)
    movie_id = models.IntegerField(default=0, blank=False, unique=True)
    poster_img = models.URLField(default='')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    written_review = models.TextField()
    review_summary = models.CharField(max_length=255, default="FUTURE")
    author_uid = models.CharField(max_length=50, default="", blank=False)
    author_username = models.CharField(max_length=50, default="", blank=False)
    spoiler_warning = models.BooleanField(default=True)
    release_date = models.DateField()
    date_time_reviewed = models.DateTimeField()
    favorited = models.BooleanField(default=False)
    future = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    is_movie = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['date_time_reviewed']

    def __str__(self):
        return self.title
    
class Message(models.Model):
    MESSAGE_TYPES = (
        ('suggestion', 'Suggestion'),
        ('contact', 'Contact'),
    )
    
    sender_name = models.CharField(max_length=100)
    sender_email = models.TextField(max_length=50, blank=True)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=20, default='unread')
    message = models.TextField(blank=False)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_sent']