from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from .models import *
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions

from django.template import loader

from .permissions import IsAnswerFromStudent, AreCoursesFromStudent, IsAdminOrReadOnly

def home(request):
    template = loader.get_template('api/home.html')
    return HttpResponse(template.render({}, request))


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
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, name):
        try:
            return TypeForm.objects.get(name = name)
        except TypeForm.DoesNotExist:
            raise Http404

    def get(self, request, name, format = None):
        typeForm = Question.objects.filter(typeForm__name = name).order_by('position')
        serializer = QuestionSerializer(typeForm, many = True)
        return Response(serializer.data)

    def post(self, request, name, format = None):
        self.check_permissions(request)

        Question.objects.filter(typeForm__name = name).delete()

        serializer = QuestionUpdateSerializer(data = request.data, many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TypeForm_general(APIView):
    """
    View to change a name and a summary corresonding to an actual typeForm
    """
    permission_classes = (IsAdminOrReadOnly, )

    def get(self, request, name, format = None):
        tf = TypeForm.objects.get(name = name)
        serializer = TypeFormSerializer(typeForm, many = False)
        return Response(serializer.data)

    def post(self, request, name, format = None):
        self.check_permissions(request)
        tf = TypeForm.objects.get(name = name)
        serializer = TypeFormSerializer(tf, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

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
        """ Put or update if already here """
        qwa = self.get_object(surveyId, questionId)
        self.check_object_permissions(request, qwa)
        serializer = QuestionWithAnswerSerializer(qwa, data = request.data)
        if serializer.is_valid():
            serializer.save()
            query_srv = Survey.objects.get(id = surveyId)
            query_srv.just_answered()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

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
