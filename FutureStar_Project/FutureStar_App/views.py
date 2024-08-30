from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserForm, RoleForm, CategoryForm, SystemSettingsForm
from .models import User, Role, Category, SystemSettings


# Login View
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            print("Password entered by user:", password)  # Print the password entered in the form

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                print("Stored hashed password for the user:", user.password)  # Print the stored hashed password
                login(request, user)
                return redirect('home')  # Redirect to the homepage or dashboard
            else:
                print("Authentication failed.")  # Debugging output if authentication fails
                return redirect('error')
        return render(request, self.template_name, {'form': form})


# User CRUD Views
class UserCreateView(View):
    template_name = 'user_form.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list after successful creation
        return render(request, self.template_name, {'form': form})


class UserUpdateView(View):
    template_name = 'user_form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list after successful update
        return render(request, self.template_name, {'form': form})


class UserDeleteView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')  # Redirect to the user list after successful deletion


class UserListView(View):
    template_name = 'user_list.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})


# Role CRUD Views
class RoleCreateView(View):
    template_name = 'role_form.html'

    def get(self, request):
        form = RoleForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
        return render(request, self.template_name, {'form': form})


class RoleUpdateView(View):
    template_name = 'role_form.html'

    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(instance=role)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
        return render(request, self.template_name, {'form': form})


class RoleDeleteView(View):
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return redirect('role_list')


class RoleListView(View):
    template_name = 'role_list.html'

    def get(self, request):
        roles = Role.objects.all()
        return render(request, self.template_name, {'roles': roles})


# Category CRUD Views
class CategoryCreateView(View):
    template_name = 'category_form.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        return render(request, self.template_name, {'form': form})


class CategoryUpdateView(View):
    template_name = 'category_form.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        return render(request, self.template_name, {'form': form})


class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category_list')


class CategoryListView(View):
    template_name = 'category_list.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


# System Settings View (Assuming there's only one instance)
class SystemSettingsUpdateView(View):
    template_name = 'system_settings_form.html'

    def get(self, request):
        settings = SystemSettings.objects.first()
        form = SystemSettingsForm(instance=settings)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        settings = SystemSettings.objects.first()
        form = SystemSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('system_settings')
        return render(request, self.template_name, {'form': form})

# Error 404 html
class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "error.html")
    


        return render(request, "forms/base-input.html")
    
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')

    def post(self, request, *args, **kwargs):
        return render(request,'index.html')
        