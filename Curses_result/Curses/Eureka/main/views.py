from django.shortcuts import render
from .models import CoursePreview
# Create your views here.


def main_page(request):
    return render(request, 'main/main_page.html', {'courses': CoursePreview.objects.all()})

def registration(request):
    return render(request, 'main/registration.html')

def authorization(request):
    return render(request, 'main/authorization.html')