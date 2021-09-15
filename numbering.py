import re
from pydantic import BaseModel


class senctence(BaseModel):
    text : str
    start_with : int

# hàm contentToList : nhập vào {đoạn văn bản} trả về {list các câu trong đoạn}

def contentToList(str):
    l = re.compile("[.|?|!]\s(?=[A-Z|Â|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ])").split(str) 
    matches = re.finditer("[.|?|!]\s(?=[A-Z|Â|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ])", str, re.MULTILINE)
    res = []
    new = senctence(
        text = l[0],
        start_with = 0
    )
    res.append(new.dict())
    for matchNum, match in enumerate(matches):
        newSentence = senctence(
            text = l[int(matchNum) + 1],
            start_with = match.end() + 1
        )
        res.append(newSentence.dict())
    return res

# hàm findSentence : nhập vào {câu cần tìm và list các câu } trả về {start_with} của câu trong đoạn văn bản

def findSentence(s, listDict):
    k2 = s.split()
    max = 0 
    res = ""
    start = -1
    for i in listDict:
        mark = 0
        k1 = i['text']
        for j in range(len(k2)):
            if(k2[j] in k1):
                mark += 1
        # print(i['text'] + " Mark = " + str(mark))
        if(mark > max):
            res = i['text']
            max = mark
            start = i['start_with']
    # print("\n"+res)
    return start


def createListQuestion(rawList):
    listQuestion = list()
    for i in range(0,len(rawList), 2):
        listQuestion.append(rawList[i])
    return listQuestion


def createListAnswer(rawList):
    listAnswer = list()
    for i in range(1,len(rawList), 2):
        listAnswer.append(rawList[i])
    return listAnswer



