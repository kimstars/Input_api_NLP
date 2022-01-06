from Google import GoogleSearchKiet
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json


load_dotenv()

def GGSearch(question):
    f = open("log.txt","a").write("\n"+question)
    results = GoogleSearchKiet(question)
    # print(results)
    n = 8
    if(n > len(results)):
        n = len(results)
    
    
    listcontext = []
    listlink = []
    context = ""
    try: 
        for i in range(n):
                listcontext.append(results[i].description)
                listlink.append(results[i].link)
                if(listcontext):
                    context = "".join(listcontext) 
                    context.replace("...",".")
    except Exception as e:
        print(e)
    return (listcontext,listlink,context)


def GGSearchAPI(question):
    f = open("log.txt","a").write("\n"+question)
    params = {
        "engine": "google",
        "q": question,
        "api_key": os.environ.get("API_KEY"),
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    n = len(results["organic_results"])
    if(n):
        ListResult = []
        listlink = []
        for i in range(n):
            try:
                ListResult.append(results["organic_results"][i]["snippet"])
                listlink.append(results["organic_results"][i]["link"])
            except Exception as e:
                print("Error", e ,results["organic_results"][i])
        context = "".join(ListResult)
        return (ListResult,listlink,context)
    else : 
        return ([],[],"")
 

def recentQuestion():
    f = open("log.txt","r").read().split("\n")[::-1]
    return f
