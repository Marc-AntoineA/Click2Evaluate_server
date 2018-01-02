from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Student, Course, Answer, TypeForm, Group, Question
from .serializers import StudentSerializer, CourseSerializer, AnswerSerializer, GroupSerializer, QuestionSerializer
from rest_framework.renderers import TemplateHTMLRenderer


# ListAPIView provides a generic view for read-only
# represent a collection of model instances
class StudentsList(ListAPIView):
    """
    List all students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AnswersStudentList(APIView):
    """
    List all 'courses' followed by a specific student
    """
    def get(self, request, pk, format = None):
        answers = Answer.objects.filter(student__ldap = pk)
        serializer = AnswerSerializer(answers, many = True)
        return Response(serializer.data)

class TypeForm(APIView):
    """
    Return all questions from a typeform corresponding to a name
    """
    def get(self, request, name, format = None):
        typeForm = Question.objects.filter(survey__name = name)
        serializer = QuestionSerializer(typeForm, many = True)
        return Response(serializer.data)
