from django.shortcuts import render,redirect
import pymongo
from urllib.parse import quote
from django.http import HttpResponse
import json
import requests

def tickethistory(request):
    url="https://kce.zendesk.com/api/v2/requests"
    ticketdata=requests.get(url, auth=("19l139@kce.ac.in", "Sabarish@2002"))
    urldata=ticketdata.json()["requests"]
   
    return render(request,"ticketapp/tickethistory.html",{"ticketdata":urldata})
    
def home(request):
    global guser
    global gname
    if(request.method=="POST") and "ticket" in request.POST:
       
        department=request.POST.get("department")
        category=request.POST.get("category")
        subject=request.POST.get("subject")
        description=request.POST.get("description")
        priority=request.POST.get("priority")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        body="Department:{}\nCatrgory:{}\nDescription:{}\nPriority:{}\nName:{}\nEmail:{}\nPhone:{}".format(department,category,description,priority,name,email,phone)
        data = {'ticket': {'subject': subject, 'comment': {'body': body}}}
        payload = json.dumps(data)
        url = 'https://kce.zendesk.com/api/v2/tickets.json'
        user = '19l139@kce.ac.in'
        pwd = 'Sabarish@2002'
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)
        if response.status_code != 201:
            return render(request,"ticketapp/fail.html")
        else:
            return render(request,"ticketapp/success.html")
    if(request.method=="POST") and "login" in request.POST:
        username=request.POST.get("email")
        password=request.POST.get("password")
        myclient = pymongo.MongoClient("mongodb+srv://sunshine:hkyvtd0o4OTA5mFr@cluster0.tw2ei.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mydb = myclient["ticket"]
        mycol = mydb["ticketusers"]
        for x in mycol.find():
            if(x["useremail"]==username and x["password"]==password):
                guser=username
                gname=x["username"]
                return render(request,"ticketapp/dashboard.html",{"user":username,"name":x["username"]})
        else:
            return render(request,"ticketapp/home.html",{"msg":"Login Credentials not valid"})
    return render(request,"ticketapp/home.html")



def register(request):
    mongodata={}
    if(request.method=="POST"):
        username=request.POST.get("username")
        useremail=request.POST.get("useremail")
        password=request.POST.get("password")
        mongodata["username"]=username
        mongodata["useremail"]=useremail
        mongodata["password"]=password
        myclient = pymongo.MongoClient("mongodb+srv://sunshine:hkyvtd0o4OTA5mFr@cluster0.tw2ei.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mydb = myclient["ticket"]
        mycol = mydb["ticketusers"]
        savedata=mycol.insert_one(mongodata)
        return redirect("/")
    return render(request,"ticketapp/register.html")
