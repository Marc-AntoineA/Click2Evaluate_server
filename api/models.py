from django.db import models
from django.utils import timezone
import datetime

# A course (= id + dates + typeform + ...) is followed that many students wo follow many courses
# An answer is made by a student for one course he follow


class TypeForm(models.Model):
    name = models.CharField(max_length = 100, unique = True) # e.g. "Classique"
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name

class Question(models.Model):
    typeForm = models.ForeignKey(TypeForm, on_delete = models.CASCADE)
    position = models.IntegerField()
    summary = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    label = models.CharField(max_length = 300)
    obligatory = models.BooleanField(default = False)
    type_question = models.CharField(max_length = 50)
    type_data = models.CharField(max_length = 400, blank = True)
    isSub = models.BooleanField(max_length = 50)
    parentsQuestionPosition = models.IntegerField(default = 0)
    parentsQuestionsValue = models.IntegerField(default = 0)

    def __str__(self):
        return self.label

    def all_answers(self):
        return [a.answer for a in QuestionWithAnswer.objects.filter(question = self)]
    
class Departement(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

    def nb_students(self):
        """
        Return the number of students from self
        """
        return len(Student.objects.filter(departement = self))

    def nb_surveys(self):
        """
        Return the number of surveys for students from self
        """
        return len(Survey.objects.filter(student__departement = self))

    def nb_answers(self):
        """
        Return the number of surveys answered
        """
        return len(Survey.objects.filter(student__departement = self, answered = True))

class Student(models.Model):
    ldap = models.CharField(max_length = 100, unique = True) # e.g. "andre.dupont@enpc.fr"
    mail = models.CharField(max_length = 100, unique = True)
    departement = models.ForeignKey(Departement, on_delete = models.CASCADE)
    def __str__(self):
        return self.ldap

class Course(models.Model):
    id_course = models.CharField(max_length = 10, unique=True)   # e.g. "TDLOG"
    label = models.CharField(max_length = 100) # e.g "Techniques de développement logiciel"
                                                    # group by group separated by ;
                                                    # (e.g. "andre.dupont@enpc.fr;louis.durand@enpc.fr"
    commissionsDate = models.DateTimeField()        # last day to submit a new answer
    availableDate = models.DateTimeField()          # first day to submnit a new answer (e.g. date of the exam)
    typeForm = models.ForeignKey(TypeForm, on_delete = models.CASCADE)  #which form is used for that course ?

    def __str__(self):
        return self.id_course + " : " + self.label

    def is_available(self):
        """
        Return true if a course is available (ie. timezone.now() >= availableDate)
        """
        return self.availableDate <= timezone.now()

    def all_available():
        """
        Return the list of all courses available today
        """
        courses = Course.objects.all()
        return [c for c in courses if c.is_available()]

    def nb_students(self):
        """
        Return the number of students who are in that course
        """
        groups = Group.objects.filter(course = self)
        return sum([g.nb_students() for g in groups])

    def nb_answers(self):
        """
        Return the number of answers for that course
        """
        return sum([g.nb_answers() for g in Group.objects.filter(course = self)])

class Group(models.Model):
    number = models.IntegerField(default = 0)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    delegate = models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.course) + " : " + str(self.number)

    def nb_students(self):
        """
        Return the number of students who are in that group
        """
        return len(Survey.objects.filter(group = self))

    def nb_answers(self):
        """
        Return the number of answers for self
        """
        return len(Survey.objects.filter(group = self, answered = True))

class Survey(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    answered = models.BooleanField(default = False) # True iff student answered course
    submissionDate = models.DateTimeField(default = timezone.now, blank = True)

    def __str__(self):
        return str(self.student) + " / " + str(self.group)

    def just_answered(self):
        print(self)
        self.answered = True
        self.submissionDate = timezone.now()
        self.save()

class QuestionWithAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 400, blank = True, default ="")

    def __str__(self):
        return str(self.question)
