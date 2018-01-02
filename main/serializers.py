from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Student, Course, Group, TypeForm, Answer

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for model Student
    """
    class Meta:
        model = Student
        fields = ('ldap',)

class TypeFormSerializer(serializers.ModelSerializer):
    """
    Serializer for model TypeForm
    """
    class Meta:
        model = TypeForm
        fields = ('name', 'form')

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

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for model Answer with ForeignKeys
    """
    id_course = serializers.CharField(source = 'group.course.id_course')
    label = serializers.CharField(source = 'group.course.label')
    delegate = serializers.CharField(source = 'group.delegate')
    commissionsDate = serializers.DateTimeField(source = 'group.course.commissionsDate')
    availableDate = serializers.DateTimeField(source = 'group.course.availableDate')
    typeForm = serializers.CharField(source = 'group.course.typeForm.name')
    group = serializers.IntegerField(source = 'group.number')

    class Meta:
        model = Answer
        fields = ('id_course', 'label', 'commissionsDate', 'availableDate', 'typeForm', 'delegate', 'group', 'answered', 'answer', 'submissionDate')
