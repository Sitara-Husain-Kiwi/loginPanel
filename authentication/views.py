from django.contrib import messages, auth
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is alredy exists')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is alredy exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('signin')
                    user.save()
                    messages.success(request, 'You are now registerd and can login')
                    print(username)
                    print(email)
                    return redirect('home')
        else:
            messages.error(request,'Password do not match')
            return redirect('signup')
    
    else:  
        return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return render(request, 'authentication/index.html')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    else:
        return render(request, 'authentication/signin.html')

def signout(request):
    auth.logout(request)
    messages.success(request, "Logged out successfully!")
    return render(request, 'authentication/index.html')