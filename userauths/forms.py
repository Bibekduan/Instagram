from userauths.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EditProfileForm(forms.ModelForm):
    image=forms.ImageField(required=True)
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your First-Name'}),required=True)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your Last-Name'}),required=True)
    bio=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter Your Bio '}),required=True)
    location=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter your location'}),required=True)
    # url=forms.URLField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter URL '}),required=True)


    class Meta:
        model=Profile
        fields=['image','first_name','last_name','bio','location']


class UserRegisterForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','class':'prompt srch_explore'}),max_length=500,required=True)
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email','class':'rompt srch_explore'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'prompt srch_explore'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'prompt srch_explore'}))

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']