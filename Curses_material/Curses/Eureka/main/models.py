from django.db import models

# Create your models here.
class CoursePreview(models.Model):
    title = models.CharField('Название', max_length=200)
    direction = models.CharField('Направление', max_length=200)
    picture = models.ImageField('Изображение', upload_to='course_previews/', blank=True, null=True)
    price = models.IntegerField('Цена')

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Курс превью'
        verbose_name_plural = 'Курсы превью'