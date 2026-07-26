from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

from .models import Trip, Facility, EmergencyContact, Recommendation


def home(request):

    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user)
    else:
        trips = Trip.objects.none()

    search = request.GET.get("search", "").strip()

    if search:
        trips = trips.filter(
        Q(city__icontains=search) |
        Q(name__icontains=search)
    )

    total_trips = trips.count()
    total_budget = sum(trip.budget for trip in trips)
    total_members = sum(trip.members for trip in trips)
    total_days = sum(trip.days for trip in trips)
    total_facilities = Facility.objects.count()
    total_emergency = EmergencyContact.objects.count()
    total_recommendation = Recommendation.objects.count()

    context = {
    "trips": trips,
    "search": search,

    "total_trips": total_trips,
    "total_budget": total_budget,
    "total_members": total_members,
    "total_days": total_days,

    "total_facilities": total_facilities,
    "total_emergency": total_emergency,
    "total_recommendation": total_recommendation,
}

    return render(request, "home.html", context)

def trip(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == "POST":

        name = request.POST.get("name").strip()
        city = request.POST.get("city").strip()
        budget = int(request.POST.get("budget"))
        days = int(request.POST.get("days"))
        members = int(request.POST.get("members"))
        spent_amount = int(request.POST.get("spent_amount"))
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        status = request.POST.get("status")

        # Validation
        if not name:
            return render(request, "trip.html", {
                "error": "Name is required."
            })

        if not city:
            return render(request, "trip.html", {
                "error": "City is required."
            })

        if budget <= 0:
            return render(request, "trip.html", {
                "error": "Budget must be greater than 0."
            })

        if days <= 0:
            return render(request, "trip.html", {
                "error": "Days must be greater than 0."
            })

        if members <= 0:
            return render(request, "trip.html", {
                "error": "Members must be greater than 0."
            })

        # Date Validation

        if not start_date or not end_date:
            return render(request, "trip.html", {
                "error": "Please select both Start Date and End Date."
            })

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            return render(request, "trip.html", {
                "error": "End Date cannot be earlier than Start Date."
            })

        actual_days = (end - start).days + 1

        if actual_days != days:
            return render(request, "trip.html", {
                "error": f"According to selected dates, Days should be {actual_days}."
            })

        

        Trip.objects.create(
            user=request.user,
            name=name,
            city=city,
            budget=budget,
            days=days,
            members=members,
            status=status,
            start_date=start_date,
            end_date=end_date,
            spent_amount=spent_amount
        )

        budget_per_day = round(budget / days, 2)
        budget_per_person = round(budget / members, 2)
        remaining_budget = budget - spent_amount

        if remaining_budget > 0:
            budget_status = "✅ You are within your budget."

        elif remaining_budget == 0:
            budget_status = "⚠️ Your entire budget has been used."

        else:
            budget_status = f"❌ Budget Exceeded by ₹{abs(remaining_budget)}"

        if budget_per_person < 2000:
            recommendation = "🔴 Low Budget Trip"
            suggestion = "Use public transport and budget hotels."

        elif budget_per_person <= 5000:
            recommendation = "🟡 Medium Budget Trip"
            suggestion = "Good budget for hotels, food and local travel."

        else:
            recommendation = "🟢 Premium Budget Trip"
            suggestion = "Luxury hotels and private transport are affordable."

        return render(request, "trip.html", {
            "message": "Trip Saved Successfully!",
            "budget": budget,
            "budget_per_day": budget_per_day,
            "budget_per_person": budget_per_person,
            "recommendation": recommendation,
            "suggestion": suggestion,

            "spent_amount": spent_amount,
            "remaining_budget": remaining_budget,
            "budget_status": budget_status,
        })

    return render(request, "trip.html")


def edit_trip(request, id):

    trip = get_object_or_404(
        Trip,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        trip.name = request.POST.get("name")
        trip.city = request.POST.get("city")
        trip.budget = request.POST.get("budget")
        trip.days = request.POST.get("days")
        trip.members = request.POST.get("members")
        spent_amount = int(request.POST.get("spent_amount") or 0)

        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None

        status = request.POST.get("status")

        trip.save()

        return redirect("/")

    return render(request, "trip.html", {
        "trip": trip
    })


def delete_trip(request, id):

    trip = get_object_or_404(
        Trip,
        id=id,
        user=request.user
    )

    trip.delete()

    return redirect("/")


# -----------------------------
# Facility
# -----------------------------

def facility(request):

    city = request.GET.get("city")

    facility = None

    if city:
        facility = Facility.objects.filter(city__iexact=city).first()

    return render(request, "facility.html", {
        "facility": facility
    })


# -----------------------------
# Emergency Contact
# -----------------------------

def emergency(request):

    city = request.GET.get("city")

    contacts = None

    if city:
        contacts = EmergencyContact.objects.filter(city__iexact=city)

    return render(request, "emergency.html", {
        "contacts": contacts
    })


# -----------------------------
# Recommendation
# -----------------------------

def recommendation(request):

    city = request.GET.get("city")

    recommendation = None

    if city:
        recommendation = Recommendation.objects.filter(city__iexact=city).first()

    return render(request, "recommendation.html", {
        "recommendation": recommendation
    })


# -----------------------------
# Register
# -----------------------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists.")

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Registration Successful.")

            return redirect("/login/")

    return render(request, "register.html")


# -----------------------------
# Login
# -----------------------------

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        else:

            messages.error(request, "Invalid Username or Password.")

    return render(request, "login.html")


# -----------------------------
# Logout
# -----------------------------

def user_logout(request):

    logout(request)

    return redirect("/login/")