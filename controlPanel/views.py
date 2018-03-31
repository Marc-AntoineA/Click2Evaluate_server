from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from api.models import *
from django.template import loader
from django.core.files.storage import FileSystemStorage
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
from django.conf import settings
import csv
import io
import tarfile
import controlPanel.models
import pandas as pd
from Click2Evaluate_server.settings import *

from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@login_required(login_url='/s2ip/connecter')
def home(request):
    template = loader.get_template('controlPanel/home.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/s2ip/connecter')
def general(request):
    template = loader.get_template('controlPanel/generalView.html')
    data = {
        "nb_students": len(Student.objects.all()),
        "nb_courses": len(Course.objects.all()),
        "nb_answers": len(Survey.objects.filter(answered = True)),
        "rate_answer": round(100.*len(Survey.objects.filter(answered = True))/len(Survey.objects.all()), 1),
    }
    return HttpResponse(template.render(data, request))

@login_required(login_url='/s2ip/connecter')
def project(request):
    template = loader.get_template('controlPanel/project.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/s2ip/connecter')
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

def convertCSVToXLSX(name, anonymous):
    df = pd.read_csv(name + ".csv", sep=",")
    col_freeze = 5
    if anonymous:
        col_freeze = 3
    df.to_excel(name + ".xlsx",'Resultats', freeze_panes=(1, col_freeze), index=False)

def export_zip_file(List_courses, anonymous = False):
    """
    Download zip file with all courses in list_courses
    e.g. list_courses = ['TDLOG', 'O2IMI']
    """
    prefix = "media/"
    suffix = ""
    if anonymous:
        suffix = "_anonyme"

    for id_course in List_courses:
        id_course.strip()
        course = Course.objects.get(id_course = id_course)
        tF = course.typeForm
        surveys = Survey.objects.filter(group__course__id_course = id_course, answered = True).order_by("submissionDate")

        answers_data = [tF.export_head(anonymous)]
        for s in surveys:
            answers_data.append(s.export(anonymous))

        with open(prefix + id_course + suffix + ".csv", 'w') as answers_file:
            writer = csv.writer(answers_file)
            writer.writerows(answers_data)


    with open("temp.zip", 'wb') as temp:
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)

        for id_course in List_courses:
            convertCSVToXLSX(prefix + id_course + suffix, anonymous)
            archive.write(prefix + id_course + suffix + ".xlsx")
        archive.close()

        wrapper = open("temp.zip", "rb")
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename= Export_reponses'  + suffix + '.zip'
        return response

@login_required(login_url='/s2ip/connecter')
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

@login_required(login_url='/s2ip/connecter')
def typeFormView(request, id_q = None):
    typeForm_list = TypeForm.objects.all()
    data = {}
    current = None
    if id_q == None:

        if len(typeForm_list) > 0:
            id_q = list(typeForm_list)[0].id
        else:
            tf = TypeForm(name = "Votre nouveau questionaire", description = "")
            tf.save()
            id_q = tf.id
            typeForm_list = TypeForm.objects.all()

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
    print(data)

    template = loader.get_template('controlPanel/survey.html')
    return HttpResponse(template.render(data, request))

@login_required(login_url='/s2ip/connecter')
def specific(request, type_request, format = None):
    item_list = []

    if type_request == "module":
        courses = Course.all_available()
        item_list = [{
            "label": c.label,
            "nb_students": c.nb_students(),
            "rate_answer": round(c.nb_answers()/float(c.nb_students())*100, 1),
            "departement": c.departement,
            "list_emails": ','.join(c.get_list_emails()),
        } for c in courses if c.nb_students() > 0]


    elif type_request == "departement":
        departements = Departement.objects.all()
        item_list = [{
            "label": d.name,
            "nb_students": d.nb_students(),
            "rate_answer": round(d.nb_answers()/float(d.nb_surveys())*100, 1),
            "list_emails": ','.join(d.get_list_emails()),
        } for d in departements if d.nb_surveys() > 0]

    else:
        raise Http404

    data = {
        "item_list": item_list,
        "type_request": type_request,
        "list_emails": ','.join(get_list_emails()),
    }

    template = loader.get_template('controlPanel/specific.html')
    return HttpResponse(template.render(data, request))

@login_required(login_url='/s2ip/connecter')
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

@login_required(login_url='/s2ip/connecter')
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

def connect(request):
    controlPanel.models.create_admins()
    logout(request)
    username = password = ''
    message = " Vous êtes actuellement déconnecté, connectez-vous pour profiter du site."
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                print(user)
                print(type(user))
                login(request, user)
                message = "Vous êtes désormais connecté, selectionnez les onglets \
                que vous souhaitez visiter."
        else:
            message = "Identifiant ou mot de passe incorrect ou vous ne disposez \
            pas des droits suffisants."

    template = loader.get_template('controlPanel/login.html')
    return HttpResponse(template.render({"message": message}, request))

@login_required(login_url='/s2ip/connecter')
def typeFormEditView(request, id_q = None):
    typeForm_list = TypeForm.objects.all()
    data = {}

    if 'action' in request.GET:
        action = request.GET['action']
        if action == "delete":
            print("delete")
            TypeForm.objects.get(id = id_q).delete()
            id_q = None

        if action == "copy":
            print("copy")
            # copy the tf
            tf = TypeForm.objects.get(id = id_q)
            tf.name = tf.name + " (copie)"
            tf.id = None
            tf.save()
            typeForm_list = TypeForm.objects.all()

            # copy all the questions
            questions = Question.objects.filter(typeForm__id = id_q)
            for q in questions:
                q.id = None
                q.typeForm = tf
                q.save()
            id_q = tf.id

    if id_q == None:
        if len(typeForm_list) > 0:
            id_q = list(typeForm_list)[0].id
        else:
            tf = TypeForm(name = "Votre nouveau questionnaire", description = "")
            tf.save()
            id_q = tf.id
            print(id_q)
            typeForm_list = TypeForm.objects.all()
    token = None
    try:
        token = Token.objects.get(user = request.user)
    except Token.DoesNotExist:
        token = Token.objects.create(user= request.user)
        token.save()

    current = TypeForm.objects.get(id = id_q)
    data = {
        "current_id": current.id,
        "current_name": current.name,
        "current_description": current.description,
        "typeForm_list": typeForm_list,
        "STATIC_URL": STATIC_URL,
        "user": request.user,
        "token": token
    }

    template = loader.get_template('controlPanel/survey_edit.html')
    return HttpResponse(template.render(data, request))
