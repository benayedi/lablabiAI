import azure.cognitiveservices.speech as speechsdk

# set up the speech configuration
speech_key = "2720979498ec43d4b4e30e0b8e98637b"
service_region = "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="fr-FR")

# set up the audio configuration
audio_filename = "test makethon.wav"
audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

# create a speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# perform speech recognition
result = speech_recognizer.recognize_once()

# output the recognized text
print(result.text)