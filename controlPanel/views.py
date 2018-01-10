from django.shortcuts import render
from django.http import HttpResponse
from api.models import *
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template('controlPanel/home.html')
    return HttpResponse(template.render({}, request))

def general(request):
    template = loader.get_template('controlPanel/generalView.html')
    return HttpResponse(template.render({}, request))

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
