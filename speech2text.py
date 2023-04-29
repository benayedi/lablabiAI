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
print ("######## translated text ###########")
print(response[0]["translations"][0]["text"])

##########################

# set up the API endpoint URL and authentication headers
api_url = "https://<your-resource-name>.cognitiveservices.azure.com/language/QuestionAnswering/v1.0/predict"
api_key = "<your-api-key>"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": api_key
}

# define the request payload with the question and context text
request_payload = {
    "question": "What is the capital of France?",
    "context": "France is a country in Western Europe. Its capital is Paris."
}

# make the HTTP POST request to the API endpoint with the request payload and headers
response = requests.post(api_url, data=json.dumps(request_payload), headers=headers)

# check if the request was successful and print the answer if available
if response.ok:
    result = json.loads(response.text)
    answer = result["answers"][0]["answer"]
    print(answer)
else:
    print("Error:", response.text)