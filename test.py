import azure.cognitiveservices.speech as speechsdk
import time
import json
Language_Get = "Unknown"
running = True

def synthesis_callback(evt):
    """
    callback for the synthesis event
    """
    print('SYNTHESIZING {}\n\treceived {} bytes of audio. Reason: {}'.format(
        evt, len(evt.result.audio), evt.result.reason))
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("RECOGNIZED: {}".format(evt.result.properties))
        if evt.result.properties.get(
                speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult) == None:
            print("Unable to detect any language")
        else:
            detectedSrcLang = evt.result.properties[
                speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
            jsonResult = evt.result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult]
            detailResult = json.loads(jsonResult)
            startOffset = detailResult['Offset']
            duration = detailResult['Duration']
            if duration >= 0:
                endOffset = duration + startOffset
            else:
                endOffset = 0
            print("Detected language = " + detectedSrcLang + ", startOffset = " + str(
                startOffset) + " nanoseconds, endOffset = " + str(endOffset) + " nanoseconds, Duration = " + str(
                duration) + " nanoseconds.")
            global language_detected
            language_detected = True

def result_callback(event_type, evt):
      """callback to display a translation result"""
      DataBack = ""
      print(evt.result.text)
      DataBack = (evt.result.json)
      DataBack = DataBack.split('"')
      print(DataBack[39])
      if DataBack[39] != "Unknown":
            Language_Get = DataBack[39]
            return

def stop_cb(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    done = True

def testing():

    speech_key, service_region = "bc26117a081546a8ab8accfc840bed51", "uksouth"
    weatherfilename = "C:\\Users\\willi\\Downloads\\Der Grüffelo.wav"

    # Currently the v2 endpoint is required. In a future SDK release you won't need to set it.
    endpoint_string = "wss://{}.stt.speech.microsoft.com/speech/universal/v2".format(service_region)
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key,endpoint=endpoint_string,speech_recognition_language='en-GB',target_languages=('en-GB'))
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority,value='Accuracy')
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig \
        (languages=["en-US", "de-DE", 'en-GB'])
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config,audio_config=audio_config,auto_detect_source_language_config=auto_detect_source_language_config)

    done = False
    recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    if Language_Get != "Unknown":
        exit(0)
    recognizer.recognizing.connect(lambda evt: result_callback('RECOGNIZING', evt))
    recognizer.recognized.connect(lambda evt: result_callback('RECOGNIZED', evt))
    recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt, evt.reason)))
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)
    recognizer.synthesizing.connect(synthesis_callback)
    recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    recognizer.stop_continuous_recognition()

#-----------------------------------------------------------------------------------------------------------------------
testing()
print("ended")