from bs4 import BeautifulSoup
import requests
import re
import unicodedata


class GoogleResult:
    def __init__(self):
        self.name = None
        self.link = None
        self.description = None


# question = "ai là người giàu nhất việt nam"

   

def GoogleSearchKiet(question):
    param = {"q": question}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
    }
    r = requests.get("https://google.com/search", params=param, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    soup.prettify()
    #debug
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
    infotext = ""
    info = soup.find('span', {'class', 'hgKElc'})
    if(info):
        infotext = info.text
    # print(infotext)
    listall = soup.findAll('div', {'class','g'})    
    result = []
    for liItem in listall:
        try:
            obj = GoogleResult()
            obj.link =  liItem.find('a')['href']
            if obj.link.startswith("/search?"):
                continue
            obj.name = liItem.find('h3',{'class','LC20lb MBeuO DKV0Md'}).get_text()
            snippets = liItem.find('div',{'class','VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})
            
            if not snippets:
                obj.description = infotext
                result.append(obj)
                continue
            
            new_str = unicodedata.normalize("NFKD", snippets.get_text()).strip()
            if('—' in new_str):
                new_str = new_str[new_str.find('—'):].replace('—','')
            obj.description = (new_str)
            result.append(obj)
        except Exception as e :
            print(e)
    return result
    
    

# a = GoogleSearch(question)

# for i in range(len(a)):
#     # print(a[i].name, a[i].link)
#     print(a[i].description)
#     print()
