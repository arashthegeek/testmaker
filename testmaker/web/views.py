from django.shortcuts import render, HttpResponse
import re
from . import ai
import json
import random
from . import models

def indexpage(request):
    return render(request,'index.html')

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
از این متن سوالات چهارگزینه ای تولید کن و به json تبدیل کن.(زیر 40 ثانیه)
json به این فرم باشد:
{
  "questions" : [
    {
      "question": text of quastion
      "options": [
        option1,
        option2,
        option3,
        option4,
      ],
      "answer": text of correct option
    },
}"""
        ai_quastion = ai_quastion.replace("\n"," ")
        #---
        
        jstring = str(ai.quastiontojson(ai_quastion))
        
        
        data = json.loads(jstring)

        question_list = data['questions']
        if len(question_list) == 0:
            pass #return 'noquestionsfound!'   --becasuse its empty of questions

        counter = 0
        for question in question_list:
            counter += 1
            q = question['question']
            
            o = question['options']
            
            oa = o[0]
            ob = o[1]
            oc = o[2]
            od = o[3]
            a = question['answer']
            
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
        
        return HttpResponse(f"آیدی: {id}")
        
    return render(request, 'mainpage.html')

def exampage(request):
    if request.method == "GET":
        if 'id' in request.GET:
            id = request.GET['id']
            Idcourse = models.IdCourse.objects.get(id=id)
            quastionobjectslist = models.IdQuastion.objects.filter(IdCoursef=Idcourse)
            
            return render(request,'exam.html',{'qlist' : quastionobjectslist,'id':id})
        else:
            return render(request,'exampage.html')
    if request.method == "POST":
        course_id = request.POST['id']
        q_a = []
        for j in request.POST:
            if j == "id" or j == "csrfmiddlewaretoken":
                continue
            j_id = ""
            j_option = ""
            bin_beforeunderscore = True
            for x in list(j):
                if x == "o":
                    continue
                if x == "_":
                    bin_beforeunderscore = False
                    continue
                if bin_beforeunderscore:
                    j_id += x
                else:
                    j_option += x
            q_a.append([j_id,j_option])
        
        http__responses = []
        for z in q_a:
            q = models.IdQuastion.objects.get(id=int(z[0])) #object
            correct_answer = q.Correct_Option #abcd
            user_answer = z[1].replace(" ","") #abcd
            question_text = q.Quastion #question?
            Ccourse = q.IdCoursef.course
            oa = q.Option_a #choice a
            ob = q.Option_b #choice b
            oc = q.Option_c #choice c
            od = q.Option_d #choice d
            Is_correct = False
            if user_answer == correct_answer:#quastion? [options] your choice:x correct choice:y
                Is_correct = True
            http__responses.append(f"{question_text} / a){oa} / b){ob} / c){oc} / d){od} / your choice: {user_answer}; correct choice:{correct_answer};")
        
        base_res = ""
        for k in http__responses:
            base_res += k
        
        qtoai = f"""'{Ccourse}' (زیر 40 ثانیه جواب بده)از این درس این سوالات چهارگزینه ای را طرح کردم و کاربر این جواب هارا داده است با توجه به جواب های کاربر آن مباحثی از درس را که یاد نگرفته است را برایم بنویس. {base_res}"""
        lines = qtoai.split('\r\n')
        qtoai_text = ""
        for line in lines:
            qtoai_text += line + " "
        re.sub(r'[\u200c\u200b\u200d\u2060]', '', qtoai_text)
        qtoai_text = qtoai_text.replace("\n"," ")
        
        ai_res = ai.aichat(qtoai_text)
        ai_res = ai_res.replace("<think>", "")
        ai_res = ai_res.replace("</think>", "")
        
        return render(request,'result.html',{'result':http__responses, 'ai_response':ai_res})