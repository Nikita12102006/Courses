from django.test import TestCase
from .models import Benefit, Course, CoursePreview

class CourseModelTests(TestCase):
    def setUp(self):
        # Создаем предварительный курс
        self.preview = CoursePreview.objects.create(title="Предварительный курс", direction="IT", price=1000)
        # Создаем основной курс
        self.course = Course.objects.create(preview=self.preview, full_description="Описание полного курса")


class BenefitModelTests(TestCase):
    def setUp(self):
        # Создаем учебный курс
        self.course = Course.objects.create(full_description="Тестовый курс")
        # Создаем преимущество
        self.benefit = Benefit.objects.create(course=self.course, title="Крутой бонус", description="Подробнее...")


from .models import NextSteps, Course

class NextStepsModelTests(TestCase):
    def setUp(self):
        # Создаем учебный курс
        self.course = Course.objects.create(full_description="Тестовый курс")
        # Создаем инструкцию дальнейших шагов
        self.next_step = NextSteps.objects.create(course=self.course, next_steps_text="Переходите к следующему этапу!")



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



from django.test import TestCase, RequestFactory
from .views import main_page
from .models import CoursePreview

class MainPageViewTests(TestCase):
    def setUp(self):
        # Создаем тестовый курс предварительного просмотра
        CoursePreview.objects.create(title="Тестовый курс", direction="IT", price=1000)
        # Заводим фабрику запросов
        self.factory = RequestFactory()


