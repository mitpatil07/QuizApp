from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Register
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, password=password)
        user.first_name = full_name
        user.email = email
        user.save()

        # Optional: Login after register
        login(request, user)
        return redirect('index')

    return render(request, 'accounts/register.html')
# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(
                request,
                "❌ Invalid username or password Register below."
            )
            return redirect('login')  # Redirect to refresh form with message

    return render(request, 'accounts/login.html')
# Logout
def logout_view(request):
    logout(request)
    return redirect('login')
