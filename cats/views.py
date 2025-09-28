from django.shortcuts import render
from django.http import Http404
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
