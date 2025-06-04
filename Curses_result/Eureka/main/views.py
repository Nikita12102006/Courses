from django.shortcuts import render
from .models import CoursePreview, Course
from django.http import Http404
from django.views.generic.detail import DetailView
from .models import Course, Lesson, Step
from django.shortcuts import get_object_or_404
# Create your views here.


def main_page(request):
    return render(request, 'main/main_page.html', {'courses': CoursePreview.objects.all()})

def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Http404("Такой курс не найден.")

    context = {
        'course': course
    }
    return render(request, 'main/course_detail.html', context)


class CourseDetail(DetailView):
    model = Course
    template_name = 'main/detail.html'  # Убедитесь, что путь к шаблону корректен
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем модули текущего курса
        modules = self.object.modules.all()

        # Формируем список уроков и шагов для каждого модуля
        lessons_list = []
        for module in modules:
            lessons = module.lessons.all()  # получаем все уроки конкретного модуля
            steps_by_lessons = []  # храним тут шаги всех уроков

            for lesson in lessons:
                steps = lesson.steps.order_by('order')  # сортируем шаги по порядку
                steps_by_lessons.append({
                    'lesson': lesson,
                    'steps': steps
                })

            lessons_list.append({
                'module': module,
                'lessons': steps_by_lessons
            })

        context['lessons'] = lessons_list
        return context