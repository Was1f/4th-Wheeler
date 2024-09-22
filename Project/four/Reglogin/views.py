from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from django.db import connection

def signup(request):
 if request.method == "POST":
  first_name = request.POST.get("first_name")
  last_name = request.POST.get("last_name")
  user_email = request.POST.get('email')
  user_password = request.POST.get("password")
  phone_number = request.POST.get("phone_number")
  nid_number = request.POST.get("nid_number")
  dob_value = request.POST.get("dob")

  print(first_name, last_name, user_email, user_password, phone_number, nid_number, dob_value)

  hashed_pw = make_password(user_password)

  with connection.cursor() as cursor:
   cursor.execute("""INSERT INTO auth_user (username, first_name, last_name, email, password, is_active, is_staff, is_superuser, date_joined)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())""", [user_email, first_name, last_name, user_email, hashed_pw, 1, 0, 0])

   cursor.execute("SELECT LAST_INSERT_ID()")
   user_id_value = cursor.fetchone()[0]

   cursor.execute("""INSERT INTO User (UserID, Password, FirstName, LastName, PhoneNo, Email, NID, IsOwner, DOB)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", [user_id_value, hashed_pw, first_name, last_name, phone_number, user_email, nid_number, 0, dob_value])

  user = authenticate(username=user_email, password=user_password)
  if user is not None:
   auth_login(request, user)
   return redirect("user_profile")

 return render(request, "signup.html")

def login(request):
 if request.method == "POST":
  user_email = request.POST.get("email")
  user_password = request.POST.get("password")

  try:
   user_found = User.objects.get(email=user_email)
   username_value = user_found.username
  except User.DoesNotExist:
   return render(request, "login.html", {'error': 'User with this email does not exist.'})

  user = authenticate(request, username=username_value, password=user_password)

  if user is not None:
   auth_login(request, user)
   return redirect('user_profile')
  else:
   return render(request, "login.html", {'error': 'Invalid credentials'})

 return render(request, "login.html")
