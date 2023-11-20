from django import forms
from .models import Video


# These are your models form
class videoForm(forms.ModelForm):
    class Meta:
       model = Video
       
       fields = ['name','url','notes'] 
       
       
class SearchForm(forms.Form):
    search_term = forms.CharField()