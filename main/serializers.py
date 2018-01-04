from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Student, Course, Group, TypeForm, Survey, Question, QuestionWithAnswer

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for model Question
    """
    class Meta:
        model = Question
        fields = ('id','position', 'summary', 'label', 'obligatory', 'type_question',
         'type_data', 'isSub', 'parentsQuestionPosition', 'parentsquestionsValue')

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for model Student
    """
    departement = serializers.CharField(source = 'departement.name')
    class Meta:
        model = Student
        fields = ('ldap','mail', 'departement')

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for model Course
    """
    typeForm_name = serializers.CharField(source='typeForm.name')
    class Meta:
        model = Course
        fields = ('id_course', 'label', 'commissionsDate', 'availableDate', 'typeForm_name')

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for model Group
    """
    course_id = serializers.CharField(source = 'course.id_course')
    class Meta:
        model = Group
        fields = ('course_id', 'number', 'delegate')

class SurveySerializer(serializers.ModelSerializer):
    """
    Serializer for model Survey with ForeignKeys
    """
    id_course = serializers.CharField(source = 'group.course.id_course')
    label = serializers.CharField(source = 'group.course.label')
    delegate = serializers.CharField(source = 'group.delegate')
    commissionsDate = serializers.DateTimeField(source = 'group.course.commissionsDate')
    availableDate = serializers.DateTimeField(source = 'group.course.availableDate')
    typeForm = serializers.CharField(source = 'group.course.typeForm.name')
    group = serializers.IntegerField(source = 'group.number')

    class Meta:
        model = Survey
        fields = ('id', 'id_course', 'label', 'commissionsDate', 'availableDate', 'typeForm', 'delegate', 'group', 'answered', 'submissionDate')

class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for model QuestionWithAnswer
    """

    class Meta:
        model= QuestionWithAnswer
        fields = ('answer',)
