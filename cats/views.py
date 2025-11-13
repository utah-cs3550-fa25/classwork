from django.shortcuts import render, redirect
from django.http import Http404, FileResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .security import *
import time

# Create your views here.
def index(request):
    cats = Cat.objects.all()

    return render(request, "index.html", {
        "cats": cats,
    })

@user_passes_test(user_is_staff)
def view_cat(request, cat_id):
    try:
        cat = Cat.objects.get(id=cat_id)
    except Cat.DoesNotExist:
        raise Http404
    else:
        return render(request, "cat.html", {
            "cat": cat,
        })

def search(request):
    if request.method == "GET":
        age = int(request.GET.get("age"))
        age_is_min = request.GET.get("agetype", "min") == "min"

        q = Cat.objects.all()
        if age_is_min:
            q = q.filter(age__gte=age)
        else:
            q = q.filter(age__lte=age)
        return render(request, "cats.html", {
            "cats": q
        })

    return render(request, "search.html", {})

@user_passes_test(can_donate_cat)
def donate(request):
    if not can_donate_cat(request.user):
        raise PermissionDenied

    errors = {}
    cat = None

    if request.method == "POST":
        cat = Cat()
        cat.health = HealthRecord()
        cat.name = request.POST.get("name", "[Unnamed]")
        cat.weight_lbs = request.POST.get("weight", "0.0")
        cat.health.spayed_neutered = "sn" in request.POST


        if not errors:
            cat.health.save()
            cat.save()
            print("Redirecting?")
            return redirect("/cat/" + str(cat.id))

    return render(request, "donate.html", {
        "errors": errors,
        "cat": cat,
    })

def handle_login(request):
    errors = []
    
    if request.method == "GET":
        next = request.GET.get("next", "/")
    elif request.method == "POST":
        username = request.POST.get("user", "")
        password = request.POST.get("pass", "")
        next = request.POST.get("next", "/")

        user = authenticate(request, username=username, password=password)
        if not user:
            errors.append("Invalid username or password")

        if not errors:
            login(request, user)
            if next.startswith("/") and not next.startswith("//"):
                return redirect(next)
            else:
                return redirect(index)

    return render(request, "login.html", {
        "errors": errors,
        "next": next,
    })

def handle_logout(request):
    logout(request)
    return redirect("/")

def api_cats(request):
    cats = Cat.objects.all()
    return JsonResponse({
        "cats": [cat.id for cat in cats]
    })

def api_cat(request):
    id = request.GET["id"]
    cat = Cat.objects.get(id=id)
    return JsonResponse({
        "name": cat.name,
        "photo": cat.photo.url if cat.photo else None,
    })
