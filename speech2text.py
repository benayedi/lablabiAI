import requests
import uuid
import json
import azure.cognitiveservices.speech as speechsdk


# def recognize_speech():
# set up the speech configuration
def speech_to_text(original_text_language_format1, audio_filename):
    speech_key = "2720979498ec43d4b4e30e0b8e98637b"
    service_region = "westeurope"
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=service_region,
        speech_recognition_language=original_text_language_format1,
    )

    # set up the audio configuration
    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    # create a speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
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
        if result != "***":
            original_outputText += result
        else:
            break

    # output the recognized text
    return original_outputText



def translate_text(
    text_to_translate,
    from_language,
):
    """Translates the text to the specified languages and returns the translations."""
    # Set up the API endpoint URL and authentication headers

    to_languages = ["en"]
    translator_key = "b58c7354a3404536b92e2578af8ec3eb"
    translator_endpoint = "https://api.cognitive.microsofttranslator.com"
    translator_location = "westeurope"

    translator_path = "/translate"
    constructed_url = translator_endpoint + translator_path
    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # Set up the request parameters and body
    params = {"api-version": "3.0", "from": from_language, "to": to_languages}
    body = [{"text": text_to_translate}]

    # Make the request and parse the response
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response_data = response.json()
    translations = [item["translations"][0]["text"] for item in response_data]

    return translations[0]


def answer_question(question, context):
    """Asks a question and returns the answer."""
    
    api_url = "https://fokzebi.cognitiveservices.azure.com/language/:query-text"
    api_key = "4caeb17bbddd400b84acc4b78e36371b"

    # Set up the API endpoint URL and authentication headers
    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
    params = {"api-version": "2021-10-01"}

    # Set up the request body
    body = {"question": question, "records": [{"id": "1", "text": context}]}

    # Make the request and parse the response
    response = requests.post(api_url, params=params, headers=headers, json=body)
    response_data = response.json()
    answers_list = [
        (answer["answerSpan"]["text"], answer["answerSpan"]["confidenceScore"])
        for answer in response_data["answers"]
        if answer["answerSpan"] is not None
    ]

    return answers_list[0][0]


def analyze_image(image_path):
    picapi_url = "https://aaazsd.cognitiveservices.azure.com/computervision/imageanalysis:analyze"

    pic_api_key = "bd95a01470fb40db990faa99a06b260e"
    """Analyzes an image and returns the dense captions."""
    # Set up the request parameters and headers
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": pic_api_key,
    }
    params = {
        "api-version": "2023-02-01-preview",
        "features": "DenseCaptions",
        "language": "en",
        "gender-neutral-caption": "False",
    }
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    body = image_bytes
    request = requests.post(picapi_url, params=params, headers=headers, data=body)

    data = json.loads(request.text)
    # Concatenate the text values
    result = ""
    for value in data["denseCaptionsResult"]["values"]:
        result += value["text"] + ". "
    # Create a list of dictionaries with text, length, and confidence values
    array = []
    for value in data["denseCaptionsResult"]["values"]:
        array.append(
            {
                "text": value["text"],
                "length": len(value["text"]) + 2,  # +2 because ". "
                "confidence": value["confidence"],
            }
        )

    # Print the resulting array

    print(result)
    print(array)
    return (result,array)


# analyze_image(
#     "https://portal.vision.cognitive.azure.com/dist/static/media/DenseCaptioningSample0.d3cd70fb.png"
# )

# print(answer_question("what is the task id?", ""))