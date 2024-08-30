from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'role': forms.Select(attrs={'placeholder': 'Select role'}),
            'is_active': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
        }
        
# Simple User Change Form
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'role': forms.Select(attrs={'placeholder': 'Select role'}),
            'is_active': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
        }
        
        
# Role Form
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter role name'}),
        }

# User Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }

# System Settings Form
class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = [
            'fav_icon', 'footer_logo', 'header_logo', 'website_name_english',
            'website_name_arabic', 'phone', 'email', 'address',
            'instagram', 'facebook', 'snapchat', 'linkedin', 'youtube'
        ]
        widgets = {
            'website_name_english': forms.TextInput(attrs={'placeholder': 'Website Name in English'}),
            'website_name_arabic': forms.TextInput(attrs={'placeholder': 'Website Name in Arabic'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter physical address', 'rows': 3}),
            'fav_icon': forms.TextInput(attrs={'placeholder': 'Favicon URL'}),
            'footer_logo': forms.TextInput(attrs={'placeholder': 'Footer logo URL'}),
            'header_logo': forms.TextInput(attrs={'placeholder': 'Header logo URL'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'Instagram URL'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'Facebook URL'}),
            'snapchat': forms.URLInput(attrs={'placeholder': 'Snapchat URL'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'LinkedIn URL'}),
            'youtube': forms.URLInput(attrs={'placeholder': 'YouTube URL'}),
        }
