
from django import forms
from  .models import ThreadModel


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)
    
class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)
    
    # image = forms.ImageField(required=False)
    
    
    # class Meta:
    #     model = ThreadModel
    #     fields = ['message','image']
        
        