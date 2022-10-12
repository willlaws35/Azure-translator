#disclaimer, I need to clear up the comments, but for now theyre a good laugh while trying not to lose you're mind
#-----------------------------------------------------------------------------------------------------------------------

#hey you know how fun installing libraries are right ?.... so kind of need every one of these or the program will become a black hole
#easiest way to install is simply go to cmd and typr "pip install" then the library so for the first one
# "pip install azure-cognitiveservices-speech" could probably automate this but nah I've had enough
#-----------------------------------------------------------------------------------------------------------------------
import azure.cognitiveservices.speech as speechsdk
import PySimpleGUI as sg
import winsound, librosa, wave, json, time, os, shutil
from playsound import playsound

#theme set for alternatives: https://www.geeksforgeeks.org/themes-in-pysimplegui/


#some variables which need to be moved, but where ?  I haven't decided yet magic man!
FileList = []
Origins = []
Translations = []
OriginsSplit = []
TranslationsSplit = []

SplitPoint = 0
theme_set = 0
theme_set_back_up = 0
Language_Get = "TEMP"
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
            LineMaker = LineMaker+TextLen[i]+" "

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
            LineMaker = LineMaker+TextLen[i]+" "

#---------------------------------------------------------------------------------------------------------------------------

def Azure(file):
    audiofile = file
    speech_key, service_region = 'bc26117a081546a8ab8accfc840bed51', 'uksouth'
    endpoint_string = "wss://{}.stt.speech.microsoft.com/speech/universal/v2".format(service_region)
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key,
        endpoint=endpoint_string,
        speech_recognition_language='de-DE',
        # so this is where the error is caused for some reason it wont translate
        # to just english it will only allow multiple languages
        target_languages=('en', 'fr'))
    audio_config = speechsdk.audio.AudioConfig(filename=audiofile)

    # Set the Priority (optional, default Latency, either Latency or Accuracy is accepted)
    translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority,
                                    value='Accuracy')

    # Specify the AutoDetectSourceLanguageConfig, which defines the number of possible languages
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["en-GB", "de-DE", "zh-CN", "fr-FR"])

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        audio_config=audio_config,
        auto_detect_source_language_config=auto_detect_source_language_config)

    def result_callback(event_type, evt):

        print("{}: {}\n\tTranslations: {}\n\tResult Json: {}".format(
            event_type, evt, evt.result.translations.items(), evt.result.json))
        TranslationsRecord = ""
        TranslationsRec = ""
        print("running...")
        if (evt.result.text == " "):
            Origins.append(" ")
        else:
            Origins.append(evt.result.text)
        TranslationsRec = evt.result.translations.items()
        TranslationsRecord = TranslationsRec[0]
        if (TranslationsRecord[1] == " "):
            Translations.append(" ")
        else:
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
def addfile(theme_set):
    temp_theme_set = theme_set
    if theme_set == 0:
        sg.theme('SystemDefault')
    if theme_set == 1:
        sg.theme('DarkGrey6')
    # dark mode theme = DarkGrey6
    # light mode theme = LightGrey6... i think
    WinRun = True
    layout = [[sg.Text('File:', size=4), sg.Input(key='_In_', do_not_clear=False), sg.FileBrowse(), sg.Submit(key = 'Submit'), sg.Button("Play")],
              [sg.Text("Files:"), sg.Combo(FileList, size = 67, key = '_Output_')],
              [sg.Text('')],
              [sg.Text("Origin feedback:"), sg.Combo(OriginsSplit, size = 58)],
              [sg.Text("Translation feedback:"), sg.Combo(TranslationsSplit, size=54)],
              [sg.Text('')],
              [sg.Button("Change Theme"), sg.Button("Help")]]
    #Don't you just love this formatting *chef's kiss*
    layout_1 = [[sg.Text("                                                Waiting to begin processing...")],
                [sg.Text("                                       Translation time can sometimes be high, ")],
                [sg.Text("       this may be due to high traffic, poor internet connection, or due to large file sizes.")],
                [sg.Text("                              Please be patient as this may take up to ten minutes.")],
                [sg.Text("")],
                [sg.Text("                                      Are you sure you want to begin translation ?")],
                [sg.Text("                                                        "),sg.Button("Yes"), sg.Button("No")]]

    window = sg.Window('Translator V0.9', layout, size=(565,215))
    window_1 = sg.Window('Translator V0.9', layout_1, size=(565,215))

    #version plans because planning ....?
    #-------------------------------------------------------------------------------------------------------------------
    #V0.1 = initial program window
    #V0.2 = text feedback and audio replay
    #V0.3 = *hopefully* help function and azure integration
    #V0.4 = should be azure integration like fuck that happening at V0.3
    #V0.5 = I said integrartion, never meant it was going to be good, so V0.5 get good newb
    #V0.6 = full integration and translation rather than partial translation because the microsofts dont like musics.
    #V0.7 = UI testing-ish and dark/light mode
    #V0.75 = Language specifications getting there but issue with azure sessions needs to be resolved.
    #V0.8 = Language specification
    #V0.9 = audio seperation integration
    #V1.0 = completed initial prototype

    while WinRun == True:
        event, values = window.read()
        filename = values['_In_']
        if event == sg.WINDOW_CLOSED:
            exit(0)
        if event == 'Submit':
            window['_Output_'].update(filename)
            FileList.append(filename)
            window_1.read()
            event_1, values_1 = window_1.read()
            if event_1 == 'Yes':
                #translations and text processing
                splitaudio(FileList[(len(FileList))-1])
                Azure(FileList[(len(FileList))-1])
                TextReadInOrigins()
                TextReadInTranslations()
                window_1.close()
                WinRun = False
                T = open('Translations.txt', 'w')
                for i in range (len(Translations)):
                     T.write(Translations[i])
                T.write("----------------------------------------------------------------------------------------")
                T.close()
                O = open('Origins.txt', 'w')
                for i in range (len(Origins)):
                    O.write(Origins[i])
                O.write("----------------------------------------------------------------------------------------")
                O.close()
                window.close()
            if event_1 == 'No':
                window_1.close()
            if event_1 == sg.WINDOW_CLOSED:
                window_1.close()
        event, values = window.read()

        if event == 'Play':
            player(filename)
            #insert audio seperation
            WinRun = False
            window.close()

        if event == 'Change Theme':
            print("pre change set", theme_set)
            if theme_set == None:
                theme_set = theme_set_back_up
            if theme_set == 0:
                theme_set = 1
            elif theme_set == 1:
                theme_set = 0
            print("post change set", theme_set)
            window.close()
            return theme_set

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
    layout = [[sg.Text('Program Guide: ')],
              [sg.Text('To Use the Translator, use the browse function')],
              [sg.Text('to select your WAV file of choice, then return')],
              [sg.Text('to the main program screen.')],
              [sg.Text('Select the submit button and confirm to start')],
              [sg.Text('the translation. Wait for the process')],
              [sg.Text('to be completed. (This may take some time.)')]]
    window = sg.Window('Help',layout,size = (325,190))
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        window.close()

def splitaudio(filepath):
    splitaudiopath = 'splitaudio/'
    try:
        os.mkdir('splitaudio')
    except FileExistsError:
        splitaudiopath = 'splitaudio/'
    location = filepath  ## unable to find where your filelocation is provided so just parse it through to here
    print(location)
    start = 0  # seconds
    end = 10  # seconds
    duration = librosa.get_duration(filename=location)
    segmentsnum = duration / 10
    remainder = duration % 10
    x = 0
    for x in range(int(segmentsnum)):
        # file to extract the snippet from
        with wave.open(location, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((end - start) * framerate))

        # write the extracted data to a new file
        with wave.open((splitaudiopath + 'part' + str(x) + '.wav'), 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)
        start += 10
        end += 10

    if (remainder > 0):
        end -= 10
        x += 1
        end += remainder
        with wave.open(location, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((end - start) * framerate))

        # write the extracted data to a new file
        with wave.open((splitaudiopath + 'part' + str(x) + '.wav'), 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)

while ProgramShut == True:
    if theme_set == None:
        theme_set = 0
        theme_set_back_up = theme_set
    theme_set = addfile(theme_set)
