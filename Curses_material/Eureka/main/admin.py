from django.contrib import admin
from .models import (
    CoursePreview,
    Course,
    CourseImage,
    Teacher,
    ProgramModule,
    Benefit,
    Lesson,
    Step,
    CourseSummary,
    Practice,
    NextSteps
)

# Register your models here.
admin.site.register(CoursePreview)
admin.site.register(Course)
admin.site.register(CourseImage)
admin.site.register(Teacher)
admin.site.register(ProgramModule)
admin.site.register(Benefit)
admin.site.register(Lesson)
admin.site.register(Step)
admin.site.register(CourseSummary)
admin.site.register(Practice)
admin.site.register(NextSteps)
