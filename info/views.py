from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import CollegeProfile, College
from datetime import date


def user_login(request):
    if request.user.is_authenticated:
        return redirect("college_profile")
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("college_profile")
        else:
            error = "Invalid ID or Password"
    return render(request, "index.html", {"error": error})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("college_profile")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def college_profile(request):
    profile, _ = CollegeProfile.objects.get_or_create(pk=1)
    colleges = College.objects.all().order_by("-id")

    college_data = []
    today = date.today()
    for c in colleges:
        diff_days = (c.expiry_date - today).days
        if diff_days < 0:
            status = "expired"
        elif diff_days <= 30:
            status = "expiring"
        else:
            status = "active"
        college_data.append({
            "obj": c,
            "status": status,
            "days_left": diff_days,
        })

    return render(request, "college.html", {
        "profile": profile,
        "colleges": college_data,
        "college_count": len(college_data),
    })


@login_required
def add_college(request):
    if request.method == "POST":
        College.objects.create(
            college_name=request.POST.get("college_name"),
            college_address=request.POST.get("college_address"),
            college_contact_number=request.POST.get("college_contact_number"),
            college_id=request.POST.get("college_id"),
            college_password=request.POST.get("college_password"),
            expiry_date=request.POST.get("expiry_date"),
            college_image=request.FILES.get("college_image"),
        )
    return redirect("college_profile")


@login_required
def edit_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    if request.method == "POST":
        college.college_name = request.POST.get("college_name")
        college.college_address = request.POST.get("college_address")
        college.college_contact_number = request.POST.get("college_contact_number")
        college.college_id = request.POST.get("college_id")
        college.college_password = request.POST.get("college_password")
        college.expiry_date = request.POST.get("expiry_date")
        if request.FILES.get("college_image"):
            college.college_image = request.FILES.get("college_image")
        college.save()
    return redirect("college_profile")


@login_required
def delete_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    college.delete()
    return redirect("college_profile")
