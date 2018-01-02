from django.db import models
from django.utils import timezone

# A course (= id + dates + typeform + ...) is followed that many students wo follow many courses
# An answer is made by a student for one course he follow

class TypeForm(models.Model):
    name = models.CharField(max_length = 100) # e.g. "Classique"
    form = models.TextField()# the questions and for each question many informations (JSON string)

    def __str__(self):
        return self.name

class Student(models.Model):
    ldap = models.CharField(max_length = 100) # e.g. "andre.dupont@enpc.fr"

    def __str__(self):
        return self.ldap

class Course(models.Model):
    id_course = models.CharField(max_length = 10)   # e.g. "TDLOG"
    label = models.CharField(max_length = 100) # e.g "Techniques de développement logiciel"
                                                    # group by group separated by ;
                                                    # (e.g. "andre.dupont@enpc.fr;louis.durand@enpc.fr"
    commissionsDate = models.DateTimeField()        # last day to submit a new answer
    availableDate = models.DateTimeField()          # first day to submnit a new answer (e.g. date of the exam)
    typeForm = models.ForeignKey(TypeForm, on_delete = models.CASCADE)  #which form is used for that course ?

    def __str__(self):
        return self.id_course


class Group(models.Model):
    number = models.IntegerField(default = 0)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    delegate = models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.course) + " : " + str(self.number)


class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    answered = models.BooleanField(default = False) # True iff student answered course
    answer = models.TextField(default = "", blank = True) # all the answers in a JSON string
    submissionDate = models.DateTimeField(default = timezone.now(), blank = True)

    def __str__(self):
        return str(self.student) + " / " + str(self.group)
