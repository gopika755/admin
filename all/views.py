from django.shortcuts import render, redirect,get_object_or_404
from all.models import AdminUser,Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.hashers import check_password
from .forms import SignupForm, LoginForm,AdminLoginForm, AppUserForm
from django.contrib import messages
from django.utils import timezone

 


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def home(request):
    return render(request, 'home.html')


def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Profile.objects.get(username=username)
            if check_password(password, user.password):
                request.session["user_id"] = user.id
                user.last_login = timezone.now()
                user.save()
                return redirect("login_success")  # <<< CHANGE HERE

            else:
                error = "Wrong password"
        except Profile.DoesNotExist:
            error = "User does not exist"

    return render(request, "login.html", {"error": error})
def login_success(request):
    return render(request, "login_success.html")


def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                admin = AdminUser.objects.get(username=username)
                if check_password(password, admin.password):
                    request.session["admin_id"] = admin.id
                    return redirect("admin_dashboard")
                else:
                    messages.error(request, "Wrong password.")
            except AdminUser.DoesNotExist:
                messages.error(request, "Admin does not exist.")
    else:
        form = AdminLoginForm()

    return render(request, "admin_login.html", {"form": form})

def admin_dashboard(request):
    users = Profile.objects.all().order_by('last_login')  # most recent first
    return render(request, "admin_dashboard.html", {"users": users})

# ADD USER
def add_user(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            error = "Passwords do not match"
        else:
            Profile.objects.create(username=username, email=email, password=password)
            return redirect("admin_dashboard")

    return render(request, "add_user.html", {"error": error})


# EDIT USER
def edit_user(request, user_id):
    user = get_object_or_404(Profile,id=user_id)
    error = ""

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        return redirect("admin_dashboard")

    return render(request, "edit_user.html", {"user": user, "error": error})


# DELETE USER
def delete_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)
    user.delete()
    return redirect("admin_dashboard")


# LOGOUT
def admin_logout(request):
    logout(request)
    return redirect("login")  # your login page