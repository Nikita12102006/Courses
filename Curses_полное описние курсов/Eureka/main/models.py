from django.db import models

class CoursePreview(models.Model):
    title = models.CharField('Название', max_length=200)
    direction = models.CharField('Направление', max_length=200)
    picture = models.ImageField('Изображение', upload_to='course_previews/', blank=True, null=True)
    price = models.IntegerField('Цена')

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
    duration = models.CharField('Длительность', max_length=50, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.preview.title if self.preview else f"Курс #{self.id}"

    class Meta:
        verbose_name = 'Полный курс'
        verbose_name_plural = 'Полные курсы'

class CourseImage(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField('Изображение', upload_to='course_images/')
    is_main = models.BooleanField('Главное изображение', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение курса'
        verbose_name_plural = 'Изображения курсов'

    def __str__(self):
        return f"Изображение {self.id} для {self.course}"

class Teacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teacher')
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    description = models.TextField('Характеристика преподавателя', blank=True)
    photo = models.ImageField('Фото', upload_to='instructors/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

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
