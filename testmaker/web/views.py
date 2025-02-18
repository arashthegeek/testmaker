from django.shortcuts import render, HttpResponse
import re
from . import ai
import json
import random
from . import models

# Create your views here.
def mainpage(request):
    if request.method == "POST":
        course = request.POST['course']
        
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0912345678"
        id = ""
        for _ in range(8):
            id += chars[random.randint(0,len(chars)-1)]
        
        #---save the course and cid(as key) into db---
        
        lines = course.split('\r\n')
        course_text = ""
        for line in lines:
            course_text += line + " "
        re.sub(r'[\u200c\u200b\u200d\u2060]', '', course_text)
        cid = models.IdCourse(id=id,course=course_text) #---save the course and cid(as key) into db---
        cid.save()
        ai_quastion = """'"""+course_text+"""'
از این متن سوالات چهارگزینه ای تولید کن و به json تبدیل کن.
json به این فرم باشد:
{
  "questions" : [
    {
      "question": 
      "options": [

      ],
      "answer": 
    },
}"""
        ai_quastion = ai_quastion.replace("\n"," ")
        #---
        print(ai_quastion)
        jstring = str(ai.quastiontojson(ai_quastion))
        print(f"---json>> {jstring}")
        
        data = json.loads(jstring)

        question_list = data['questions']
        if len(question_list) == 0:
            pass #return 'noquestionsfound!'   --becasuse its empty of questions

        counter = 0
        for question in question_list:
            counter += 1
            q = question['question']
            print(q)
            o = question['options']
            print(o)
            oa = o[0]
            ob = o[1]
            oc = o[2]
            od = o[3]
            a = question['answer']
            print(a)
            if a == oa:
                ao = 'a'
            elif a == ob:
                ao = 'b'
            elif a == oc:
                ao = 'c'
            elif a == od:
                ao = 'd'
            else:
                continue
        
            #__---__ here add to models with cid as key
            quastion_model = models.IdQuastion(IdCoursef=cid,Quastion=q,Option_a=oa,Option_b=ob,Option_c=oc,Option_d=od,Correct_Option=ao)
            quastion_model.save()
        
        return HttpResponse(f"id: {id}")
        
    return render(request, 'mainpage.html')