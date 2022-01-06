from infer import tokenize_function,data_collator,extract_answer
from model.mrc_model import MRCQuestionAnswering
from transformers import AutoTokenizer

from ggapi import GGSearchAPI,GGSearch
# model_checkpoint = "nguyenvulebinh/vi-mrc-base"
tokenizer = AutoTokenizer.from_pretrained('ModelTokenize')
model = MRCQuestionAnswering.from_pretrained('ModelQA')


# tokenizer.save_pretrained('ModelTokenize')
# model.save_pretrained('ModelQA')

# QA_input = {
#   'question': "Bill chuyển vị trí kiến trúc sư trưởng sang cho ai?",
#   'context': "Gates đã thôi giữ chức giám đốc điều hành của Microsoft từ tháng 1 năm 2000 nhưng ông vẫn còn là chủ tịch và kiến trúc sư trưởng về phần mềm tại tập đoàn. Tháng 6 năm 2006, Gates thông báo ông sẽ chỉ giành một phần thời gian làm việc cho Microsoft và giành nhiều thời gian hơn cho Quỹ Bill & Melinda Gates. Bill dần dần chuyển vị trí kiến trúc sư trưởng sang cho Ray Ozzie, và vị trí giám đốc chiến lược và nghiên cứu sang cho Craig Mundie.."
# }

# questions = "Ai là người giàu nhất Việt Nam?"


def answeringQA(questions):
  (listcontext,listlink,context) = GGSearch(questions)
  QA_input = {
    'question': questions,
    'context': context
  }
  
  print(QA_input,len(context))
  inputs = [tokenize_function(QA_input)]
  inputs_ids = data_collator(inputs)
  outputs = model(**inputs_ids)
  answer = extract_answer(inputs, outputs, tokenizer)
  print(answer)
  return (answer,listlink,listcontext)

# print(answeringQA(questions))
