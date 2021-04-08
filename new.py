from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Challan


class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(max_length=100,label=("Email"),label_suffix="")
    password1 = forms.CharField(max_length=100,label=("Password"),label_suffix="",widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=100,label=("Confirm Password"),label_suffix="",widget=forms.PasswordInput())
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={'type':"date"}))
    address =  forms.CharField(max_length=100,label=("Address"),label_suffix="")
    class Meta:
        model = CustomUser
        fields = ["username","address",'date_of_birth',"password1","password2"]


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email','date_of_birth','address']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['profile']
        

    

class ChallanForm(forms.ModelForm):
    class Meta:
        model=Challan
        fields=["name","email",'place',"fine","license_number","vechile_number","vechile_type"]
        widgets = {
              'name':forms.TextInput(attrs={"placeholder":"Name"}),
              'email':forms.EmailInput(attrs={"placeholder":"Email"}),
              'place':forms.TextInput(attrs={"placeholder":"Location"}),
               'fine':forms.TextInput(attrs={"placeholder":"Fine Charge"}),
              'license_number':forms.TextInput(attrs={"placeholder":"License Number"}),
              'vechile_number':forms.TextInput(attrs={"placeholder":"Vechile Number"}),
             }
        








from django.shortcuts import render,redirect
from .models import Challan,CustomUser
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.views import View
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import ChallanForm,CustomUserCreationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy



class Login(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request,"login.html")
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                print("YES")
            return redirect("home")
        else:
           msg = messages.error(request,"Username or Password didnot match.")
           return render(request,"login.html",{"msg":msg})

class UserSignUp(View):

    def get(self,request):
        context={
            "signup":CustomUserCreationForm(use_required_attribute=False),
            }
        return render(request,"signup.html",context)
    
    def post(self,request):
        fm=CustomUserCreationForm(request.POST)
        print(request.POST['username'],request.POST['date_of_birth'],request.POST['address'],request.POST['password1'],request.POST['password2'])
        
        if fm.is_valid():
            fm.save()
            return redirect("login")
        else:
            print(fm.error_messages)
            context={
            "signup":CustomUserCreationForm(use_required_attribute=False,data=request.POST),
            }
            return render(request,"signup.html",context)


def LogOut(request):
    logout(request)
    return redirect("login")



class Home(View):

    def get(self,request):
        form = ChallanForm(use_required_attribute=False)
        bills = Challan.objects.all()
        return render(request,"index.html",{"form":form,"bills":bills})
    
    def post(self,request):
        form = ChallanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            place = form.cleaned_data['place']
            form.save()
            bill = Challan.objects.get(name=name,place=place)
            bill.created_by=request.user
            bill.save()
            return redirect("home")
        else:
            bills = Challan.objects.all()
            form = ChallanForm(data=request.POST,use_required_attribute=False)
            return render(request,"index.html",{"form":form,"bills":bills})



class BillDetails(DeleteView):
    model = Challan
    template_name = "details.html"

class UpdateBill(UpdateView):
    model = Challan
    template_name = "update.html"
    fields = ["name","email",'place',"license_number","vechile_number","vechile_type"]

class UpdateUser(View):

    def get(self,request,pk):
        context={
            "form":UserUpdateForm
        }
        return render(request,"editProfile.html",context)


class UpdateUserPhoto(View):

    def get(self,request,pk):
        context={
            "form":ProfileUpdateForm
        }
        return render(request,"editProfile.html",context)
    

class DeleteBill(DeleteView):
    model = Challan
    success_url = reverse_lazy('home')
    template_name = "delete.html"


   


   