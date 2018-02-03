from django.shortcuts import render
from django.http import HttpResponse, Http404
from api.models import *
from django.template import loader
from django.core.files.storage import FileSystemStorage
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
from django.conf import settings
import csv
import io
import tarfile

from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    template = loader.get_template('controlPanel/home.html')
    return HttpResponse(template.render({}, request))


def general(request):
    template = loader.get_template('controlPanel/generalView.html')
    data = {
        "nb_students": len(Student.objects.all()),
        "nb_courses": len(Course.objects.all()),
        "nb_answers": len(Survey.objects.filter(answered = True)),
        "rate_answer": round(100.*len(Survey.objects.filter(answered = True))/len(Survey.objects.all()), 1),
    }
    return HttpResponse(template.render(data, request))


def project(request):
    template = loader.get_template('controlPanel/project.html')
    return HttpResponse(template.render({}, request))


def importDb(request):
    if request.method == 'POST' and request.FILES['course_file'] and request.FILES['student_file']:
        course_file = request.FILES['course_file']
        student_file = request.FILES['student_file']

        fs = FileSystemStorage()
        fs.delete("student_file.csv")
        fs.save("student_file.csv", student_file)
        fs.delete("course_file.csv")
        fs.save("course_file.csv", course_file)
        create_database()

    template = loader.get_template('controlPanel/import.html')
    return HttpResponse(template.render({}, request))

def export_zip_file(List_courses, anonymous = False):
    """
    Download zip file with all courses in list_courses
    e.g. list_courses = ['TDLOG', 'O2IMI']
    """
    prefix = "media/"
    suffix = ".csv"
    if anonymous:
        suffix = "_anonyme.csv"

    for id_course in List_courses:
        id_course.strip()
        print(id_course)
        course = Course.objects.get(id_course = id_course)
        tF = course.typeForm
        surveys = Survey.objects.filter(group__course__id_course = id_course, answered = True).order_by("submissionDate")

        answers_data = [tF.export_head(anonymous)]
        for s in surveys:
            answers_data.append(s.export(anonymous))

        with open(prefix + id_course + suffix, 'w') as answers_file:
            writer = csv.writer(answers_file)
            writer.writerows(answers_data)

    # Create the response and the tar file
    response = HttpResponse(content_type='application/x-gzip')
    name_tar = "export_reponses"
    response['Content-Disposition'] = 'attachment; filename= Export_reponses'  + suffix + '.tar.gz'
    tarred = tarfile.open(fileobj=response, mode='w:gz')

    for id_course in List_courses:
        tarred.add(prefix + id_course + suffix)
    tarred.close()

    return response

def exportDb(request):

    # List of all available courses
    courses = Course.objects.all()
    item_list = [{
        "label": c.label,
        "commissionsDate": c.commissionsDate,
        "id": c.id_course,
        "rate_answer": round(c.nb_answers()/float(c.nb_students())*100, 1),
    } for c in courses if c.nb_students() > 0]

    data = {
        "item_list": item_list,
    }
    template = loader.get_template('controlPanel/export.html')

    if "courses" in request.GET:
        data_requested = request.GET['courses']
        print(data_requested)
        list_courses = data_requested.split(",")
        print(list_courses)
        anonymous = "anonymous" in request.GET

        return export_zip_file(list_courses, anonymous)
    else:
        return HttpResponse(template.render(data, request))

def typeFormView(request, id_q = None):
    typeForm_list = TypeForm.objects.all()
    data = {}

    if id_q != None:
        current = TypeForm.objects.get(id = id_q)
        questions = Question.objects.filter(typeForm = current).order_by('position')
        for q in questions:
            q.data = q.type_data.split(";")
        #question
        main_questions = [q for q in questions if not(q.isSub)]
        for q in main_questions:
            q.sub_questions = list(Question.objects.filter(isSub = True, parentsQuestionPosition = q.position))
            q.had_sub_questions = len(q.sub_questions) > 0

        data = {
            "current_id": current.id,
            "current_name": current.name,
            "current_description": current.description,
            "typeForm_list": typeForm_list,
            "main_questions": main_questions,
        }
    else:
        data = {
            "typeForm_list": typeForm_list,
        }

    template = loader.get_template('controlPanel/survey.html')
    return HttpResponse(template.render(data, request))


def specific(request, type_request, format = None):
    item_list = []

    if type_request == "module":
        courses = Course.all_available()
        item_list = [{
            "label": c.label,
            "nb_students": c.nb_students(),
            "rate_answer": round(c.nb_answers()/float(c.nb_students())*100, 1),
        } for c in courses if c.nb_students() > 0]


    elif type_request == "departement":
        departements = Departement.objects.all()
        item_list = [{
            "label": d.name,
            "nb_students": d.nb_students(),
            "rate_answer": round(d.nb_answers()/float(d.nb_surveys())*100, 1)
        } for d in departements if d.nb_surveys() > 0]

    else:
        raise Http404

    # Useless
    f = (lambda x: x["label"])

    reverse = False

    item_list.sort(key = f, reverse = reverse)
    data = {
        "item_list": item_list,
        "type_request": type_request,
    }

    template = loader.get_template('controlPanel/specific.html')
    return HttpResponse(template.render(data, request))


def question_home(request):

    questions = Question.objects.all()
    item_list = [{
        "id_q": q.id,
        "label": q.label,
        "typeForm": q.typeForm
    } for q in questions]

    data = {
        "item_list": item_list,
    }

    template = loader.get_template('controlPanel/questionsAll.html')
    return HttpResponse(template.render(data, request))


def question(request, id_q):
    template = loader.get_template('controlPanel/question.html')
    question = Question.objects.get(id = id_q)

    answers = question.all_answers()
    #answers = ["Oui", "Oui", "Oui", "Non","Oui", "Peut-être"]

    frq_answers = {}
    max_frq = 0

    if question.type_question == "selectOne" or question.type_question == "select":
        list_answers = question.type_data.split(';')

        for x in list_answers:
            frq_answers[x] = 0

        for a in answers:
            label_answer = list_answers[int(a)]
            print(label_answer)
            if label_answer in frq_answers:
                frq_answers[label_answer] += 1
            else:
                frq_answers[label_answer] = 1

            max_frq = max(frq_answers[label_answer], max_frq)


    typeForm = question.typeForm

    print(frq_answers)
    rate_answer = 0
    if len(QuestionWithAnswer.objects.filter(question = question)) > 0:
        rate_answer = round(100.*len(QuestionWithAnswer.objects.filter(question = question, survey__answered = True))
            /len(Survey.objects.filter(group__course__typeForm = typeForm)), 1)

    data = {
        "question_label": question.label,
        "question_type": question.type_question,
        "nb_answers": len(QuestionWithAnswer.objects.filter(question = question, survey__answered = True)),
        "rate_answer": rate_answer,
        "frq_answers": frq_answers,
        "answers": answers,
        "max_frq": max_frq,
    }
    return HttpResponse(template.render(data, request))
