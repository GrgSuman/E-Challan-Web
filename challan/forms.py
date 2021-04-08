from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Challan


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100,label=(""),label_suffix="",widget=forms.TextInput(attrs={'placeholder':"Fullname","class":"username"}))
    username = forms.EmailField(max_length=100,label=(""),label_suffix="",widget=forms.EmailInput(attrs={'placeholder':"Email","class":"username"}))
    password1 = forms.CharField(max_length=100,label=(""),label_suffix="",widget=forms.PasswordInput(attrs={'placeholder':"Password","class":"username"}))
    password2 = forms.CharField(max_length=100,label=(""),label_suffix="",widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password","class":"username"}))
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={'type':"date","placeholder":"Date","class":"username"}),label="")
    address =  forms.CharField(max_length=100,label=(""),label_suffix="",widget=forms.TextInput(attrs={"placeholder":"Address","class":"username"}))
    class Meta:
        model = CustomUser
        fields = ['name',"username","address",'date_of_birth',"password1","password2"]




class UserUpdateForm(forms.ModelForm):
    username = forms.EmailField(max_length=100,label=("Email"),label_suffix="")
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={'type':"date"}))
    address =  forms.CharField(max_length=100,label=("Address"),label_suffix="")

    class Meta:
        model = CustomUser
        fields = ['username','date_of_birth','address']


class ProfileUpdateForm(forms.ModelForm):

    profile = forms.ImageField(label=(''),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    
    class Meta:
        model = CustomUser
        fields = ['profile']
        

    

class ChallanForm(forms.ModelForm):
    class Meta:
        model=Challan
        fields=["name","email",'place',"fine","license_number","vechile_number","vechile_type"]

        