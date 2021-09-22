from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body, Request, Form
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson.objectid import ObjectId
import numbering
import pymongo
import uuid
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import datetime
from bs4 import BeautifulSoup
import urllib.request

load_dotenv()

myclient = pymongo.MongoClient(os.environ.get("DB_URL"))

mydb = myclient["NLPdataBase"]
collection = mydb["database"]


class ANS(BaseModel): 
	text : str
	answer_start : int

class QAS(BaseModel) :
	question : str
	id : str
	answer : ANS

class data(BaseModel) : 
	content : str
	qas: list
 
class NEWS(BaseModel): 
	content : str
	qas : list

 
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def form_delete(request: Request):
    colname = mydb.list_collection_names()
    print(colname)
    return templates.TemplateResponse("index.html", {"request": request, "CollectionName":colname})

@app.post('/')
async def createCollection(request: Request, colname: str  = Form(...), ip: str = Form(...)):
    print(colname) 
    time = datetime.datetime.now()
    collection = mydb[colname]
    create_time = {"name": colname, "time create": time, "ip": ip}
    x = collection.insert_one(create_time)
    colname = mydb.list_collection_names()
    return templates.TemplateResponse("index.html", {"request": request, 
                                                     "CollectionName":colname})



        
@app.post("/display", response_class=HTMLResponse)
def loadData(request: Request, nameCollection:str = Form(...) ):
    colname = mydb.list_collection_names()
    collection = mydb[nameCollection]
    li = list(collection.find())
    size = len(li)
    print(colname)
    tieude = "Xem tất cả data đã nhập từ collection "+ nameCollection
    return templates.TemplateResponse("displayData.html", {
        "request": request, 
        "size" : size,
        "jsonData" : li,
        "tieude" : tieude,
        "CollectionName":colname,   
        "nameCollection":nameCollection,
})


@app.get("/home", response_class=HTMLResponse)
def write_home(request: Request ):
    colname = mydb.list_collection_names()
    user_name = "MTA NLP TEAM"
    return templates.TemplateResponse("home.html", {"request": request,
                                                    "username": user_name,
                                                    "CollectionName":colname,
                                                    })


def MainProcess(collection, content, listQuestion , listAnswer):# tạo data và thêm vào db
    listContent = numbering.contentToList(content)
    listQAS = list()
    for i in range(len(listAnswer)):
        answer = listAnswer[i]
        question = listQuestion[i]
        start = numbering.findSentence(answer,listContent)
        objAnswer = ANS(
            text = answer,
            answer_start = start
        )
        id = (uuid.uuid4().hex)
        objQuestionAndAnswer = QAS(
            question = question,
            id = id,
            answer = objAnswer
        )
        listQAS.append(objQuestionAndAnswer.dict())
    print(len(listQAS))
    newData = data(
        content = content,
        qas = listQAS
    )
    print(collection)
    collection.insert_one(newData.dict())
    return (newData.dict())


@app.post('/home')
async def handle_form(content : str = Form(...), qas : list = Form(...), nameCollection:str = Form(...)):
    collection = mydb[nameCollection]
    listQuestion = numbering.createListQuestion(qas) 
    listAnswer = numbering.createListAnswer(qas)
    return MainProcess(collection, content, listQuestion, listAnswer)


@app.get("/display-data", response_class=HTMLResponse)
def loadGetAllData(request: Request):
    colname = mydb.list_collection_names()
    tieude = "Xem tất cả data đã nhập"
    return templates.TemplateResponse("displayData.html", {
        "request": request, 
        "tieude" : tieude,
        "CollectionName":colname,
        })
    
    


@app.get("/delete/{id}/{nameCollection}")
async def form_delete(request: Request, id : str, nameCollection : str):
    collection = mydb[nameCollection]
    myquery = {"_id":  ObjectId(id)}
    li = collection.find_one(myquery)
    content = li['content']
    qas = li['qas']
    tieude = "Xem lại data đã xóa"
    collection.delete_one(myquery)
    
    return templates.TemplateResponse("delete.html", {"request": request,
                                                      "tieude": tieude,
                                                      "content": content,
                                                      "qas" : qas})
    
    


@app.get("/editData/{id}/{nameCollection}", response_class=HTMLResponse)
def editData(request: Request, id : str, nameCollection: str):
    collection = mydb[nameCollection]
    myquery = {"_id":  ObjectId(id)}
    obj = collection.find_one(myquery)
    content = obj['content']
    qas = obj['qas']
    return templates.TemplateResponse("editData.html", {
        "request": request, 
        "content" : content,
        "qas" : qas,
        "id": id,
        "nameCollection":nameCollection,
    })
    
    

def UpdateProcess(collection, idObj, content, listQuestion , listAnswer):# update một bảng ghi trong db
    listContent = numbering.contentToList(content)
    listQAS = list()
    for i in range(len(listAnswer)):
        answer = listAnswer[i]
        question = listQuestion[i]
        start = numbering.findSentence(answer,listContent)
        objAnswer = ANS(
            text = answer,
            answer_start = start
        )
        id = (uuid.uuid4().hex)
        objQuestionAndAnswer = QAS(
            question = question,
            id = id,
            answer = objAnswer
        )
        listQAS.append(objQuestionAndAnswer.dict())
    print(len(listQAS))
    newData = data(
        content = content,
        qas = listQAS
    )
    myquery = {"_id":  ObjectId(idObj)}
    newvalues = { "$set": newData.dict()}

    collection.update(myquery, newvalues)
    return (newData.dict())


    
    
@app.post('/update-data')
async def updateData(content : str = Form(...), qas : list = Form(...), id = Form(...), nameCollection: str = Form(...)):
    print(id)
    collection = mydb[nameCollection]
    listQuestion = numbering.createListQuestion(qas)
    listAnswer = numbering.createListAnswer(qas)
    return UpdateProcess(collection, id, content, listQuestion, listAnswer)




@app.get("/guide", response_class=HTMLResponse)
def write_home(request: Request):
    return templates.TemplateResponse("guide.html", {"request": request})


# ========================================= CRAWL DATA ===========================================================


@app.get("/crawl", response_class=HTMLResponse)
async def form_delete(request: Request):
    colname = mydb.list_collection_names()
    print(colname)
    return templates.TemplateResponse("crawl.html", {"request": request, "CollectionName":colname})

@app.post('/crawl')
async def createCollection(nameCollection: str  = Form(...), url: str = Form(...)):
    print(nameCollection) 
    time = datetime.datetime.now()
    collection = mydb[nameCollection]
    create_time = {"name": nameCollection, "time create": time}
    x = collection.insert_one(create_time)
    diclist = crawlData(url)
    for li in diclist:
        content = li['content']
        qas = li['qas']
        listQuestion = numbering.createListQuestion(qas) 
        listAnswer = numbering.createListAnswer(qas)
        MainProcess(collection, content, listQuestion, listAnswer)
        
    
    return "done"



def crawlData(url):
    dictList = []
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    news = soup.find_all('div', attrs={'class' : 'para-wrap'})

    for i in range(len(news)):
        content = (news[i].find('pre').text)
        qaswrap = news[i].find_all('div', class_='qa-wrap')
        li = []
        for j in range(len(qaswrap)):
            question = qaswrap[j].find_all('strong',class_='question')
            answer = qaswrap[j].find_all('span',class_='answer')
            if(not len(answer)):
                answer = qaswrap[j].find_all('span',class_='no-answer')
            if(len(question)):
                li.append(question[0].text)
                li.append(answer[0].text)
        temp = NEWS(
            content = content,
            qas = li
        ).dict()
        dictList.append(temp)
        
    return dictList
