from django.db import models
from django.contrib.auth.models import User # For authentication
from django.utils import timezone
import datetime
import json
from django.core.validators import RegexValidator
from .csvToJson import convert

# A course (= id + dates + typeform + ...) is followed that many students wo follow many courses
# An answer is made by a student for one course he follow

class TypeForm(models.Model):
    name = models.CharField(max_length = 100, unique = True) # e.g. "Classique"
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name

    def export_head(self, anonymous = False):
        """
        Return the head
        """
        L = ["Cours", "Groupe", "Eleve", "Date"]
        if anonymous:
            L = ["Cours", "Groupe"]

        questions = Question.objects.filter(typeForm = self)
        print(questions)
        print(self)
        for q in questions:
            L.extend(q.export_head())
        return L


class Question(models.Model):
    typeForm = models.ForeignKey(TypeForm, on_delete = models.CASCADE)
    position = models.IntegerField()
    title = models.CharField(max_length = 100)
    label = models.CharField(max_length = 300)
    obligatory = models.BooleanField(default = False)
    type_question = models.CharField(max_length = 50,
        validators=[
            RegexValidator(
                regex='^(select|selectOne|inline|text|number)$',
                message='Veuillez choisir un type de question parmi select, selectOne, inline ou text',
            ),
        ])
    type_data = models.CharField(max_length = 400, blank = True)
    isSub = models.BooleanField(max_length = 50)
    parentsQuestionPosition = models.IntegerField(default = 0)
    parentsQuestionsValue = models.IntegerField(default = 0)

    def __str__(self):
        return self.label

    def all_answers(self):
        """
        Return a list containing all answers for one question (for every Course)
        """
        return [a.answer for a in QuestionWithAnswer.objects.filter(question = self)]

    def export_head(self):
        """
        Return an array containing the questions (not the answers)
        """
        if self.type_question == "select":
            return [self.label + " --> " +  x for x in self.type_data.split(";")]
        else:
            return [self.label]

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

    # 'user' used for authentification
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ldap = models.CharField(max_length = 100, unique = True) # e.g. "andre.dupont@enpc.fr"
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
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
        """
        Change the submissionDate and self.answered to True
        """
        self.answered = True
        self.submissionDate = timezone.now()
        self.save()

    def export(self, anonymous = False):
        """
        Export every answers from self
        """
        L = []
        if anonymous:
            L = [self.group.course.id_course, self.group.number]
        else:
            L = [self.group.course.id_course, self.group.number, self.student.ldap, self.submissionDate]

        if self.answered:
            answers = QuestionWithAnswer.objects.filter(survey = self).order_by('question__position')
            for a in answers:
                L.extend(a.export_answer())

            return L


class QuestionWithAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 400, blank = True, default ="")

    def __str__(self):
        return str(self.question)

    def export_answer(self):
        """
        Return an array containing the answer of the question =[booleans]> for 'select' and [X] for others
        """
        if self.question.type_question == "select":
            choices = self.answer.split(';')
            ans = []
            for c in choices:
                if c == "true":
                    ans.append("Oui")
                else:
                    ans.append('Non')
            return ans
        if self.question.type_question == "selectOne":
            return [self.question.type_data.split(";")[int(self.answer)]]
        return [self.answer]

def get_departement(s):
    """
    Return the firt word of s. E.g. "IMI - Finance" become "IMI" and "IMI-Finance" stay "IMI-Finance" (no space).
    If s is "" or only wone word --> return ""
    """
    try:
        return s.split(" ")[0]
    except:
        return ""

def create_database():
    convert('media/student_file')
    convert('media/course_file')

    with open("media/student_file.json") as json_data_students:
        with open("media/course_file.json") as json_data_courses:
            #% Delete files in databases
            Student.objects.all().delete()
            User.objects.exclude(username = "s2ip").delete()
            Course.objects.all().delete()
            Survey.objects.all().delete()
            Departement.objects.all().delete()
            QuestionWithAnswer.objects.all().delete()
            Group.objects.all().delete()
            Survey.objects.all().delete()

            d_students = json.load(json_data_students)
            d_courses = json.load(json_data_courses)

            # Add students and departements
            k = 0
            for line in d_students:
                #Add the departement if necessary

                query_dpt = ""
                try:
                    dpt = get_departement(line["DEPARTEMENT"])
                    query_dpt = Departement.objects.get(name = dpt)

                except Departement.DoesNotExist:
                    query_dpt = Departement(name = dpt)
                    query_dpt.save()
                except:
                    pass
                #Add the student if necessary (with mail, ldap and departement)

                ldap = line["LOGIN_LDAP"]
                first_name = line["PRENOM"]
                last_name = line["NOM"]
                email = line["MAIL"]
                if type(ldap) == type(" ") and type(first_name) == type(" ") \
                    and type(last_name) == type(" ") and type(email) == type(" "):
                    query_stdt = ""
                    try:
                        query_stdt = Student.objects.get(ldap = ldap)
                    except Student.DoesNotExist:
                        # password (here the last ldap) is not used in reality: it's useless.
                        user = User(username = ldap, email = email, password = "my password")
                        user.save()
                        query_stdt = Student(ldap = ldap, mail = email,
                            departement = query_dpt, user = user,
                            first_name = first_name, last_name = last_name)
                        query_stdt.save()

            #Add courses and groups from d_courses
            for line in d_courses :
                #Add the course if necessary
                id_course = line["id_course"]
                query_crse = ""
                try:
                    query_crse = Course.objects.get(id_course = id_course)

                except Course.DoesNotExist:
                    # Add the course
                    query_tF = TypeForm.objects.get(name = line['typeForm'])
                    query_crse = Course(id_course = id_course, label = line['label'],
                                        commissionsDate = line['commissionsDate'],
                                        availableDate = line['availableDate'],
                                        typeForm = query_tF)
                    query_crse.save()

                # Add the groups
                delegates_tab = line['delegates'].split(',')
                for k in range(len(delegates_tab)):
                    try:
                        query_grp = Group.objects.get(course__id_course = id_course, number = k)
                    except Group.DoesNotExist:
                        query_stdt = Student.objects.get(ldap = delegates_tab[k])
                        query_grp = Group(course = query_crse, delegate = query_stdt, number = k)
                        query_grp.save()

            # Link students and groups into surveys
            for line in d_students:
                try:
                    # Creating the survey
                    query_grp = Group.objects.get(course__id_course = line['CODE_MODULE'], number = line['SC_GROUPE'])
                    query_stdt = Student.objects.get(ldap = line['LOGIN_LDAP'])
                    query_srv = Survey(student = query_stdt, group = query_grp)
                    query_srv.save()

                except:
                    pass
