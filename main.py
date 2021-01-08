import io
import cv2
import requests
import json 
from googletrans import Translator
import googletrans
from flask import Flask

URL_API = "https://api.ocr.space/parse/image"

app = Flask(__name__)

def ask():
  img = None
  while type(img) == type(None): 
    x = input("Please enter the name of a screenshot with text: ")
    img = cv2.imread(str(x))
    if type(img) == type(None):
      print("Try again")
  return img 


def lang_code_check(answer):
  language = ""
  if answer == "Arabic":
    language = "ara"
  elif answer == "Bulgarian":  
    language = "bul"
  elif answer == "Chinese (Simplified)":
    language = "chs"
  elif answer == "Chinese (Traditional)":
    language = "cht"
  elif answer == "Croatian":
    language = "hrv"
  elif answer == "Danish":
    language = "dan"
  elif answer == "Dutch":
   language = "dut"
  elif answer == "English":
   language = "eng"
  elif answer == "Finnish":
   language = "fin"
  elif answer == "French":
   language = "fre"
  elif answer == "German":
    language = "ger"
  elif answer == "Greek":
    language = "gre"
  elif answer == "Hungarian":
    language = "hun"
  elif answer == "Korean":
    language = "kor"
  elif answer == "Italian":
   language = "ita"
  elif answer == "Japanese":
   language = "jpn"
  elif answer == "Polish":
   language = "pol"
  elif answer == "Portuguese":
   language = "pol"
  elif answer == "Russian":
   language  = "rus"
  elif answer == "Slovenian":
   language = "slv"
  elif answer == "Spanish":
   language = "spa"
  elif answer == "Swedish":
   language = "swe"
  elif answer == "Turkish":
   language = "tur"

  return language

def google_codes(answer):
  language = "en"
  if answer == "arabic":
    language = "ar"
  elif answer == "bulgarian":  
    language = "bg"
  elif answer == "chinese (simplified)":
    language = "zh-cn"
  elif answer == "chinese (traditional)":
    language = "zn-tw"
  elif answer == "croatian":
    language = "hr"
  elif answer == "danish":
    language = "da"
  elif answer == "dutch":
   language = "nl"
  elif answer == "english":
   language = "en"
  elif answer == "finnish":
   language = "fi"
  elif answer == "french":
   language = "fr"
  elif answer == "german":
    language = "du"
  elif answer == "greek":
    language = "el"
  elif answer == "hungarian":
    language = "hu"
  elif answer == "korean":
    language = "ko"
  elif answer == "italian":
   language = "it"
  elif answer == "japanese":
   language = "ja"
  elif answer == "polish":
   language = "pl"
  elif answer == "portuguese":
   language = "pt"
  elif answer == "russian":
   language  = "ru"
  elif answer == "slovenian":
   language = "sl"
  elif answer == "spanish":
   language = "es"
  elif answer == "swedish":
   language = "sv"
  elif answer == "turkish":
   language = "tr"

  return language

def language(lang = "", tran = ""):
  answer = input("Text Language (capitalized):") if lang == "" else lang
  language = lang_code_check(answer)
  

  translate = input("Translated Text Language:") if tran == "" else tran
  translate.lower()
  list_code = []
  list_code.append(answer)
  list_code.append(language)
  list_code.append(translate)
  list_code.append(lang_code_check(translate))
  return list_code

def size(img, hight, width):
  # height, width, _  = img.shape 
  roi = img[0: hight, 0: width ]
  #roi = img=[startingHeight: endingHeight, startingWidth: endingWidth]
  _, compressesdimage = cv2.imencode(".jpg", roi, [1,90])
  file_bytes = io.BytesIO(compressesdimage)
  return file_bytes

def request_orc(file_bytes, userInputs):
  result = requests.post(URL_API, 
                files = {"scrennshot.jpg": file_bytes},
                data = {"apikey" : "helloworld",
                        "language": userInputs[1] })

  result = result.content.decode()
  result = json.loads(result)
  return result

def parsed_text(results):
  parsed_results = results.get("ParsedResults")[0]
  text_detected = parsed_results.get("ParsedText")
  return text_detected
  
def single_line(text):
  new_text = ""
  for letter in text:
    if letter == "\n":
      new_text = new_text + " "
    else:
      new_text += letter
  return new_text

def formation(text):
  ask = input("Format your text?")
  ask.lower()
  if ask == "yes":
    text = " ".join(text.splitlines())
  return text
  
def main():
  img = ask() 
  userInputs = language()
  height, width, _  = img.shape 
  file_bytes = size(img, height ,width)
  result = request_orc(file_bytes,userInputs)
  parsedText = parsed_text(result)
  text = single_line(parsedText)
  newText = formation(text)
  with open("originalText.txt", "w") as fileoutput:
    fileoutput.write(newText)
  translator = Translator()
  translated = translator.translate(newText, src= userInputs[0].lower(), dest= userInputs[2])

  with open("translatedText.txt", "w") as fileoutput:
    fileoutput.write(translated.text)

@app.route("/ocr/<img_url>/")
@app.route("/ocr/<img_url>/<lang>/<translate>")
def flask_main(img_url="image.jpg", lang="English", translate="English"):
  img = cv2.imread(str(img_url))
  if type(img) == type(None):
    raise ValueError("Cannot find image")
  height, width, _  = img.shape 
  file_bytes = size(img, height ,width)
  lang_list = language(lang, translate)
  result = request_orc(file_bytes,lang_list)
  parsedText = parsed_text(result)
  text = single_line(parsedText)
  newText = " ".join(text.splitlines())
  print(newText)
  translator = Translator()
  print("TRY TO TRANSLATE")
  print(google_codes(lang.lower()))
  print(google_codes(translate.lower()))
  translated = translator.translate(newText, src= google_codes(lang.lower()), dest= google_codes(translate.lower()))
  print("TRANSLATION DONE")
  return str(translated)

@app.route("/")
def index():
  return "This is an OCR translator"

if __name__ == "__main__":
  #main()
  app.run(host="0.0.0.0")
  #print("Running...")
  #print(flask_main())
