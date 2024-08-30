from django.shortcuts import render,redirect
from django import views
from .forms import SignUpForm,LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.
# class Login(views.View):
#     def get(self, request, *args, **kwargs):
#         return render(request,'login.html')

#     def post(self, request, *args, **kwargs):
#         return render(request,'login.html')
        
# class Signup(views.View):
#     def get(self, request, *args, **kwargs):
#         return render(request,'signup.html')

#     def post(self, request, *args, **kwargs):
#         return render(request,'signup.html')
    

    

def LoginFormView(request):
    form = LoginForm(request.POST or None)

  

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dash")
            else:
               return HttpResponse("no")
        else:
            print("validate data")

    return render(request, "login.html", {"form": form})

def SignupFormView(request):
   
    

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
           

            

            return redirect("/")

        else:
           return HttpResponse("not worjing")
    else:
        form = SignUpForm()
        print("Asdhgbjsd")

    return render(request, "signup.html", {"form": form})

class Dashboard(views.View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')

    def post(self, request, *args, **kwargs):
        return render(request,'index.html')
        