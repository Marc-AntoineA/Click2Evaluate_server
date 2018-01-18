from django.shortcuts import render
from django.http import HttpResponse, Http404
from api.models import *
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template('controlPanel/home.html')
    return HttpResponse(template.render({}, request))

def general(request):
    template = loader.get_template('controlPanel/generalView.html')
    data = {
        "nb_students": len(Student.objects.all()),
        "nb_courses": len(Student.objects.all()),
        "nb_answers": len(Survey.objects.filter(answered = True)),
        "rate_answer": round(100.*len(Survey.objects.filter(answered = True))/len(Survey.objects.all()), 1),
    }
    return HttpResponse(template.render(data, request))

def project(request):
    template = loader.get_template('controlPanel/project.html')
    return HttpResponse(template.render({}, request))

def importDb(request):
    template = loader.get_template('controlPanel/import.html')
    return HttpResponse(template.render({}, request))

def exportDb(request):
    template = loader.get_template('controlPanel/export.html')
    return HttpResponse(template.render({}, request))

def typeFormView(request, id_q = None):
    typeForm_list = TypeForm.objects.all()
    data = {}
    if id_q != None:
        current = TypeForm.objects.get(id = id_q)


        data = {
            "current_id": current.id,
            "current_name": current.name,
            "current_description": current.description,
            "typeForm_list": typeForm_list,
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
    #if request.method =="GET" and 'key' in request.GET:
    #    if request.GET['key'] == "data":
    #        f = (lambda x: x["label"])
    #    elif request.GET['key'] == "number":
    #        f = (lambda x: x["nb_students"])
    #    elif request.GET['key'] == "rate":
    #        f = (lambda x: x["rate_answer"])

    reverse = False
    #if request.method =="GET" and 'order' in request.GET:
    #    if request.GET['order'] == "inverse":
    #        reverse = True

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
    answers = ["Oui", "Oui", "Oui", "Non"]
    frq_answers = {}
    max_frq = 0

    if question.type_question == "selectOne" or question.type_question == "select":
        for a in answers:
            if a in frq_answers:
                frq_answers[a] += 1
            else:
                frq_answers[a] = 0
            max_frq = max(frq_answers[a], max_frq)


    print(frq_answers)
    rate_answer = 0
    if len(QuestionWithAnswer.objects.filter(question = question)) > 0:
        rate_answer = round(100.*len(QuestionWithAnswer.objects.filter(question = question, survey__answered = True))/len(QuestionWithAnswer.objects.filter(question = question)), 1),

    data = {
        "question_label": question.label,
        "question_type": question.type_question,
        "nb_answers": len(QuestionWithAnswer.objects.filter(question = question, survey__answered = True)),
        "rate_answer": rate_answer,
        "frq_answers": frq_answers,
        "max_frq": max_frq,
    }
    return HttpResponse(template.render(data, request))
