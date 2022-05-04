from django.shortcuts import render, redirect
from django.http import HttpResponse

## imported by self
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ITW_Project2 import settings
from django.core.mail import send_mail
# Create your views here.


def contact(request):
    return render(request ,"user/contact.html")


def services(request):
    return render(request ,"user/services.html")


def about(request):
    return render(request ,"user/about.html")




def home(request):
    #return HttpResponse("Hello world")
    return render(request, "user/index.html")


def signup(request):

    if request.method == "POST":
        print("yes")
        #username = request.POST.get('username')
        username = request.POST['username']
        print(username)
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(fname, lname, email, pass1, pass2)


        if User.objects.filter(username = username):
            messages.error(request, "Username already exists, try another")
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request, "Email already registered!")
            return redirect('signup')

    

        if pass1 != pass2:
            messages.error(request, "passwords did not matched")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('signup')

        


        Myuser = User.objects.create_user(username, email, pass1)
        Myuser.first_name = fname
        Myuser.last_name = lname

        Myuser.save()
        messages.success(request, "Your account has been created succesfully we have sent login credentials to the registered email. do not share with anyone.")


        ## Try writing email

        subject = "Welcome to Techstack login validation!"
        message = "Hello " + Myuser.first_name + "\n" + "Welcome to techstack \nThank you for your interest in techstack \nUsername : " + Myuser.username + "\nPassword : " + Myuser.password + "\nPlease do not share username or password with anyone"
        from_email = settings.EMAIL_HOST_USER
        to_list = [Myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)


        return redirect('signin')

    return render(request, "user/signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        Myuser1 = authenticate(username = username, password = pass1)

        if Myuser1 is not None:
            
            login(request, Myuser1)
            fname = Myuser1.first_name
            return render(request, "user/index.html", {'fname': fname})

        else:
            messages.error(request, "Username or password may be incorrect")
            return redirect('signin')

    return render(request, "user/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out succesfully")
    return redirect('home')

