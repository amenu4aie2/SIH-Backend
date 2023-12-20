from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Employee
from .textanalysis import doT
from django.views.decorators.csrf import csrf_exempt
import datetime
from .serializer import EmployeeSerializer
# Create your views here.
def index(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def store(request):
    if request.method == 'POST':
        data = request.POST.get('text')
        s = str(data)
        senetnces = []
        sent = ''
        for i in s:
            sent+=i
            if i=='.' or i=='?' or i=='!':
                senetnces.append(i)
                sent = ''
        res = {}
        for i in senetnces:
            t = doT(i)
            t = t.decode('utf-8')
            t = json.loads(t)
            print(t,type(t))
            if t['score']<0.6:
                t['label'] = 'normal'
            if t['label'] in res:
                res[t['label']]+=1
            else:
                res[t['label']] = 1
        res = json.dumps(res)
        # jsont to string
        res = str(res).replace('\"','')
        empName = request.POST.get('empName')
        dateNow = datetime.datetime.now()
        emp = Employee(name=empName,date=dateNow ,jsonData=res)
        emp.save()
        return JsonResponse({'status':'saved'})

    
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
    
@csrf_exempt
def getEmp(request):
    empName = request.POST.get('empName')
    emp = Employee.objects.filter(name=empName)
    # print(emp.id,emp.name,emp.date,emp.jsonData)
    emp = EmployeeSerializer(emp,many=True)
    print(emp.data)
    # emp = json.loads(emp.data)
    return JsonResponse({'data':emp.data})

@csrf_exempt
def getEmps(request):
    emp = Employee.objects.all()
    emp = EmployeeSerializer(emp,many=True)
    print(emp.data)
    return JsonResponse({'data':emp.data})

import replicate
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_Zgy3QtTt9akCXmztPXRasxZWDHBnjGh3gFIFx"

def replme(request):
    output = replicate.run(
        "nateraw/nous-hermes-llama2-awq:c71045fdc98cb810b828c43bc1421dfa6d6f5607105b91587665e3cfddcfda75",
        input={"prompt": "what is 2+2"}
    )
    # The nateraw/nous-hermes-llama2-awq model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    s = ''
    for item in output:
        # https://replicate.com/nateraw/nous-hermes-llama2-awq/api#output-schema
        s += item
        print(item, end="")
    return JsonResponse({'data':s})

