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
from .permissions import IsAnswerFromStudent, AreCoursesFromStudent

# ListAPIView provides a generic view for read-only
# represent a collection of model instances

class SurveyStudentList(APIView):
    """
    List all 'courses' followed by a specific student
    """
    permission_classes = (AreCoursesFromStudent,)
    def get(self, request, pk, format = None):
        surveys = Survey.objects.filter(student__ldap = pk)
        self.check_object_permissions(request, surveys)
        serializer = SurveySerializer(surveys, many = True)
        return Response(serializer.data)

class TypeForm_questions(APIView):
    """
    Return all questions from a typeform corresponding to a name
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, name, format = None):
        typeForm = Question.objects.filter(typeForm__name = name).order_by('position');
        serializer = QuestionSerializer(typeForm, many = True)
        return Response(serializer.data)

class Answers(APIView):
    """
    Retrieve or update an answer instance.
    """
    permission_classes = (IsAnswerFromStudent,)
    def get_object(self, surveyId, questionId):
        print(surveyId, questionId)
        try:
            return QuestionWithAnswer.objects.get(survey__id = surveyId, question__id = questionId)
        except QuestionWithAnswer.DoesNotExist:
            raise Http404

    def get(self, request, surveyId, questionId):
        qwa = self.get_object(surveyId, questionId)
        self.check_object_permissions(request, qwa)
        serializer = QuestionWithAnswerSerializer(qwa)
        return Response(serializer.data)

    def put(self, request, surveyId, questionId):
        qwa = self.get_object(surveyId, questionId)
        self.check_object_permissions(request, qwa)
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
            self.check_object_permissions(request, qwa)
        except:
            query_qst = Question.objects.get(id = questionId)
            qwa = QuestionWithAnswer(survey = query_srv, question = query_qst)
            print(qwa)
            self.check_object_permissions(request, qwa)
            print(qwa)
            qwa.save()

        serializer = QuestionWithAnswerSerializer(qwa, data = request.data)
        if serializer.is_valid():
            serializer.save()
            query_srv.just_answered()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# Old functions unused and unreachable (no path in api.urls.py)
class ExistsStudent(APIView):
    """
    Return the student if possible
    USELESS
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, name, format = None):
        try:
            student = Student.objects.get(ldap = name)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Http404

class StudentsList(ListAPIView):
    """
    List all students USELESS
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
