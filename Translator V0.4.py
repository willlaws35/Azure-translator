#disclaimer, I need to clear up the comments, but for now theyre a good laugh while trying not to lose you're mind
#-----------------------------------------------------------------------------------------------------------------------
#purely added this line to get to 250 lines, what can i say round numbers are just fun.



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

#for MP3 to WAV converter if needs be...
#---------------------------------------
#from os import path
#from pydub import AudioSegment


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

#not so fun functions
#-----------------------------------------------------------------------------------------------------------------------


# function to get direct file name maybe needed for MP3 to WAV converter
#-----------------------------------------------------------------------------------------------------------------------
#def FNameOnly(file):
 #   temp_file = file.split('/')
  #  term = (len(temp_file))-1
   # out_file = temp_file[term]
    #print(out_file)
    #Mp3Wav(out_file)

#MP3 to WAV converter but "it did a broke" can't seem to recognise any file path ever
#-----------------------------------------------------------------------------------------------------------------------
#def Mp3Wav(file):
 #   input_file = file
  #  output_file = input_file + ".wav"
   # sound = AudioSegment.from_mp3(input_file)
    #sound.export(output_file, format = "wav")
    #Azure(output_file)




#-----------------------------------------------------------------------------------------------------------------------
#actual translation stuff mucho importante, however has a bug where it doesnt return whole line, maybe training ???

# ight so had a bit of a brain cell moment, what if we need to divide the file and have multiple smaller conversions
# then return the values a chunk at a time, that way it would be forced to provide output?

#but this then brings into question how do we know how long the snippets are, like is it routinely the same amount of time
#or not, and well it isnt the same amount of time so i have no fucking idea and this is a waste of space argghhghghghghghg
#-----------------------------------------------------------------------------------------------------------------------
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

    #recognizer = the bastard line of the day
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)

    #it works but not with mp3 ???????, oh what joys apparently something to do with comprhesion rates between 8 and 16 khz
    #dont expect me to know that what stack overflow is for.

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print ("recognized: ", result.text)
        print ("German: ", result.translations['de'])
        Origins.append(result.text)
        Translations.append(result.translations['de'])
        TextReadInOrigins(Origins[0])
        TextReadInTranslations(Translations[0])

    #error catching chonk however when the whole program is an error do you really need it ?
    #-------------------------------------------------------------------------------------------------------------------

    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
       print("Translation canceled: {}".format(result.cancellation_details.reason))
    elif result.cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(result.cancellation_details.error_details))

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

    window = sg.Window('Translator V0.5', layout, size=(565,300))

    #version plans because planning ....?
    #-------------------------------------------------------------------------------------------------------------------
    #V0.1 = initial program window
    #V0.2 = text feedback and audio replay
    #V0.3 = *hopefully* help function and azure integration
    #V0.4 = should be azure integration like fuck that happening at V0.3
    #V0.5 = I said integrartion, never meant it was going to be good, so V0.5 get good newb
    #V0.6 = full integrationa and translation rather than partial translation because the microsofts dont like musics.
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
            Azure(filename)
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

#supposed to snippet audio, needs a dynamic function to appropriately size snippets,
# and oh yeah kind of needs to god damn work...
#-----------------------------------------------------------------------------------------------------------------------

#def AudioSep():
 #   w = wave.open(r"C:\Users\willi\Downloads\[ONTIVA.COM] Tonight on Bottom Gear-128k.wav",'r')
  #  start = 0
   # end = 30
    #duration = liborsa.get_distribution(w)
#
 #   segmentsnum = duration/30
  #  remainder = duration % 30
#
 #   x=0
  #  for x in range(int(segmentsnum)):
   #     with wave.open(w) as infile:
    #        nchannels = infile.getnchannels()
     #       sampwidth = infile.getsampwidth()
      #      framerate = infile.getframerate()
       #     infile.setpos(int(start * framerate))
        #    data = infile.readframes(int((end - start)*framerate))
        #with wave.open((file+str(x)+'.wav'),'w')as outfile:
         #   outfile.setnchannels(nchannels)
          #  outfile.setsampwidth(sampwidth)
           # outfile.setframerate(framerate)
            #outfile.setnframes(int(len(data) / sampwidth))
            #outfile.outfile.writeframes(data)
        #start += 30
        #end += 30

        #if (remainder > 0):
         #   end -= 30
          #  x += 1
           # end += remainder
            #with wave.open(w, "rb") as infile:
                # get file data
             #   nchannels = infile.getnchannels()
              #  sampwidth = infile.getsampwidth()
               # framerate = infile.getframerate()
                # set position in wave to start of segment
                #infile.setpos(int(start * framerate))
                # extract data
                #data = infile.readframes(int((end - start) * framerate))

            # write the extracted data to a new file
            #with wave.open(('my_out_file' + str(x) + '.wav'), 'w') as outfile:
             #   outfile.setnchannels(nchannels)
              #  outfile.setsampwidth(sampwidth)
               # outfile.setframerate(framerate)
                #outfile.setnframes(int(len(data) / sampwidth))
                #outfile.writeframes(data)

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



#below is an absolute cluster-fuck but works perfectly, need to add a custom file finder but other than that dont breathe on the fucker.
#currently has a direct path, however should be able to utilise the text result directly from azure once it decides to get it's shit together
#-----------------------------------------------------------------------------------------------------------------------

def TextReadInOrigins(text):
    TextLen = []
    LineMaker = ""
    TextChunk = text
    TextLen = TextChunk.split()
    for i in range(len(TextLen)):
        if len(LineMaker)<60:
            LineMaker = LineMaker+TextLen[i]+" "
        elif len(LineMaker)>=60:
            OriginsSplit.append(LineMaker)
            LineMaker = " "

def TextReadInTranslations(text):
    TextLen = []
    LineMaker = ""
    TextChunk = text
    TextLen = TextChunk.split()
    for i in range(len(TextLen)):
        if len(LineMaker)<60:
            LineMaker = LineMaker+TextLen[i]+" "
        elif len(LineMaker)>=60:
            TranslationsSplit.append(LineMaker)
            LineMaker = " "


#main bit, bit pathetic if were going to be honest with ourselves, even text read in is going to be internalised in add file,
#oh well, might shift some variables here to make it feel less lonely.
#-----------------------------------------------------------------------------------------------------------------------
while ProgramShut == True:
    addfile()