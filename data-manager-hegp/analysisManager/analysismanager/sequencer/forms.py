from django import forms
#~ from .models import Calcu

DISPLAY_CHOICES = (
    ("locationbox", "Display Location"),
    ("displaybox", "Display Direction")
)

class MyForm(forms.Form):
  #  display_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DISPLAY_CHOICES)
    display_type = forms.ChoiceField(widget=forms.CheckboxInput, choices=DISPLAY_CHOICES)
#~ 
#~ 
#~ class UserForm(forms.ModelForm):
    #~ class Meta:
        #~ model = Calcu
        #~ fields = [
            #~ "n",
        #~ ]
