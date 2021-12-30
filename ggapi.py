import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

# API_KEY="9fa9843b01905bc0f6c462f8b1bec45715a47918e271ab86fb8f70ad1b0466a1"

load_dotenv()



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
        res = []
        listlink = []
        for i in range(n):
            try: 
                res.append(results["organic_results"][i]["snippet"])
                listlink.append(results["organic_results"][i]["link"])
            except Exception as e:
                print(e)
        return (res,listlink)
    else : 
        return ([],[])
    
# print(GGSearchAPI("Ai là người giàu nhất thế giới?"))


def recentQuestion():
    f = open("log.txt","r").read().split("\n")[::-1]
    return f
