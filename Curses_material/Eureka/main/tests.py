from django.test import TestCase
from .models import Course, CoursePreview
from .models import Step
from .models import Lesson, ProgramModule, Practice
from django.test import RequestFactory
from django.urls import reverse
from .views import main_page
from django.core.exceptions import ObjectDoesNotExist
from .views import course_detail
from .models import Benefit, Course

class CourseModelTests(TestCase):
    def setUp(self):
        # Создаем предварительный курс
        self.preview = CoursePreview.objects.create(title="Предварительный курс", direction="IT", price=1000)
        # Создаем основной курс
        self.course = Course.objects.create(preview=self.preview, full_description="Описание полного курса")

    def test_string_representation(self):
        """Проверяем строку, возвращаемую методом __str__"""
        expected_str = str(self.preview)
        self.assertEqual(str(self.course), expected_str)

    def test_one_to_one_relationship(self):
        """Проверяем корректность one-to-one отношения"""
        self.assertEqual(self.course.preview, self.preview)

    def test_course_creation(self):
        """Проверяем создание основного курса"""
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first().preview, self.preview)


class BenefitModelTests(TestCase):
    def setUp(self):
        # Создаем учебный курс
        self.course = Course.objects.create(full_description="Тестовый курс")
        # Создаем преимущество
        self.benefit = Benefit.objects.create(course=self.course, title="Крутой бонус", description="Подробнее...")

    def test_benefit_attached_to_course(self):
        """Проверяем, что преимущество связано с курсом."""
        self.assertEqual(self.benefit.course, self.course)

    def test_benefit_icon_formatting(self):
        """Проверяем формат иконки (использование эмоджи)."""
        benefit = Benefit.objects.create(course=self.course, title="Ещë одно преимущество", icon="🎉")
        self.assertEqual(benefit.icon, "🎉")

from .models import NextSteps, Course

class NextStepsModelTests(TestCase):
    def setUp(self):
        # Создаем учебный курс
        self.course = Course.objects.create(full_description="Тестовый курс")
        # Создаем инструкцию дальнейших шагов
        self.next_step = NextSteps.objects.create(course=self.course, next_steps_text="Переходите к следующему этапу!")

    def test_next_steps_attached_to_course(self):
        """Проверяем, что инструкция дальнейших шагов привязана к курсу."""
        self.assertEqual(self.next_step.course, self.course)

from django.test import TestCase, RequestFactory
from .views import CourseDetail
from .models import Course, CoursePreview, ProgramModule, Lesson, Step


class CourseDetailViewTests(TestCase):
    def setUp(self):
        # Фиксируем учебные материалы
        self.preview = CoursePreview.objects.create(title="Тестовый курс", direction="IT", price=1000)
        self.course = Course.objects.create(preview=self.preview, full_description="Полный курс")
        self.module = ProgramModule.objects.create(course=self.course, title="Основной модуль", lessons_count=3)
        self.lesson = Lesson.objects.create(module=self.module, title="Первое занятие")
        self.step = Step.objects.create(lesson=self.lesson, title="Первый шаг", text="Детали...", order=1)
        # Фабрика запросов
        self.factory = RequestFactory()

    def test_course_detail_response_status(self):
        """Проверяем, что страница курса доступна."""
        request = self.factory.get(f'/course/{self.course.pk}/')
        view = CourseDetail.as_view()
        response = view(request, pk=self.course.pk)
        self.assertEqual(response.status_code, 200)

    def test_modules_and_lessons_in_context(self):
        """Проверяем, что модули и занятия попадают в контекст."""
        request = self.factory.get(f'/course/{self.course.pk}/')
        view = CourseDetail.as_view()
        response = view(request, pk=self.course.pk)
        context = response.context_data
        self.assertIn('lessons', context)
        self.assertIsNotNone(context['lessons'])
        self.assertGreater(len(context['lessons']), 0)

from django.test import TestCase, RequestFactory
from .views import main_page
from .models import CoursePreview

class MainPageViewTests(TestCase):
    def setUp(self):
        # Создаем тестовый курс предварительного просмотра
        CoursePreview.objects.create(title="Тестовый курс", direction="IT", price=1000)
        # Заводим фабрику запросов
        self.factory = RequestFactory()

    def test_main_page_status_code(self):
        """Проверяем статус HTTP для главной страницы."""
        request = self.factory.get('/')
        response = main_page(request)
        self.assertEqual(response.status_code, 200)






