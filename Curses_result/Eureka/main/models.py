from django.db import models

class CoursePreview(models.Model):
    title = models.CharField('Название', max_length=200)
    direction = models.CharField('Направление', max_length=200)
    picture = models.ImageField('Изображение', upload_to='course_previews/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс превью'
        verbose_name_plural = 'Курсы превью'

class Course(models.Model):
    preview = models.OneToOneField(
        CoursePreview,
        on_delete=models.CASCADE,
        related_name='full_course',  # Добавляем unique related_name
        null=True,
        blank=True
    )
    full_description = models.TextField('Полное описание', blank=True)
    picture = models.ImageField('Изображение', upload_to='course_previews/', blank=True, null=True)

    def __str__(self):
        return self.preview.title if self.preview else f"Курс #{self.id}"

    class Meta:
        verbose_name = 'Полный курс'
        verbose_name_plural = 'Полные курсы'


class ProgramModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название модуля', max_length=200)
    description = models.TextField('Описание модуля', blank=True)
    lessons_count = models.PositiveSmallIntegerField('Количество уроков')

    def __str__(self):
        return f"Модуль: {self.title}"

    class Meta:
        verbose_name = 'Модуль программы'
        verbose_name_plural = 'Модули программы'

class Benefit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='benefits')
    title = models.CharField('Преимущества', max_length=200)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка', max_length=50, help_text="Используйте эмодзи")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Преимущества'
        verbose_name_plural = 'Преимущества'


class Lesson(models.Model):
    module = models.ForeignKey(ProgramModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название урока', max_length=200)
    description = models.TextField('Описание урока', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Step(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField('Название шага', max_length=200)
    text = models.TextField('Содержание шага')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Шаг урока'
        verbose_name_plural = 'Шаги урока'

    def __str__(self):
        return self.title


class CourseSummary(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name='summary',
    )
    summary_points = models.TextField('Итоги курса')

    def __str__(self):
        return f"Итоги курса: {self.course.preview.title}"

    class Meta:
        verbose_name = 'Итоги курса'
        verbose_name_plural = 'Итоги курсов'



class NextSteps(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name='next_steps',
    )
    next_steps_text = models.TextField('Что дальше?')

    def __str__(self):
        return f"Что дальше? {self.course.preview.title}"

    class Meta:
        verbose_name = 'Что дальше?'
        verbose_name_plural = 'Что дальше?'


