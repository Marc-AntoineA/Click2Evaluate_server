from django.contrib import admin

# Register your models here.
from .models import Student, Course, Survey, TypeForm, Group, Question, QuestionWithAnswer

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Survey)
admin.site.register(TypeForm)
admin.site.register(Group)
admin.site.register(Question)
admin.site.register(QuestionWithAnswer)
