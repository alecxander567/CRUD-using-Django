from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    users = User.objects.all()  # Fetch all users
    return render(request, "home.html", {"users": users})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")  # ✅ Success message
            return redirect('home')  # Redirect to home page after successful sign-up
        else:
            messages.error(request, "Password is too common please try again.")  # ❌ Error message

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# View to display all users
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})

# View to update a user
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('user_list')
    
    return render(request, 'update_user.html', {'user': user})

# View to delete a user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('user_list')