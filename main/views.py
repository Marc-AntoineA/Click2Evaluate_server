from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Student, Course, Survey, TypeForm, Group, Question, QuestionWithAnswer
from .serializers import StudentSerializer, CourseSerializer, SurveySerializer, GroupSerializer, QuestionSerializer, QuestionWithAnswerSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions

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

class TypeForm(APIView):
    """
    Return all questions from a typeform corresponding to a name
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, name, format = None):
        typeForm = Question.objects.filter(typeForm__name = name)
        serializer = QuestionSerializer(typeForm, many = True)
        return Response(serializer.data)

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
            return Response(serializer.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
