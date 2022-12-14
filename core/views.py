from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from psutil import users 
from .models import Profile, Post

# Create your views here.
@login_required(login_url = 'signin')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {"posts": posts})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        missing = []
        fields = {"username": username, "email": email, "password": password, "password2": password2}
        for field in fields:
            if not fields[field]: 
                missing.append(field)
        if missing:
            messages.info(request, "Missing " + ", ".join(missing))
            return redirect('signup')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user: 
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url = 'signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url = 'signin')
def settings(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        Profile.objects.filter(user=request.user).update(bio=bio)
        messages.info(request, 'Bio changed')
        return redirect('settings')
    else:
        curr_bio = Profile.objects.filter(user=request.user).first().bio
        return render(request, 'settings.html', {'bio': curr_bio})

@login_required(login_url = 'signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        body = request.POST['body']
        new_post = Post.objects.create(user=user, body=body)
        new_post.save()
        messages.info(request, 'You posted')
        return redirect('/')
    else:
        return redirect('/')