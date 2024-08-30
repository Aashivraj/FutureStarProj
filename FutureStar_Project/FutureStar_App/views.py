from django.shortcuts import render,redirect,get_object_or_404
from django import views
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin



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
        


class Table(views.View):
    def get(self, request, *args, **kwargs):
        return render(request,'table/datatable-basic-init.html')
    
    
############################################################## User CRUD ##############################################################
class UserListView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'table/datatable-basic-init.html', context)

class UserEditView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        form = UserChangeForm(instance=user)
        context = {
            'form': form,
            'user_obj': user,
        }
        return render(request, 'users/user_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-list')
        return render(request, 'users/user_form.html', {'form': form, 'user_obj': user})

class UserDeleteView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        context = {
            'user_obj': user,
        }
        return render(request, 'users/user_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user-list')

############################################################## Category CRUD ##############################################################
class CategoryListView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'categories/category_list.html', context)

class CategoryCreateView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        context = {
            'form': form,
        }
        return render(request, 'categories/category_form.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'categories/category_form.html', {'form': form})

class CategoryUpdateView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        context = {
            'form': form,
        }
        return render(request, 'categories/category_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'categories/category_form.html', {'form': form})

class CategoryDeleteView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        context = {
            'category': category,
        }
        return render(request, 'categories/category_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category-list')



############################################################## Role CRUD ##############################################################
class RoleListView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        context = {
            'roles': roles,
        }
        return render(request, 'roles/role_list.html', context)

class RoleCreateView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        form = RoleForm()
        context = {
            'form': form,
        }
        return render(request, 'roles/role_form.html', context)

    def post(self, request, *args, **kwargs):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role-list')
        return render(request, 'roles/role_form.html', {'form': form})

class RoleUpdateView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(instance=role)
        context = {
            'form': form,
        }
        return render(request, 'roles/role_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role-list')
        return render(request, 'roles/role_form.html', {'form': form})

class RoleDeleteView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        role = get_object_or_404(Role, pk=pk)
        context = {
            'role': role,
        }
        return render(request, 'roles/role_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return redirect('role-list')



############################################################## System Settings CRUD ##############################################################
class SystemSettingListView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        settings = SystemSettings.objects.all()
        context = {
            'system_settings': settings,
        }
        return render(request, 'settings/systemsetting_list.html', context)

class SystemSettingCreateView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        form = SystemSettingsForm()
        context = {
            'form': form,
        }
        return render(request, 'settings/systemsetting_form.html', context)

    def post(self, request, *args, **kwargs):
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('systemsetting-list')
        return render(request, 'settings/systemsetting_form.html', {'form': form})

class SystemSettingUpdateView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        setting = get_object_or_404(SystemSettings, pk=pk)
        form = SystemSettingsForm(instance=setting)
        context = {
            'form': form,
        }
        return render(request, 'settings/systemsetting_form.html', context)

    def post(self, request, pk, *args, **kwargs):
        setting = get_object_or_404(SystemSettings, pk=pk)
        form = SystemSettingsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('systemsetting-list')
        return render(request, 'settings/systemsetting_form.html', {'form': form})

class SystemSettingDeleteView(LoginRequiredMixin, views.View):
    def get(self, request, pk, *args, **kwargs):
        setting = get_object_or_404(SystemSettings, pk=pk)
        context = {
            'setting': setting,
        }
        return render(request, 'settings/systemsetting_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        setting = get_object_or_404(SystemSettings, pk=pk)
        setting.delete()
        return redirect('systemsetting-list')
