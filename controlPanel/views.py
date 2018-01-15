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
        "nb_students": 100,
        "nb_courses": 50,
        "nb_answers": 17,
        "rate_answer": 20,
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

def survey(request):
    template = loader.get_template('controlPanel/survey.html')
    return HttpResponse(template.render({}, request))

def specific(request, type_request):
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

    item_list.sort(key = lambda x: x["label"])
    data = {
        "item_list": item_list,
        "type_request": type_request,
    }
    template = loader.get_template('controlPanel/specific.html')
    return HttpResponse(template.render(data, request))

def question_home(request):
    return HttpResponse("page question")

def question(request, id_q):
    return HttpResponse("page question specifique")
