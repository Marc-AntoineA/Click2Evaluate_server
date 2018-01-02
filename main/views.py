from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Student, Course, Answer, TypeForm, Group
from .serializers import StudentSerializer, CourseSerializer, AnswerSerializer, TypeFormSerializer, GroupSerializer


# List all students or create a new one
class StudentsList(APIView):
    def get(self, request, format = None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many = True)
        return Response(serializer.data)

class AnswersStudentList(APIView):
    """
    List all 'courses' followed by a specific student
    """
    def get(self, request, pk, format = None):
        answers = Answer.objects.filter(student__ldap = pk)
        serializer = AnswerSerializer(answers, many = True)
        return Response(serializer.data)

class TypeFormDetail(APIView):
    """
    Return the Typeform corresponding to a name
    """
    def get_object(self, name):
        try:
            return TypeForm.objects.get(name = name)
        except:
            raise Http404

    def get(self, request, name, format = None):
        typeForm = self.get_object(name)
        serializer = TypeFormSerializer(typeForm)
        return Response(serializer.data)
