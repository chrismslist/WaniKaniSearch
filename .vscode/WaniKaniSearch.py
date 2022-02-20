# intialize WaniKani API
from re import search
from wanikani_api.client import Client

#Import Libraries
from colored import fg, bg, attr #Import Colored Library
import os #Import OS Library
import sys #Import SYS Library
import jaconv #Import US to Kana converter Library
from wanikani_api.models import Assignment #import Japanese Conversion tool
import json #import json Library


#Clear Console
os.system('cls')

#Get account from API Key
v2_api_key = "be14ad6f-4754-4f0c-bf13-9dea954af506" # You can get it here: https://www.wanikani.com/settings/account

#Set api key to client
client = Client(v2_api_key)

#Set global variables
previousCommand = []
iteration = 0

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
    print(" ")

    #save()
    


"""
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

    files = os.listdir()
    
    return

def rewrite(): #rewrite files when new information is added


    global file_vocabulary
    global file_kanji
    global file_radicals


    try:
        file_vocabulary = open("vocabulary.json","r+")
    except FileNotFoundError:
        file_vocabulary = open("vocabulary.json","w+")
        rewrite()
    try:
        file_radicals = open("radicals.json","r+")
    except FileNotFoundError:
        file_radicals = open("radicals.json","w+")
        rewrite()
    try:
        file_kanji = open("kanji.json","r+")
    except FileNotFoundError:
        file_kanji = open("kanji.json","w+")
        rewrite()

    return

def save(): #write all WaniKani Data and numbers to local file
    
    saved_radicals={}
    saved_kanji=kanji
    saved_vocabulary=vocabulary


    for item in radicals:
            saved_radicals.update({item.characters: item.meanings[0].meaning})

    # create json object from dictionary
    json = json.dumps(saved_radicals)

    # open file for writing, "w" 
    f = open("radicals.json","w")

    # write json object to file
    f.write(json)

    # close file
    f.close()

    rewrite()

    

    #file_kanji.writerow([radicals.subject, val])
    #file_radicals.writerow([key, val])

    file_vocabulary.close()
    file_kanji.close()
    file_radicals.close()

    load()#reloads all variables in local file


    mainLoop()#returns to start of program state
"""

#Function to print more info on a term, takes parameters for the search term, and the type of term (radical, vocabulary, kanji)
def printMoreInfo(searchTerm, type):
    if type == 'radical':
        subjects = client.subjects(types=["radical"], levels=userLevel)
        print("")
        print("%s--More Information--%s" % (fg(1), attr(0)))
        print('Selected Radical: '+searchTerm)
        print('Name: ')
        print(subjects.meanings[0].meaning)
    else:
        return
        

def mainLoop(): #Main Loop of the Program, Where User Performs Specified Actions
    #Def Global Vars in the Function
    global listedPrevious
    global previousCommand
    global iteration
    
    if iteration==2:
        previousCommand=[]
    
    #Prompt user for Action
    action = input("%sType an Action: %s" % (fg(2), attr(0)))
    
    #Reset / Define Count Variables
    count=0
    num = []
    #List all Vocab from Database
    if "list vocab" in action:
        try: num = [int(s) for s in action.split() if s.isdigit()]
        except IndexError: num[0] = -1
        
        #If length of list from input is zero, means no numbers have been entered, so set vals to zero to avoid error
        if len(num)==0:
            num = [0,0]
            num[0] = 1000000000
        
        print("%s--Kanji: Reading, Meaning--%s" % (fg(1), attr(0)))
        
        #Print vocab for loop, prints all vocab unless number specified
        for vocab in vocabulary:
            count+=1
            print(str(count)+". "+vocab.characters+"%s: %s"% (fg(3), attr(0))+vocab.readings[0].reading+", "+vocab.meanings[0].meaning)
            if count>=num[0]:
                break

    #Search for Meaning in Hiragana
    if action =="search for vocab meaning":
        
        #Prompt for input reading in romaji
        search_word = input("Enter Reading in Romaji: ")
        
        #Convert alphabet to kana using api
        searchKana = jaconv.alphabet2kana(search_word)

        print("%s--Search Results--%s" % (fg(1), attr(0)))
        print("%s--Kanji: Reading, Meaning--%s" % (fg(1), attr(0)))
        count=0
        for vocab in vocabulary:
            #print(vocab.readings[0].reading)
            if searchKana in vocab.readings[0].reading:
                count+=1
                print(str(count)+". "+vocab.characters+"%s: %s"% (fg(3), attr(0))+vocab.readings[0].reading+", "+vocab.meanings[0].meaning)

    #Search for Reading in English
    if action =="search for vocab reading":
            print("Warning: Case Sensitive")
            search_word = input("Enter Meaning in English: ")
            print("%s--Search Results--%s" % (fg(1), attr(0)))
            print("%s--Meaning: Reading, Kanji--%s" % (fg(1), attr(0)))
            count=0
            for vocab in vocabulary:
                if search_word in vocab.meanings[0].meaning:
                    count+=1
                    print(str(count)+". "+vocab.meanings[0].meaning+"%s: %s"% (fg(3), attr(0))+vocab.readings[0].reading+", "+vocab.characters)

    #List Current Vocab for User's Level
    if action=="list current vocab": 
        subjects = client.subjects(types=["vocabulary"], levels=userLevel)
        print("")
        print("%s--Reading, Meaning--%s" % (fg(1), attr(0)))
        count = 0
        for subject in subjects:
            count+=1
            try: print(str(count)+". "+subject.readings[0].reading+"%s: %s"% (fg(3), attr(0))+subject.meanings[0].meaning)
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
        print("%s--Kanji: Reading, Meaning--%s" % (fg(1), attr(0)))
        count = 0
        for subject in subjects:
            count+=1
            print(str(count)+". "+subject.characters+"%s: %s"% (fg(3), attr(0))+subject.readings[0].reading+", "+subject.meanings[0].meaning)
    
    #List Current Radicals for User's Level
    if action=="list current radicals": 
        subjects = client.subjects(types=["radical"], levels=userLevel)
        print("")
        print("%s--Reading, Meaning--%s" % (fg(1), attr(0)))
        count = 0
        listedPrevious = {}
        for subject in subjects:
            count+=1
            try: print(str(count)+". "+subject.characters+"%s: %s"% (fg(3), attr(0))+subject.meanings[0].meaning)
            except: print('Unknown // Type Error')
            listedPrevious.update({count: subject.characters})

    #Get more information based on Number from List User Selects
    #Keep at bottom of actions this applies to
    if "select" in action:
        num = []
        try: num = [int(s) for s in action.split() if s.isdigit()]
        except IndexError: num[0] = 1
        
        print(num)
        print(listedPrevious)
        
        selected = listedPrevious[num[0]]
        if 'radical' in previousCommand[0]:
            printMoreInfo(selected, "radical")
            
    if action =='help':
        print('Help')
            
            
    previousCommand.append(action)
    iteration+=1
    
       
    mainLoop() #Go Back to Top of Function

#loadDatabase() #Load Latest WaniKani Data
mainLoop() #Run main program loop