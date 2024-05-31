from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.conf import settings
import os



# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,"account/login.html",{
                "error":"username or password is uncorrect!"
            })

    return render(request,"account/login.html")

def register_page(request):

    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return render(request,"account/register.html",{
                    "error":"this username already exists!",
                    "username":username,
                    "email":email,
                    "name":name
                    })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request,"account/register.html",{
                        "error":"this E-mail already exists!",
                        "username":username,
                        "email":email,
                        "name":name })
                else:
                    user = User.objects.create_user(username=username,email=email,first_name=name,password=password)
                    user.save()
                    login(request, user)
                    return redirect("home")
        else:
            return render(request,"account/register.html",{
                "error":"passwords not matching!" ,
                "username":username,
                "email":email,
                "name":name 
                })

    return render(request,"account/register.html")


def profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect("login") 
    user= get_object_or_404(CustomUser, user__username=username)
    mybio = user.user_bio
    mytags = user.user_tags
    is_owner = False


    if request.method == "POST":
        mybio = request.POST.get('biography')
        mytags = request.POST.get('tags')

        user = CustomUser.objects.get(user=request.user)

        # Profil bilgilerini güncelle
        user.user_bio = mybio
        user.user_tags = mytags
        user.save()
        

    if user.user == request.user:
        is_owner = True

    context = {
        'user': user,
        'mybio': user.user_bio,
        'mytags': user.user_tags,
        'is_owner': is_owner,

    }


    return render(request, "account/profile.html", context)




def setting_page(request):
    if not request.user.is_authenticated:
        return redirect("login") 

    return render(request,"account/settings.html")


def update_profile_picture(request):
    if not request.user.is_authenticated:
        return redirect("login") 
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        profile_picture = request.FILES['profile_picture']
        custom_user = CustomUser.objects.get(user=request.user)
        custom_user.profile_picture = profile_picture
        custom_user.save()
        return redirect('profile', request.user.username)

    return redirect('profile', request.user.username)


def delete_profile_picture(request):
    if not request.user.is_authenticated:
        return redirect("login") 
    if request.method == 'POST':
        custom_user = CustomUser.objects.get(user=request.user)
        if custom_user.profile_picture != 'default_pp.jpg':
            os.remove(os.path.join(settings.MEDIA_ROOT, custom_user.profile_picture.name))
            custom_user.profile_picture = 'default_pp.jpg'
            custom_user.save()
        return redirect('profile', request.user.username)

    return redirect('profile', request.user.username)


def logging_out(request):
    logout(request)
    return redirect('login')

