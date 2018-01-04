from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from .models import Student, Course, Survey, TypeForm, Group, Question, QuestionWithAnswer, Departement
from .serializers import StudentSerializer, CourseSerializer, SurveySerializer, GroupSerializer, QuestionSerializer, QuestionWithAnswerSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions
import json

# ListAPIView provides a generic view for read-only
# represent a collection of model instances
class StudentsList(ListAPIView):
    """
    List all students
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SurveyStudentList(APIView):
    """
    List all 'courses' followed by a specific student
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk, format = None):
        surveys = Survey.objects.filter(student__ldap = pk)
        serializer = SurveySerializer(surveys, many = True)
        return Response(serializer.data)

class TypeForm_questions(APIView):
    """
    Return all questions from a typeform corresponding to a name
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, name, format = None):
        typeForm = Question.objects.filter(typeForm__name = name)
        serializer = QuestionSerializer(typeForm, many = True)
        return Response(serializer.data)

class ExistsStudent(APIView):
    """
    Return the student if possible
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, name, format = None):
        try:
            student = Student.objects.get(ldap = name)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Http404

class Answers(APIView):
    """
    Retrieve or update an answer instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, surveyId, questionId):
        print(surveyId, questionId)
        try:
            return QuestionWithAnswer.objects.get(survey__id = surveyId, question__id = questionId)
        except QuestionWithAnswer.DoesNotExist:
            raise Http404

    def get(self, request, surveyId, questionId):
        qwa = self.get_object(surveyId, questionId)
        serializer = QuestionWithAnswerSerializer(qwa)
        return Response(serializer.data)

    def put(self, request, surveyId, questionId):
        qwa = self.get_object(surveyId, questionId)
        serializer = QuestionWithAnswerSerializer(qwa, data = request.data)
        if serializer.is_valid():
            serializer.save()
            query_srv = Survey.objects.get(id = surveyId)
            query_srv.just_answered()
            return Response(serializer.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, surveyId, questionId):
        qwa = None
        query_srv = Survey.objects.get(id = surveyId)
        try:
            qwa = self.get_object(surveyId, questionId)
        except:

            query_qst = Question.objects.get(id = questionId)
            qwa = QuestionWithAnswer(survey = query_srv, question = query_qst)
            qwa.save()

        serializer = QuestionWithAnswerSerializer(qwa, data = request.data)
        if serializer.is_valid():
            serializer.save()
            query_srv.just_answered()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


def update_database(request, format = None):
    with open("data/data_students.json") as json_data_students:
        with open("data/data_courses.json") as json_data_courses:

            d_students = json.load(json_data_students)
            d_courses = json.load(json_data_courses)

            # Add students and departements
            k = 0
            for line in d_students:
                #Add the departement if necessary
                dpt = line["DEPARTEMENT"]
                query_dpt = ""
                try:
                    query_dpt = Departement.objects.get(name = dpt)

                except Departement.DoesNotExist:
                    query_dpt = Departement(name = dpt)
                    query_dpt.save()

                #Add the student if necessary (with mail, ldap and departement)
                ldap = line["LOGIN_LDAP"]
                if type(ldap) == type(" "):
                    query_stdt = ""
                    try:
                        query_stdt = Student.objects.get(ldap = ldap)
                    except Student.DoesNotExist:
                        query_stdt = Student(ldap = ldap, mail = line["MAIL"], departement = query_dpt)
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
                delegates_tab = line['delegates'].split(';')
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
