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
            return redirect('user_list')  # Redirect to the user list after successful update
        return render(request, self.template_name, {'form': form})


class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list') 
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')  # Redirect to the user list after successful deletion





# Role CRUD Views
class RoleCreateView(View):
    template_name = 'forms/role_form.html'

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
    template_name = 'forms/role_form.html'

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
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return redirect('role_list')

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        return redirect('role_list')


class RoleListView(View):
    template_name = 'admin/role.html'

    def get(self, request):
        roles = Role.objects.all()
        return render(request, self.template_name, {'roles': roles})


# Category CRUD Views
class CategoryCreateView(View):
    template_name = 'forms/category_form.html'

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
            return redirect('category_list')
        return render(request, self.template_name, {'form': form})


class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category_list')
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category_list')


class CategoryListView(View):
    template_name = 'admin/category.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


# System Settings View (Assuming there's only one instance)
class System_Settings(LoginRequiredMixin,View):
    login_url = '/'
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

        # Save other fields
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

        system_settings.save()
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
        