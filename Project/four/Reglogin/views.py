from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

def signup(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        #username=request.POST.get("Username:")
        email = request.POST.get('email')
        password = request.POST.get("password")
        phn = request.POST.get("phone_number")
        nid = request.POST.get("nid_number")

        # Print user input for debugging
        print(fname, lname, email, password, phn, nid)

        #Use email as the username
        #username = email

        # Create the user
        my_user = User.objects.create_user(
            username=email,  # Email as username
            first_name=fname,
            last_name=lname,
            email=email,
            password=password  # Password will be hashed automatically
        )

        # Log the user in and redirect
        login(request)
        return redirect("login")  # Redirect to the login page

    return render(request, "signup.html")  # Render the signup form





def login(request): 
    if request.method=="POST":
        email=request.POST.get("email:")
        pass_w=request.POST.get("password:")
        print(email,pass_w)
        user= authenticate(request,email=email,password=pass_w)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return redirect("login")
        
       
    return render(request,"login.html")

def temp_home(request):    
    return render(request,"Temp_home.html")