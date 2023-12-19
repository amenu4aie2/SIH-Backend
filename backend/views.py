from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Employee
from .textanalysis import doT
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return JsonResponse({'foo':'bar'})


def store(request):
    data = json.loads(request.body)
    
    return JsonResponse({'foo':'saved'})
# csrf_exempt

@csrf_exempt
def doText(request):
    if request.method == 'POST':
        data = request.POST.get('text')
        # convert bytes to string
        d = doT(data)
        d = d.decode('utf-8')
        print(d)
        # Decode the byte string to a regular (UTF-8) string
        json_string = d

        # Load the string as a JSON object
        json_object = json.loads(json_string)
        print(json_object)
        return JsonResponse(json_object)