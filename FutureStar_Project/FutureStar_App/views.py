import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserForm, RoleForm, CategoryForm, SystemSettingsForm
from .models import User, Role, Category, SystemSettings
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Login View

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        
        if not form.is_valid():
            # Add a message if the form is not valid due to blank fields
            if not form.cleaned_data.get('username'):
                messages.error(request, 'Username cannot be blank.')
            if not form.cleaned_data.get('password'):
                messages.error(request, 'Password cannot be blank.')
            if form.cleaned_data.get('username') and form.cleaned_data.get('password'):
                messages.error(request, 'Please correct the errors below.')
            
            return render(request, self.template_name, {'form': form})

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
        
        return render(request, self.template_name, {'form': form})

#User Crud
class UserListView(View):
    template_name = 'admin/user.html'

    def get(self, request):
        User = get_user_model()  # Get the custom user model
        users = User.objects.all()
        roles = Role.objects.all()
        return render(request, self.template_name, {'users': users, 'roles': roles})


class UserUpdateView(View):
    template_name = 'forms/user_form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} was successfully updated.')
            return redirect('user_list')  # Redirect to the user list after successful update
        else:
            messages.error(request, 'There was an error updating the user.')
        return render(request, self.template_name, {'form': form})


class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, f'User {user.username} was successfully deleted.')
        return redirect('user_list')  # Redirect to the user list after successful deletion

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, f'User {user.username} was successfully deleted.')
        return redirect('user_list')  # Redirect to the user list after successful deletion



# Role CRUD Views
class RoleCreateView(View):
    def get(self, request):
        form = RoleForm()
        return render(request, 'forms/role_form.html', {'form': form})

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            # Check for existing role with the same name
            name = form.cleaned_data.get('name')
            if Role.objects.filter(name=name).exists():
                messages.error(request, 'A role with this name already exists.')
                return redirect('role_list')  # Redirect back to role_list with an error message
            form.save()
            messages.success(request, 'Role was successfully created.')
            return redirect('role_list')
        else:
            messages.error(request, 'There was an error creating the role. Please ensure all fields are filled out correctly.')
        return redirect('role_list') 
class RoleUpdateView(View):
    template_name = 'forms/role_form.html'

    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(instance=role)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            # Check for existing role with the same name but different pk
            name = form.cleaned_data.get('name')
            if Role.objects.filter(name=name).exclude(pk=pk).exists():
                messages.error(request, 'A role with this name already exists.')
                return render(request, self.template_name, {'form': form})
            form.save()
            messages.success(request, 'Role was successfully updated.')
            return redirect('role_list')
        else:
            messages.error(request, 'There was an error updating the role. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})


class RoleDeleteView(View):
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        messages.success(request, 'Role was successfully deleted.')
        return redirect('role_list')

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        messages.success(request, 'Role was successfully deleted.')
        return redirect('role_list')

class RoleListView(View):
    template_name = 'admin/role.html'

    def get(self, request):
        roles = Role.objects.all()
        return render(request, self.template_name, {'roles': roles})


# Category CRUD Views

class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'forms/category_form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Check for existing category with the same name
            name = form.cleaned_data.get('name')
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'A category with this name already exists.')
                return redirect('category_list')  # Redirect back to category_list with an error message
            form.save()
            messages.success(request, 'Category was successfully created.')
            return redirect('category_list')
        else:
            messages.error(request, 'There was an error creating the category. Please ensure all fields are filled out correctly.')
        return redirect('category_list')

class CategoryUpdateView(View):
    template_name = 'forms/category_form.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was successfully updated.')
            return redirect('category_list')
        else:
            messages.error(request, 'There was an error updating the category. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})


class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category was successfully deleted.')
        return redirect('category_list')

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category was successfully deleted.')
        return redirect('category_list')

class CategoryListView(View):
    template_name = 'admin/category.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


# System Settings View (Assuming there's only one instance)
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')

class System_Settings(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()  # Fetch the first record
        return render(request, 'admin/system_settings.html', {
            'system_settings': system_settings,
            'MEDIA_URL': settings.MEDIA_URL,  # Pass MEDIA_URL to the template
        })

    def post(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()
        if not system_settings:
            system_settings = SystemSettings()

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'System_Settings'))

        # Validation flags
        errors = []

        # Handle fav_icon
        if 'fav_icon' in request.FILES:
            if system_settings.fav_icon:
                old_fav_icon_path = os.path.join(settings.MEDIA_ROOT, system_settings.fav_icon)
                if os.path.isfile(old_fav_icon_path):
                    os.remove(old_fav_icon_path)
            fav_icon_file = request.FILES['fav_icon']
            fav_icon_filename = 'favicon.jpg'
            fs.save(fav_icon_filename, fav_icon_file)
            system_settings.fav_icon = os.path.join('System_Settings', fav_icon_filename)
        else:
            errors.append("Fav Icon is required.")

        # Handle footer_logo
        if 'footer_logo' in request.FILES:
            if system_settings.footer_logo:
                old_footer_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.footer_logo)
                if os.path.isfile(old_footer_logo_path):
                    os.remove(old_footer_logo_path)
            footer_logo_file = request.FILES['footer_logo']
            footer_logo_filename = 'footer_logo.jpg'
            fs.save(footer_logo_filename, footer_logo_file)
            system_settings.footer_logo = os.path.join('System_Settings', footer_logo_filename)
        else:
            errors.append("Footer Logo is required.")

        # Handle header_logo
        if 'header_logo' in request.FILES:
            if system_settings.header_logo:
                old_header_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.header_logo)
                if os.path.isfile(old_header_logo_path):
                    os.remove(old_header_logo_path)
            header_logo_file = request.FILES['header_logo']
            header_logo_filename = 'header_logo.jpg'
            fs.save(header_logo_filename, header_logo_file)
            system_settings.header_logo = os.path.join('System_Settings', header_logo_filename)
        else:
            errors.append("Header Logo is required.")

        # Save other fields with validation
        system_settings.website_name_english = request.POST.get('website_name_english')
        system_settings.website_name_arabic = request.POST.get('website_name_arabic')
        system_settings.phone = request.POST.get('phone')
        system_settings.email = request.POST.get('email')
        system_settings.address = request.POST.get('address')
        system_settings.instagram = request.POST.get('instagram')
        system_settings.facebook = request.POST.get('facebook')
        system_settings.snapchat = request.POST.get('snapchat')
        system_settings.linkedin = request.POST.get('linkedin')
        system_settings.youtube = request.POST.get('youtube')

        # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(system_settings.email)
        except ValidationError:
            errors.append("Invalid email format.")

        # Validate phone number format
        if not PHONE_REGEX.match(system_settings.phone):
            errors.append("Invalid phone number format.")

        # Validate social media URLs
        if not system_settings.instagram:
            errors.append("Instagram URL is required.")
        if not system_settings.facebook:
            errors.append("Facebook URL is required.")
        if not system_settings.snapchat:
            errors.append("Snapchat URL is required.")
        if not system_settings.linkedin:
            errors.append("LinkedIn URL is required.")
        if not system_settings.youtube:
            errors.append("YouTube URL is required.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'admin/system_settings.html', {
                'system_settings': system_settings,
                'MEDIA_URL': settings.MEDIA_URL,  # Pass MEDIA_URL to the template
            })

        system_settings.save()
        messages.success(request, "System settings updated successfully.")
        return redirect('home')

# Error 404 html
class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "error.html")
    

    
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')

    def post(self, request, *args, **kwargs):
        return render(request,'index.html')
        