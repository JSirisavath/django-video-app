from django.shortcuts import render, redirect

from .forms import videoForm, SearchForm

# Temp messages from django
from django.contrib import messages

from .models import Video

from django.core.exceptions import ValidationError

from django.db import IntegrityError

from django.db.models.functions import Lower # Lowercase

# Create your views here.
def home (request):
    app_name = 'The Weeknd\'s mind' 
    return render(request, 'video_collection/home.html',{'app_name': app_name})


def add (request):
    if request.method == "POST": 
        # New Video form object values will be user's data request
        new_video_form = videoForm(request.POST)
        
        # Check if user's POST request is valid, by checking if the new_video_form is object is valid
        if new_video_form.is_valid():
            
            # Try and except handler catch if the save video form worked or not
            try:
                # Save to the db
                new_video_form.save()
                
                # Redirect to video list once saved
                return redirect('video_list')
                
                # Todo show success message or redirect to list of videos
            except ValidationError:
                messages.warning(request,'Invalid Youtube URL')
                
            # Duplicate videos
            except IntegrityError:
                messages.warning(request, 'Duplicate video, video was already added before')
        
        # Warning messages if form is not valid and passes all the other except functions
        messages.warning(request,'Please check data entered.')
        # Render and show the same page to them WITH their new added video information
        return render(request, 'video_collection/add.html',{'new_video_form':new_video_form})
        
        
    new_video_form = videoForm()
    
    return render(request, 'video_collection/add.html',
                  {'new_video_form': new_video_form})
    
    
def video_list(request):
    search_form = SearchForm(request.GET) # Build form from data users has sent to app
    
    if search_form.is_valid():
        # Searching the key word in the db
        search_term = search_form.cleaned_data['search_term'] # example: 'slowed'
    
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # Match all that contains that search word case insensitive
        
    else: # Form is nt filled in or this is te first time the users see's this page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))
        
    # # Grab all videos from the object
    # videos = Video.objects.all()
    
    # Render to video_list.html page
    return render(request, 'video_collection/video_list.html',
                  {'videos': videos, 'search_form': search_form})