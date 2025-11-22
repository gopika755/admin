from django.shortcuts import render, redirect,get_object_or_404
from all.models import Profile
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, LoginForm,AdminLoginForm,AddUserForm,EditUserForm
from django.views.decorators.cache import never_cache


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.user 
            request.session['user_id'] = user.id
            return redirect("login_success")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def login_success(request):
    if "user_id" not in request.session:
        return redirect("login")

    return render(request, "login_success.html")

def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)

        if form.is_valid():
            admin = form.admin  
            request.session["admin_id"] = admin.id
            return redirect("admin_dashboard")
    else:
        form = AdminLoginForm()

    return render(request, "admin_login.html", {"form": form})


@never_cache
def admin_dashboard(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    users = Profile.objects.all()
    return render(request, "admin_dashboard.html", {"users": users})

def add_user(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = AddUserForm()

    return render(request, "add_user.html", {"form": form})
    
def edit_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)

    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = EditUserForm(instance=user)

    return render(request, "edit_user.html", {"form": form, "user": user})

def delete_user(request, user_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    user = get_object_or_404(Profile, id=user_id)
    user.delete()
    return redirect("admin_dashboard")

def admin_logout(request):
    logout(request)
    return redirect("admin_login") 