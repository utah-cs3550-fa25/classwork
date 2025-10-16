from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.http import require_GET
from django.core.exceptions import ValidationError
from .models import *

# Create your views here.
def index(request):
    cats = Cat.objects \
              .filter(health__spayed_neutered=True)

    return render(request, "index.html", {
        "cats": cats,
    })

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

def donate(request):
    errors = {}
    cat = None

    if request.method == "POST":
        cat = Cat()
        cat.health = HealthRecord()
        cat.name = request.POST.get("name", "[Unnamed]")
        cat.weight_lbs = request.POST.get("weight", "0.0")
        cat.spayed_neutered = "sn" in request.POST


        try:
            cat.full_clean()
        except ValidationError as e:
            errors = e.message_dict

        if not errors:
            cat.health.save()
            cat.save()
            return redirect("/cat/" + str(cat.id))

    return render(request, "donate.html", {
        "errors": errors,
        "cat": cat,
    })
