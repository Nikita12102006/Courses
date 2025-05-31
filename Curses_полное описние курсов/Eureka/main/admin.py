from django.contrib import admin
from .models import (
    CoursePreview,
    Course,
    CourseImage,
    Teacher,
    ProgramModule,
    Benefit
)

# Register your models here.
admin.site.register(CoursePreview)
admin.site.register(Course)
admin.site.register(CourseImage)
admin.site.register(Teacher)
admin.site.register(ProgramModule)
admin.site.register(Benefit)