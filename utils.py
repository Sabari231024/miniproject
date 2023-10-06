import requests
import gtts as gt
import os
from googletrans import Translator
from playsound import playsound
import easyocr

#part1 object recognition

def object_recognition(image):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}

    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()

    output = query(image)
    text=output[0]['generated_text']
    return(text)
    
    
#part2 ocr detection
def ocr_detection(image):
    lang_list=["hi","mr","ne","en"]
    reader = easyocr.Reader(lang_list)
    translator=Translator()
    bounds = reader.readtext(image, add_margin=0.55, width_ths=0.7, link_threshold=0.8, decoder='beamsearch', blocklist='=.',detail=0)
    text_comb=' '.join(bounds)
    lan1=translator.detect(text_comb)
    l=lan1.lang
    text2=[]
    for i in bounds:
        lan=translator.detect(i)
        if  lan.lang==l or lan.lang in lang_list:
            text1=translator.translate(i,src=lan.lang)
            text2.append(text1.text)
    text=' '.join(text2)
    if text:
        trans(text)
    else:
        None
    return(text)
    
#debbugging
#ocr_detection("")

#translateengine
def trans(text):
    
    translator=Translator()
    out=translator.translate(text,dest='ta')
    tts=gt.gTTS(text=out.text,lang='ta')
    tts.save('sample.mp3')
    playsound('sample.mp3')
    os.remove('sample.mp3')
    
    
