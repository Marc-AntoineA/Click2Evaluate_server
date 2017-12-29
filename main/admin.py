from django.contrib import admin

# Register your models here.
from .models import Student, Course, Answer, TypeForm, Group

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Answer)
admin.site.register(TypeForm)
admin.site.register(Group)
