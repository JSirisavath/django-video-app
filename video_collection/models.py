from django.db import models

from urllib import parse

from django.core.exceptions import ValidationError
# A library that allows to parse. This will help parse the YT video ID for you

# Create your models here.


# What goes in a video class? 
# Name, YTVidURL, and optional Note


class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes= models.TextField(blank=True, null=True)
    # This is for the YT video id field
    # With unique value to be true for no replicate vid
    video_id = models.CharField(max_length=40, unique=True)
    
    
    # Override built in save method for model objects from django, and then add code we would want to run before the actual built in save function from django
    
    # The args and kwargs is django's save method arguments
    def save(self, *args, **kwargs):
        # Check if the video id from yt url starts with the base url (https://www.youtube.com/watch), if it doesn't, then raise a validation error
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Not a Youtube URL {self.url}')
        
        # extract the video id from users passed in object of the yt video url
        url_components = parse.urlparse(self.url)
        
        query_string = url_components.query # ID would be like 'v=4fsdfsa11d'
        
        # If the query string is not valid, then raise a validation error with invalid message and the url's payload
        if not query_string:
            raise ValidationError(f'Invalid YT Video URL {self.url}')
        
        # Parse qs basically converts the query string into a dictionary or object, which essentially separates the query  string'v=4fsdfsa11d' into -> {v: '4fsdfsa11d'}
        # Strict passing makes sure it is a valid string
        parameters = parse.parse_qs(query_string, strict_parsing=True)
        
        v_parameters_list = parameters.get('v') 
        # get value for key,'v', which is from the string query params of the yt vid url. We can do this method because it is a dictionary 
        # If the key has no 'V' it will return None, no key found e.g (abc: '324fdfd')
    
    
        # v_parameters_list is a python list
        if not v_parameters_list: # Check of none or empty list, then raise validationerror
            raise ValidationError(f'Invalid YT Video URL, missing valid key parameters {self.url}')
        
        # Else we will make video_id from the Video class to be the first of the list of v_parameters_list
        self.video_id = v_parameters_list[0] # String 
        
        # Original Save function from django that actually saves to the db needs to run after
        super().save(*args,**kwargs)
        
    # Formatted way to display the information strings
    # Truncate to the first 200 letters
    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}'