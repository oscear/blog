from django.shortcuts import render
from django.views import View
from rest_framework.templatetags.rest_framework import data

from .models import Article, Category, Banner, Tag, Link
import json
from rest_framework import serializers
from django.http import JsonResponse, HttpResponse



def get_json(request):
    a = Article.objects.all()
    data['result'] = json.loads(serializers.serialize("json", a))
    return JsonResponse(data)