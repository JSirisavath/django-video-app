from django.db import models

# Create your models here.


# What goes in a video class? 
# Name, YTVidURL, and optional Note


class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes= models.TextField(blank=True, null=True)
    
    # Formatted way to display the information strings
    # Truncate to the first 200 letters
    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Notes: {self.notes[:200]}'