#disclaimer, I need to clear up the comments, but for now theyre a good laugh while trying not to lose you're mind
#-----------------------------------------------------------------------------------------------------------------------

#hey you know how fun installing libraries are right ?.... so kind of need every one of these or the program will become a black hole
#easiest way to install is simply go to cmd and typr "pip install" then the library so for the first one
# "pip install azure-cognitiveservices-speech" could probably automate this but nah I've had enough
#-----------------------------------------------------------------------------------------------------------------------
import azure.cognitiveservices.speech as speechsdk
import PySimpleGUI as sg
import winsound
import librosa
import wave
import json
import os
from playsound import playsound


#theme set for alternatives: https://www.geeksforgeeks.org/themes-in-pysimplegui/
sg.theme('DarkGrey6')

#some variables which need to be moved, but where ?  i havent decided yet magic man
FileList = []
Origins = []
Translations = []
OriginsSplit = []
TranslationsSplit = []

SplitPoint = 0
TempAzure = ' '
LangFrom = ["ENG","GER","FRA"]
LangTo = ["ENG","GER","FRA"]
ProgramShut = True

def TextReadInOrigins():
    OriginsComp = ""
    temp_1 = len(Origins)
    temp_2 = 0
    while (temp_2 < temp_1):
        OriginsComp = str(OriginsComp) + str(Origins[temp_2])
        temp_2 = temp_2 + 1
    TextLen = []
    LineMaker = ""
    TextChunk = OriginsComp
    TextLen = TextChunk.split()
    for i in range(len(TextLen)):
        if len(LineMaker)<60:
            LineMaker = LineMaker+TextLen[i]+" "
        elif len(LineMaker)>=60:
            OriginsSplit.append(LineMaker)
            LineMaker = " "

def TextReadInTranslations():
    TranslationsComp = ""
    temp_1 = len(Translations)
    temp_2 = 0
    while (temp_2 < temp_1):
        TranslationsComp = str(TranslationsComp) + str(Translations[temp_2])
        temp_2 = temp_2 +1
    TextLen = []
    LineMaker = ""
    TextChunk = TranslationsComp
    TextLen = TextChunk.split()
    for i in range(len(TextLen)):
        if len(LineMaker)<60:
            LineMaker = LineMaker+TextLen[i]+" "
        elif len(LineMaker)>=60:
            TranslationsSplit.append(LineMaker)
            LineMaker = " "

def Azure(file):
    audiofile = file
    speech_key, service_region = 'bc26117a081546a8ab8accfc840bed51', 'uksouth'

    #do something for the love of christ

    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)
    speech_recognition_language = 'en-GB'
    target_languages = 'de'

    translation_config.speech_recognition_language = speech_recognition_language
    translation_config.add_target_language(target_languages)
    audio_config = speechsdk.audio.AudioConfig(filename=audiofile)
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    def result_callback(event_type, evt):
        TranslationsRecord = ""
        TranslationsRec = ""
        print("running...")
        Origins.append(evt.result.text)
        TranslationsRec = evt.result.translations.items()
        TranslationsRecord = TranslationsRec[0]
        Translations.append(TranslationsRecord[1])
    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # connect callback functions to the events fired by the recognizer
    recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # event for final result
    recognizer.recognized.connect(lambda evt: result_callback('RECOGNIZED', evt))
    # cancellation event
    recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt, evt.reason)))

    # stop continuous recognition on either session stopped or canceled events
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)
    # start translation
    recognizer.start_continuous_recognition()

    while not done:
        sg.time.sleep(.5)

    recognizer.stop_continuous_recognition()
#essentially main, issues a plenty here, mainly file management via the drop down list but I'll just pretend I dont see it
#-----------------------------------------------------------------------------------------------------------------------
def addfile():
    WinRun = True
    layout = [[sg.Text('File:', size=4), sg.Input(key='_In_', do_not_clear=False), sg.FileBrowse(), sg.Submit(key = 'Submit'), sg.Button("Play")],
              [sg.Text("Files:"), sg.Combo(FileList, size = 67, key = '_Output_')],
              [sg.Text('')],
              [sg.Text("Origin feedback:"), sg.Combo(OriginsSplit, size = 58)],
              [sg.Text("Translation feedback:"), sg.Combo(TranslationsSplit, size=54)],
              [sg.Text('')],
              [sg.Text("Origin Language:       "), sg.Combo(LangFrom, size=10)],
              [sg.Text("Conversion Language:"), sg.Combo(LangTo, size=10)],
              [sg.Text('')],
              [sg.Button("Help")]]

    layout_1 = [[sg.Text("")],
                [sg.Text("")],
                [sg.Text("")],
                [sg.Text("Processing... please wait.")],
                [sg.Text("If the translation time is high, this may be due to high traffic or poor internet connection.")],
                [sg.Text("Pleae be patient as this may take up to five minutes.")]]

    window = sg.Window('Translator V0.6', layout, size=(565,300))

    #version plans because planning ....?
    #-------------------------------------------------------------------------------------------------------------------
    #V0.1 = initial program window
    #V0.2 = text feedback and audio replay
    #V0.3 = *hopefully* help function and azure integration
    #V0.4 = should be azure integration like fuck that happening at V0.3
    #V0.5 = I said integrartion, never meant it was going to be good, so V0.5 get good newb
    #V0.6 = full integration and translation rather than partial translation because the microsofts dont like musics.
    #V0.7 = audio seperation and UI testing
    #

    event, values = window.read()
    filename = values['_In_']
    while WinRun == True:
        if event == sg.WINDOW_CLOSED:
            exit(0)
        if event == 'Submit':
            window['_Output_'].update(filename)
            print(filename)
            FileList.append(filename)
            #window_1 = sg.Window('Translator V0.5', layout_1, size=(565, 300))
            #window_1.open()
            Azure(filename)
            TextReadInOrigins()
            TextReadInTranslations()
            WinRun = False
            window.close()
        event, values = window.read()
        if event == 'Play':
            player(filename)

            #Audio sep for file snippets however it is also doing a broke, blame brandon for that one,
            # or don't I'm not the boss of you
            #-----------------------------------------------------------------------------------------------------------
            #AudioSep(filename)

            TempAzure = Azure(filename)
            print(TempAzure)
            WinRun = False
            window.close()
        if event == 'Help':
            HelpingHand()


#this is stupid now, but may be better once the audio seperation works, or not idfk at this point
#-----------------------------------------------------------------------------------------------------------------------
def player(file):
    playsound(file)

#as amazing as this would be, please for the love of christ change the help to be helpful,
#no one in business appreciates humour anymore.
#-----------------------------------------------------------------------------------------------------------------------
def HelpingHand():
    #do some fucking shit
    layout = [[sg.Text('Look imma be straight with you,')],
              [sg.Text('What on Gods green earth are you stuck on')],
              [sg.Text('like if its a bug fair enough, you get what')],
              [sg.Text('you pay for, but other than that what do you want')],
              [sg.Text('seriously pop your question in google translate')],
              [sg.Text('get your answer then go touch some grass')],
              [sg.Text('*actual reminder, for the love of christ change this*')]]
    window = sg.Window('Help',layout,size = (325,190))
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        window.close()

#main bit, bit pathetic if were going to be honest with ourselves, even text read in is going to be internalised in add file,
#oh well, might shift some variables here to make it feel less lonely.
#-----------------------------------------------------------------------------------------------------------------------
while ProgramShut == True:
    addfile()