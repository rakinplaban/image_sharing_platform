import email
from email.mime import image
from tkinter.messagebox import RETRY
from tokenize import group
from django.core.mail import send_mail
from django.shortcuts import redirect
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404 
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from .forms import Img_form, Cat_form
from .decorators import allowed_users, admin_only
from .models import Like, User, Images, Categories,Role, Permission, Image_category

# from rest_framework.authtoken import TokenAuthentication
# Create your views here.


def index(request):
    # if request.method == "GET":
    #     search = request.GET['q']
    #     image_search = Images.objects.filter(title__contains = search)
    # c_form = cat_form()
    
    categories = Categories.objects.all()
    # img = 
    # checkw = Like.objects.filter(image = img,user = request.user).count()
    if request.method == "POST":
        # if request.user.is_authenticated:
        i_form = Img_form(request.POST, request.FILES)

        if i_form.is_valid():
            instance = i_form.save(commit = False)
            # images = Images(user_id = request.user.id , title = images.title, url = images.url, location = images.location, description= images.description)
            instance.user = request.user
            instance.save()
            i_form = Img_form()
            # return HttpResponseRedirect('')
    
    else:
        i_form = Img_form()
        # c_form = cat_form()
    # if request.method == "GET":
    #     search = request.GET['q']
    #     user_search = User.objects.filter(title__contains=search)

    images = Images.objects.all().order_by("-id")

    return render(request,"stock_app/index.html",{
        "i_form" : i_form,
        "categories" : categories,
        "images" : images,
        
        # "checkw" : checkw,
        # "c_form" : c_form,
        # "image_search" : image_search,
    })

@csrf_protect
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "stock_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "stock_app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_protect
def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        address = request.POST["address"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "stock_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.full_name = full_name
            user.phone = phone
            user.address = address
            user.save()

            group = Group.objects.get(name="publisher")
            user.groups.add(group)
        except IntegrityError:
            return render(request, "stock_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "stock_app/register.html")


def categories(request):
    c_form = Cat_form()
    if request.method == "POST":
        c_form = Cat_form(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request,"stock_app/cat.html",{
        "c_form" : c_form,
    })

def category(request,slug):
    items = Categories.objects.get(slug=slug)
    # photos = [val for val in Images.objects.all() if val in Categories.images.all()]
    photos = items.images.all().order_by('-id')
    return render(request,"stock_app/category.html",{
        "items" : items,
        "photos" : photos,
        "categories" : Categories.objects.all()
    })

def search(request):
    if request.method == "GET":
        search = request.GET['q']
        
        try:
            categories = Categories.objects.get(name__icontains=search)
            images = categories.images.all().order_by('-id')
        except ObjectDoesNotExist:
            return render(request,"stock_app/index.html",{
            "message" : "No Result Found!",
            "categories" : Categories.objects.all(),
        })
           
        return render(request,"stock_app/index.html",{
            "search" : search,
            "images" : images,
            "categories" : Categories.objects.all(),
        })


# def add_wishlist(request):
#     if request.method == "GET":
#         pid = request.GET["image_id"]
#         images = Images.objects.get(pk=pid)
#     data = {}
#     checkw = Like.objects.filter(image = images,user = request.user).count()
#     if checkw > 0:
#         data = {
#             'bool' : False
#         }
#     else:
#         like = Like.objects.create(image=images, user=request.user)
#         data = {'bool':True}

#     return JsonResponse(data)


# def remove_wishlist(request):
#     if request.method == "GET":
#         pid = request.GET["image_id"]
#         images = Images.objects.get(pk=pid)
#     data = {}
#     checkw = Like.objects.filter(image = images,user = request.user).count()
#     if checkw > 0:
#         data = {
#             'bool' : True
#         }
#     else:
#         like = Like.objects.get(user=request.user)
#         like.delete()
#         data = {'bool':False}

#     return JsonResponse(data)

def reset_password(request):

    if request.method == "POST":
        email_id = request.POST['email']
        try:
            email_id_check = User.objects.get(email=email_id)
            uidb64 = urlsafe_base64_encode(force_bytes(email_id_check.id))
            token = default_token_generator.make_token(email_id_check)
            subject = "Password Reset Application"
            message = f'''Hi there, your user id : {email_id_check}. Time to reset your password.\nGet ready url\n
            http://127.0.0.1:8000/reset/{uidb64}/{token}'''
            recipient_list = []
            recipient_list.append(email_id)
            send_mail(subject,message,from_email=None, recipient_list = recipient_list)
            return render(request,'stock_app/t_password_reset_done.html')
             
        except User.DoesNotExist:
            return render(request,'stock_app/t_password_reset.html',{
                "message" : "Looks like your email isn't registered!"
            })
     
    
    return render(request,'stock_app/t_password_reset.html')



def reset_password_confirm(request,uidb64,token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user_ob = User.objects.get(id=uid)
    validlink = default_token_generator.check_token(user_ob, token)
    if validlink:
        if request.method == "POST":
            password = request.POST["password"]
            confirmation = request.POST["conform-password"]
            if password != confirmation:
                return render(request, "stock_app/t_password_reset_confirm.html", {
                    "message": "Passwords must match."
                })
            else:
               
                user_ob.set_password(password)
                user_ob.save()
                return render(request,'stock_app/t_password_reset_complete.html')
    else:
        return render(request,'stock_app/t_password_reset_confirm.html',{
        "message" : "url not valid!"
    })
    return render(request,'stock_app/t_password_reset_confirm.html',{
        'validlink' : validlink,
        'uidb64' : uidb64,
        'uid' : uid,
        'user_ob' : user_ob,
        'token' : token
    })


def shared_img(requests,id):
    photo = Images.objects.get(pk=id)
    images = Images.objects.all().order_by("-id")
    
    # try: 
    #     like_img = Like.objects.get(image=photo)
    #     flag = True
    #     count = 0
    #     return render(requests,"stock_app/share.html",{
    #         "photo" : photo,
    #         "images" : images,
    #         "like_img" : like_img,
    #         "flag" : flag,
    #         "count" : count,
    #         # "like_usr" : like_usr,
    #     })
    # # like_img = Like.objects.select_related('photo').values_list('image_id')
    # # like_usr = Like.objects.select_related('user').values_list('user_id')
    # except Like.DoesNotExist:
    #     flag = False
    #     count = 0
        # like = like_img.filter(user=requests.user)
    return render(requests,"stock_app/share.html",{
        "photo" : photo,
        "images" : images,
        # "like_img" : like_img,
        # "flag" : flag,
        # "count" : count,
        # "like_usr" : like_usr,
    })

def add_image(request):
    if request.method == "POST":
        # if request.user.is_authenticated:
        i_form = Img_form(request.POST, request.FILES)

        if i_form.is_valid():
            instance = i_form.save(commit = False)
            # images = Images(user_id = request.user.id , title = images.title, url = images.url, location = images.location, description= images.description)
            instance.user = request.user
            instance.save()
            i_form = Img_form()
            
    else:
        i_form = Img_form()

    images = Images.objects.all().order_by("-id")
    return render(request,"stock_app/add.html",{
        "i_form" : i_form,
        "categories" : categories,
        "images" : images,
    })


def delete_img(request,id):
    image = Images.objects.get(pk=id).delete()
    return redirect('index')

def update_img(request,id):
    image = Images.objects.get(id=id)
    images = Images.objects.all().order_by('-id')
    form = Img_form(request.POST or None, request.FILES or None, instance=image)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request,"stock_app/update.html",{
        "images" : images,
        "form" : form,
    })


def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('image_id'))
        image = get_object_or_404(Images, id= id)
        if image.liked.filter(id=request.user.id).exists():
            image.liked.remove(request.user)
            image.like_count -= 1
            result = image.like_count
            image.save()
        else:
            image.liked.add(request.user)
            image.like_count += 1
            result = image.like_count
            image.save()

        return JsonResponse({"result":result, })

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_panel(request):
    return render(request,"stock_app/adminpanel.html")


