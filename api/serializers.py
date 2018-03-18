from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Student, Course, Group, TypeForm, Survey, Question, QuestionWithAnswer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for model Question used to read typeForm
    """

    class Meta:
        model = Question
        fields = ('id','position', 'label', 'obligatory', 'type_question',
         'type_data', 'isSub', 'parentsQuestionPosition', 'parentsQuestionsValue')

class QuestionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for model Question used to post typeForm
    """
    typeForm = serializers.CharField(source = 'typeForm.name')

    class Meta:
        model = Question
        fields = ('position', 'label', 'obligatory', 'type_question',
         'type_data', 'isSub', 'parentsQuestionPosition', 'parentsQuestionsValue', 'typeForm')

    def create(self, validated_data):
        vd = validated_data
        print(vd)
        typeForm = None
        try:
            typeForm = TypeForm.objects.get(name = vd["typeForm"]["name"])
        except TypeForm.DoesNotExist:
            typeForm = TypeForm(name = vd["typeForm"]["name"])
            typeForm.save()

        question = Question(position = vd["position"], label = vd["label"],\
            obligatory = vd["obligatory"], type_question = vd["type_question"],\
            isSub = vd["isSub"], parentsQuestionPosition = vd["parentsQuestionPosition"],\
            parentsQuestionsValue = vd["parentsQuestionsValue"], typeForm = typeForm)
        question.save()
        return question

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

class TypeFormSerializer(serializers.ModelSerializer):
    """
    Serializer for model TF
    """

    class Meta:
        model = TypeForm
        fields = ('name', 'description')
