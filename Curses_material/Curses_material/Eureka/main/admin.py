from django.contrib import admin
from .models import (
    CoursePreview,
    Course,
    ProgramModule,
    Benefit,
    Lesson,
    Step,
    CourseSummary,
    NextSteps
)

# Register your models here.
admin.site.register(CoursePreview)
admin.site.register(Course)
admin.site.register(ProgramModule)
admin.site.register(Benefit)
admin.site.register(Lesson)
admin.site.register(Step)
admin.site.register(CourseSummary)
admin.site.register(NextSteps)
