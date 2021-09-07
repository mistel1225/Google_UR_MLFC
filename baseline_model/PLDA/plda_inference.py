from __future__ import annotations
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import tomotopy as tp

#第一次執行要安裝 之後可以刪掉
import nltk
nltk.download('wordnet')

label_map = {'Account': 'A',
 'Third Party App': 'B',
 'Appearance': 'C',
 'Audio/Voice': 'D',
 'Backup': 'E',
 'Battery': 'F',
 'Bluetooth': 'G',
 'Boot': 'H',
 'Camera': 'I',
 'Communication': 'J',
 'Customer Service': 'K',
 'Device Connection': 'L',
 'Feature Request and suggestion': 'M',
 'GPS': 'N',
 'Google App': 'O',
 'Headphone': 'P',
 'Internet': 'Q',
 'Multimedia': 'R',
 'Notification': 'S',
 'Screen': 'T',
 'Security': 'U',
 'Setup': 'V',
 'Sim/eSim': 'W',
 'Software/System Update': 'X',
 'Stability': 'Y',
 'Storage': 'Z',
 'System Service': 'a',
 'USB/Type-C': 'b',
 'Useless': 'c',
 'Virtual Assistance': 'd'}

topictolabel = {v: k for k, v in label_map.items()}

stemmer = PorterStemmer()
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def inference(mdl:tp.PLDAModel, title:str, content:str, threshold:float=.05, ground_truth:list=[], print_detail:bool=False) -> Tuple[list, float]:

  if print_detail:
    print("title:", title)
    print("content:", content)

  doc = preprocess(title + ' ' + content)
  stopwords = ['googl', 'pixel', 'tri', 'phone', 'work', 'issu', 'help', 'time',
               'devic', 'problem', 'like', 'go', 'want', 'know', 'need', 'thank',
               'happen', 'get', 'come']
  for word in stopwords:
    while word in doc:
      doc.remove(word)

  if print_detail:
    print(doc)
  if doc == []:
      return [], 0
  
  doc = mdl.make_doc(doc)
  predicted_label = []
  result = mdl.infer(doc=doc)[0]
  for label, prob in sorted(zip(mdl.topic_label_dict, result), key=lambda x:x[1], reverse=True):
    if prob >= threshold:
      if print_detail:
        print(topictolabel[label], prob)
      predicted_label.append(topictolabel[label])
    else:
      break
  
  jaccard_score = 0

  if ground_truth:
    if print_detail:
      print("GT:", ground_truth)

    jaccard_score = len(set(predicted_label)&set(ground_truth))/len(set(predicted_label)|set(ground_truth))
    
    if print_detail:
      print("jaccard score:", jaccard_score)

  return predicted_label, jaccard_score

if __name__ == "__main__":
    model = tp.PLDAModel().load("PLDA_for_1000_labeled_data.model")
    
    t = "I cant add my esim Pixel 4 XL"
    c = """Im trying to add my esim on my pixel 4 xl but getting this error ,

Networks not activated Something went wrong while trying to activate your numbers. Please contact your network providers for help. 
You may need the EID number for this device 

Note that I am able to add this eSIM on iPhone normaly + tried different barcodes from the carrier + tried different carrier + different countries carrier got the same on all cases .

My phone is unlocked and bought it from google online store"""
    
    l = ['Sim/eSim']
    result, jaccard_score = inference(model, t, c, .1, l, print_detail=True)
    print(result, jaccard_score)
