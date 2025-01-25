from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('news', 'News'),
        ('outdoors_nature', 'Outdoors & Nature'),
        ('business_industrial', 'Business & Industrial'),
        ('computers_electronics', 'Computers & Electronics'),
        ('health_fitness', 'Health & Fitness'),
        ('arts_entertainment', 'Arts & Entertainment'),
        ('education', 'Education'),
        ('sports', 'Sports'),
        ('food_drink', 'Food & Drink'),
        ('fashion', 'Fashion'),
    ]  # Add more as necessary

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Article_Title = models.CharField(max_length=200)
    image = models.ImageField("Image", blank=True, null=True, upload_to="images/")
    Article_Text = models.TextField()
    Article_Category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tech')  # Added category
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.Article_Title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#lets seee    

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField()

#comment section

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # Correct model name here
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"