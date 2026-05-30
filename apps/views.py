from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request , "html/home.html")


def luxa(request):
    return render(request , "html/luxa.html")

def collection_department(request):
    return render(request , "html/collection_department.html")