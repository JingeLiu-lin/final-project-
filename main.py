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

def language(lang = "", tran = ""):
  answer = input("Text Language (capitalized):") if lang == "" else lang
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

  translate = input("Translated Text Language:") if tran == "" else tran
  translate.lower()
  list = []
  list.append(answer)
  list.append(language)
  list.append(translate)
  return list

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
  result = request_orc(file_bytes,language(lang, translate))
  parsedText = parsed_text(result)
  text = single_line(parsedText)
  newText = " ".join(text.splitlines())
  translator = Translator()
  translated = translator.translate(newText, src= lang.lower(), dest= translate)
  return str(translated)

@app.route("/")
def index():
  return "This is an OCR translator"

if __name__ == "__main__":
  #main()
  app.run(host="0.0.0.0")
  #print("Running...")
  #print(flask_main())
