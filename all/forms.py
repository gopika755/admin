from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import AdminUser,Profile

    
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if any(char.isdigit() for char in username):
            raise ValidationError("Username cannot contain numbers.")

        if Profile.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Profile.objects.filter(email=email).exists():
            raise ValidationError("Email already used.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")
        
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters.")

        if password1 and password2 and password1 != password2:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = Profile.objects.get(username=username)
            except Profile.DoesNotExist:
                raise ValidationError("Invalid username")

            if not check_password(password, user.password):
                raise ValidationError("Incorrect password")

            self.user = user

        return cleaned_data

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                admin = AdminUser.objects.get(username=username)
            except AdminUser.DoesNotExist:
                raise ValidationError("Admin does not exist.")

            if not check_password(password, admin.password):
                raise ValidationError("Incorrect password.")

            self.admin = admin

        return cleaned_data

class AddUserForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ["username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if any(char.isdigit() for char in username):
            raise ValidationError("Username cannot contain numbers.")

        if Profile.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")

        return username

    def clean(self):
        cleaned = super().clean()
        password1=self.cleaned_data.get('password')
        password2 = cleaned.get("confirm")
        
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if password1 != password2:
            self.add_error("confirm", "Passwords do not match")

        return cleaned

class EditUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if any(char.isdigit() for char in username):
            raise ValidationError("Username cannot contain numbers.")

        if Profile.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")

        return username
        
class AppUserForm(forms.ModelForm):
   class Meta:
        model = Profile
        fields = ["username", "email"]