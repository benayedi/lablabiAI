import requests, uuid, json
import azure.cognitiveservices.speech as speechsdk

# set up the speech configuration
speech_key = "2720979498ec43d4b4e30e0b8e98637b"
service_region = "westeurope"
original_text_language_format1 = "fr-FR"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, 
                                       speech_recognition_language=original_text_language_format1)

# set up the audio configuration
audio_filename = "testmakethon.wav"
audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

# create a speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
done = False
original_outputText = ""
# perform speech recognition
def recognize_once():
    """performs one-shot recognition and returns the recognized text"""
    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return "***"

while True:
    result = recognize_once()
    if (result != "***"):
        original_outputText += result
    else:
        break

# output the recognized text
print(original_outputText)

#############################
#translatte the text to english
original_text_language_format2 = "fr"
# Add your key and endpoint
translator_key = "b58c7354a3404536b92e2578af8ec3eb"
translator_endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
translator_location = "westeurope"

translator_path = '/translate'
constructed_url = translator_endpoint + translator_path

params = {
    'api-version': '3.0',
    'from': original_text_language_format2,
    'to': ['en']
}

headers = {
    'Ocp-Apim-Subscription-Key': translator_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': translator_location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text': original_outputText
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()
translated_text = response[0]["translations"][0]["text"]
print ("######## translated text ###########")
print(translated_text)

##########################
#  ---------------------------QUESTIONS ABOUT THE TEXT--------------------------------------
# set up the API endpoint URL and authentication headers
api_url = "https://fokzebi.cognitiveservices.azure.com/language/:query-text"
api_key = "4caeb17bbddd400b84acc4b78e36371b"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": api_key
}  

# define the request payload with the question and context text
params = {
    "api-version": "2021-10-01"
}

body = {
	"question": "when were the tasks completed?",
	"records": [{
        "id" :"1",
        "text": translated_text
        }]
}
print("########################")
# make the HTTP POST request to the API endpoint with the request payload and headers
request = requests.post(api_url,params=params, headers=headers, json=body)
# print(request.text)
response = request.json
# data = request.text
data = json.loads(request.text)
# print(data)
# check if the request was successful and print the answer if available
results = []
print("#############")
answers_list = []
for answer in data['answers']:
    if answer['answerSpan'] is not None:
        text = answer['answerSpan']['text']
        confidence_score = answer['answerSpan']['confidenceScore']
        answers_list.append((text, confidence_score))

print(answers_list)

#  ---------------------------QUESTIONS ABOUT THE IMAGE--------------------------------------
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bd95a01470fb40db990faa99a06b260e',
}

params = {
    # Request parameters
    'api-version' : '2023-02-01-preview',
    'features': 'DenseCaptions',
    'language': 'en',
    'gender-neutral-caption': 'False'
}
body = {
	"url": "https://portal.vision.cognitive.azure.com/dist/static/media/DenseCaptioningSample0.d3cd70fb.png"
}
picapi_url= "https://aaazsd.cognitiveservices.azure.com/computervision/imageanalysis:analyze"
request = requests.post(picapi_url,params=params, headers=headers, json=body)
response = request.json()
data = json.loads(request.text)
# Concatenate the text values
result = ''
for value in data['denseCaptionsResult']['values']:
    result += value['text'] + '\n'
# Create a list of dictionaries with text, length, and confidence values
array = []
for value in data['denseCaptionsResult']['values']:
    array.append({
        'text': value['text'],
        'length': len(value['text']),
        'confidence': value['confidence']
    })

# Print the resulting array

print(data)
print(result)
print(array)



     
