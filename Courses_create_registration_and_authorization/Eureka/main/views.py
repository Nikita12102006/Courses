from django.shortcuts import render
from .models import CoursePreview, Course
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.


def main_page(request):
    return render(request, 'main/main_page.html', {'courses': CoursePreview.objects.all()})

def registration(request):
    return render(request, 'main/registration.html')

def authorization(request):
    return render(request, 'main/authorization.html')

def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Http404("Такой курс не найден.")

    context = {
        'course': course
    }
    return render(request, 'main/course_detail.html', context)