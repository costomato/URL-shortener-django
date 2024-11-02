from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Urls
import random, string


def home(request):
    return render(request, "home.html")


def generateSuffix(size=5):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=size))


def shorten(request):
    if request.method == "GET":
        return render(request, "error.html")

    suffix = request.POST.get("customSuffix")
    if not suffix:
        suffix = generateSuffix()
        # check if suffix exists. If yes, create new one.
        while Urls.objects.filter(suffix=suffix).exists():
            suffix = generateSuffix()
    elif (
        Urls.objects.filter(suffix=suffix).exists()
        or suffix == "admin"
        or suffix == "shorten"
        or not suffix.isalnum()
    ):
        return JsonResponse({"status": False, "res": "Please try another suffix"})
    elif len(suffix) > 30:
        return JsonResponse(
            {"status": False, "res": "Suffix length must not exceed 30 characters"}
        )

    url = request.POST.get("url")

    if "://" not in url:
        url = "http://" + url

    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return JsonResponse({"status": False, "res": "Invalid URL"})

    insert = Urls(suffix=suffix, url=url)
    insert.save()

    return JsonResponse({"status": True, "res": suffix, "url": url})


def visit(request, suffix):
    cursor = Urls.objects.filter(suffix=suffix)
    if not cursor.exists():
        return render(request, "error.html")

    url = cursor[0].url
    return HttpResponseRedirect(url)
