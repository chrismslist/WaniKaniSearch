# intialize WaniKani API
from wanikani_api.client import Client

#Import Libraries
from colored import fg, bg, attr #Import Colored Library
import os #Import OS Library
import sys #Import SYS Library
import jaconv
from wanikani_api.models import Assignment #import Japanese Conversion tool

#Clear Console
os.system('cls')

#Get account from API Key
v2_api_key = "be14ad6f-4754-4f0c-bf13-9dea954af506" # You can get it here: https://www.wanikani.com/settings/account

#Set api key to client
client = Client(v2_api_key)

#Set global variables
#use dict value to store variables?


#Try to get client information
try:
    user_information = client.user_information()
except:
    print("%sUnable to Connect / Incorrect Wanikani API Key! Program Terminated!%s" % (fg(1), attr(0)))
    sys.exit()

#Simplify Variables
userName = user_information.username
userLevel = user_information.level 
userProfile = user_information.profile_url
userStarted = user_information.started_at

#Print User Infromation from API Personal Profile
print("%sUser Information: \nUsername: %s" % (fg(1), attr(0))+
    userName+"\n%sLevel:%s "  % (fg(2), attr(0))+
    str(userLevel)+"\n%sProfile Url:%s " % (fg(3), attr(0))+
    userProfile+"\n%sStart Date:%s " % (fg(4), attr(0))+
    str(userStarted)) 

def loadDatabase(): #Get and Save All WaniKani Data from API
    
    #Load Local Database and check if avaliable
    #load()

    global vocabulary
    global radicals
    global kanji

    print(" ")
    print("Loading WaniKani Database (This may take a minute)...")
    #Load all WaniKani Information
    vocabulary = client.subjects(types="vocabulary", fetch_all=True)
    print("-Vocab Loaded-")
    radicals = client.subjects(types="radical", fetch_all=True)
    print("-Radicals Loaded-")
    kanji = client.subjects(types="kanji", fetch_all=True)
    print("-Kanji Loaded-")

    print(" ")
    print("Total Vocabulary: "+str(len(vocabulary)))
    print("Total Radicals: "+str(len(radicals)))
    print("Total Kanji: "+str(len(kanji)))

    #save()
    

'''
def load(): #load and create file to memory
    try:
        os.chdir("C:\\WaniKaniData")
    except FileNotFoundError:
        os.chdir("C:\\")
        os.mkdir("WaniKaniData")
        os.chdir("C:\\WaniKaniData")
        print("Sys: Folder Not Found: ReWritten and Set Default")

    global saved_radicals
    global saved_vocabulary
    global saved_kanji
    global file_vocabulary
    global file_kanji
    global file_radicals

    global files

    try:
        file_vocabulary = open("vocabulary.txt","r+")
    except FileNotFoundError:
        file_vocabulary = open("vocabulary.txt","w+")
        print("Sys: Vocabulary File Missing: ReWritten")
        load()
    try:
        file_radicals = open("radicals.txt","r+")
    except FileNotFoundError:
        file_radicals = open("radicals.txt","w+")
        print("Sys: Radical File Missing: ReWritten")
        load()

    try:
        file_kanji = open("kanji.txt","r+")
    except FileNotFoundError:
        file_kanji = open("kanji.txt","w+")
        print("Sys: Kanji File Missing: ReWritten")
        load()

    files = os.listdir()

    saved_vocabulary = file_vocabulary.read().splitlines()
    saved_kanji = file_kanji.read().splitlines()
    saved_radicals = file_radicals.read().splitlines()

    #team_combined = [[team_nums],[team_names]]

    return
'''

'''
def rewrite(): #rewrite files when new information is added


    #global file_vocabulary
    #global file_kanji
    #global file_radicals


    try:
        file_vocabulary = open("vocabulary.txt","r+")
    except FileNotFoundError:
        file_vocabulary = open("vocabulary.txt","w+")
        rewrite()
    try:
        file_radicals = open("radicals.txt","r+")
    except FileNotFoundError:
        file_radicals = open("radicals.txt","w+")
        rewrite()
    try:
        file_kanji = open("kanji.txt","r+")
    except FileNotFoundError:
        file_kanji = open("kanji.txt","w+")
        rewrite()

    return
'''

'''
def save(): #write all WaniKani Data and numbers to local file

    file_vocabulary.close()
    file_kanji.close()
    file_radicals.close()

    os.remove("vocabulary.txt")
    os.remove("radicals.txt")
    os.remove("kanji.txt")

    rewrite()

    saved_radicals=radicals
    #saved_kanji=kanji
    saved_vocabulary=vocabulary


    for vocab in saved_vocabulary:
        file_vocabulary.write("%s\n" % vocab)
    for kanji in saved_kanji:
        file_kanji.write("%s\n" % kanji)
    for radical in saved_radicals:
        file_radicals.write("%s\n" % radical)


    file_vocabulary.close()
    file_kanji.close()
    file_radicals.close()

    load()#reloads all variables in local file

    mainLoop()#returns to start of program state
'''

def mainLoop(): #Main Loop of the Program, Where User Performs Specified Actions

    action = input("Type an Action: ")
    
    #List all Vocab from Database
    if action =="list":
        for vocab in vocabulary:
            for vocab in vocabulary:
                print(vocab)

    #Search for Meaning in Hiragana
    if action =="search for meaning":
        search_word = input("Enter Reading in Romaji: ")
        searchKana = jaconv.alphabet2kana(search_word)
        print("%s--Search Results--%s" % (fg(1), attr(0)))
        for vocab in vocabulary:
            #print(vocab.readings[0].reading)
            if searchKana in vocab.readings[0].reading:
                print(vocab.readings[0].reading+"%s: %s"% (fg(3), attr(0))+vocab.meanings[0].meaning)

    #Search for Reading in English
    if action =="search for reading":
            print("Warning: Case Sensitive")
            search_word = input("Enter Meaning in English: ")
            print("%s--Search Results--%s" % (fg(1), attr(0)))
            for vocab in vocabulary:
                if search_word in vocab.meanings[0].meaning:
                    print(vocab.meanings[0].meaning+"%s: %s"% (fg(3), attr(0))+vocab.readings[0].reading )

    #List Current Vocab for User's Level
    if action=="list current vocab": 
        subjects = client.subjects(types=["vocabulary"], levels=userLevel)
        print("")
        print("%s--Reading, Meaning--%s" % (fg(1), attr(0)))
        for subject in subjects:
            try: print(subject.readings[0].reading+"%s: %s"% (fg(3), attr(0))+subject.meanings[0].meaning)
            except: print('Unknown // Type Error')
        
        """
        assignments = client.assignments(subject_types="vocabulary")
        print("Total Vocab:"+str(len((assignments))))
        print("SRS Level, Reading, Word (English)")
        for assignment in assignments:
            try: print(assignment.srs_stage,  assignment.subject.readings[0].reading, assignment.subject.meanings[0].meaning)
            except: print('Unknown // Type Error')
        """

    #List Current Kanji for User's Level
    if action=="list current kanji": 
        subjects = client.subjects(types=["kanji"], levels=userLevel)
        print("")
        print("%s--Reading, Meaning--%s" % (fg(1), attr(0)))
        for subject in subjects:
            print(subject.readings[0].reading+"%s: %s"% (fg(3), attr(0))+subject.meanings[0].meaning)
    
    #List Current Radicals for User's Level
    if action=="list current radicals": 
        subjects = client.subjects(types=["radical"], levels=userLevel)
        print("")
        print("%s--Reading, Meaning--%s" % (fg(1), attr(0)))
        for subject in subjects:
            try: print(subject.characters+"%s: %s"% (fg(3), attr(0))+subject.meanings[0].meaning)
            except: print('Unknown // Type Error')
        
    mainLoop() #Go Back to Top of Function

#loadDatabase() #Load Latest WaniKani Data
mainLoop() #Run main program loop