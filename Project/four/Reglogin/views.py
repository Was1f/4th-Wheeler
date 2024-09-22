from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


from django.contrib.auth.hashers import make_password
from django.db import connection  # To execute raw SQL queries

def signup(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get('email')
        password = request.POST.get("password")
        phn = request.POST.get("phone_number")
        nid = request.POST.get("nid_number")
        dob = request.POST.get("dob")  # Assuming DOB is part of your form

        # Print user input for debugging
        print(fname, lname, email, password, phn, nid, dob)

        # Hash the password before storing it in the database
        hashed_password = make_password(password)

        # Use raw SQL queries to insert data into `auth_user`
        with connection.cursor() as cursor:
            # Insert into `auth_user` table (Django default table)
            cursor.execute("""
                INSERT INTO auth_user (username, first_name, last_name, email, password, is_active, is_staff, is_superuser, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, [email, fname, lname, email, hashed_password, 1, 0, 0])

            # Get the ID of the last inserted row
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]

            # Insert into the custom `User` table
            cursor.execute("""
                INSERT INTO User (UserID, Password, FirstName, LastName, PhoneNo, Email, NID, IsOwner, DOB)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [user_id, hashed_password, fname, lname, phn, email, nid, 0, dob])  # Assuming IsOwner is 0 by default

        # Log the user in using the user ID from `auth_user`
        from django.contrib.auth import authenticate, login
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_profile")  # Redirect to the login page

    return render(request, "signup.html")  # Render the signup form






def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Try to find a user by their email and use their username for authentication
        try:
            user = User.objects.get(email=email)  # Find user by email
            username = user.username  # Get the username associated with this email
        except User.DoesNotExist:
            return render(request, "login.html", {'error': 'User with this email does not exist.'})
        
        # Authenticate using the username (since Django uses 'username' field for authentication)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and redirect to the user profile
            auth_login(request, user)
            return redirect('user_profile')
        else:
            # Invalid credentials; display an error message
            return render(request, "login.html", {'error': 'Invalid credentials'})
    
    return render(request, "login.html")
