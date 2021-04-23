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
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse



def welcome(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request,"welcome.html")




class Login(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request,"login.html",{"login":AuthenticationForm(use_required_attribute=False)})
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

        else:
           messages.error(request,"Username or Password didnot match.")
           return redirect("login")

class UserSignUp(View):

    def get(self,request):
        context={
            "signup":CustomUserCreationForm(use_required_attribute=False),
            }
        return render(request,"signup.html",context)
    
    def post(self,request):
        fm=CustomUserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            uname = fm.cleaned_data.get("username")
            fullname = fm.cleaned_data.get("name").split()
            usr = CustomUser.objects.get(username=uname)
            usr.first_name=fullname[0]
            usr.last_name=fullname[len(fullname)-1]
            usr.email=uname
            usr.save()
            return redirect("login")
        else:
            messages.error(request,"Fields improperly filled, please try again")
            return redirect("signup")
        


def LogOut(request):
    logout(request)
    return redirect("login")


def UnactiveUser(request):
    return HttpResponse("User not active")



class Dashboard(View):

    def get(self,request):
        return render(request,"baseDashboard.html")



class Home(View):

    def get(self,request):
        hasCreatedBill = False
        bill = Challan.objects.filter(created_by=request.user)
        if bill.exists():
            hasCreatedBill = True
        form = ChallanForm(use_required_attribute=False)
        bills = Challan.objects.all()
        users = CustomUser.objects.all()
        myChallans = Challan.objects.filter(created_by=request.user)
        context={
            "form":form,
            "bills":bills,
            'profile':ProfileUpdateForm(instance=request.user),
            "users":users,
            "flag":hasCreatedBill,
            "totalUsers":len(users),
            "myChallan":len(myChallans),
            "totalChallan":len(bills)
        }
        return render(request,"index.html",context)
    
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
            return redirect("home")
    

class BillDetails(DeleteView):
    model = Challan
    template_name = "details.html"

class UpdateBill(UpdateView):
    model = Challan
    template_name = "update.html"
    fields = ["name","email",'place',"fine","license_number","vechile_number","vechile_type"]


class UpdateUser(View):

    def get(self,request,pk):
        usr = CustomUser.objects.get(id=pk)
        return render(request,"editProfile.html",{"editUser":usr})
    
    def post(self,request,pk):
        usr = CustomUser.objects.get(id=pk)
        fm = UserUpdateForm(data=request.POST,instance=usr)
        if fm.is_valid():
            fm.save()
            usr = CustomUser.objects.get(id=pk)
            fullname = request.POST.get("fullname").split()
            usr.first_name=fullname[0]
            usr.last_name=fullname[len(fullname)-1] 
            usr.save()
            return redirect("home")
        else:
            return redirect("home")
        

class UpdateUserPhoto(View):

    def post(self,request):
        fm = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if fm.is_valid():
            print("Valid")
            fm.save()
            return redirect("home")
        else:
            return redirect("home")

class DeleteBill(DeleteView):
    model = Challan
    success_url = reverse_lazy('home')
    template_name = "delete.html"



class DeleteUser(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

    



class ChangeUserStatus(View):
    def get(self,request,pk):
        user = CustomUser.objects.get(pk=pk)
        if user.active:
            user.active=False
            user.save()
            return JsonResponse(f"{user.first_name}, account has been disabled",safe=False)

        else:
            user.active=True
            user.save()
            return JsonResponse(f"{user.first_name}, account has been activated",safe=False)



   


   