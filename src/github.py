#!/usr/bin/env python3
# Light drizzle, mist 🌦   🌡️+49°F (feels +47°F, 90%) 🌬️←7mph 🌒 Wed May  4 05:26:13 2022
# Overcast ☁️   🌡️+34°F (feels +32°F, 75%) 🌬️↘4mph 🌓 Tue Nov 29 08:56:35 2022


import requests
import json
from datetime import date
import time
import sys
import os
import json
from config import CACHE_FOLDER, CACHE_FOLDER_IMAGES, HISTORY_FOLDER, QUICKLOOK_PREF, HISTORY_FILE

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)



def checkingTime ():
## Checking if the database needs to be built or rebuilt
    timeToday = time.time()
    if not os.path.exists(HISTORY_FILE):
        log ("History File missing ... building")
        myGitHistory = {}
        myGithubHub, myURLs = FetchGithub (username,token,myGitHistory)
    else: 
        databaseTime= (int(os.path.getmtime(HISTORY_FILE)))
        time_elapsed = int((timeToday-databaseTime)/86400)
        log (str(time_elapsed)+" days from last update")
        if time_elapsed >= refRate:
            log ("rebuilding database ⏳...")
               # Loading the JSON history file
            f = open(HISTORY_FILE)
            myGitHistory = json.load(f)
            f.close()

            FetchGithub (username,token, myGitHistory)
            log ("done 👍")
            #return "toBeUpdated"
    
    
####################
# inputs          ##
####################
username = os.getenv("myUsername")
token = os.getenv("myAPIkey")
downCheck = os.getenv("downCheck")
watchCheck = os.getenv("watchCheck")
issueCheck = os.getenv("issueCheck")
forkCheck = os.getenv("forkCheck")
starCheck = os.getenv("starCheck")

myGitHistory = {}
today = date.today()
refRate = int(os.getenv("RefreshRate"))
chartPref = os.getenv("chartPref")

result = {"items": []}
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")
MYINPUT= sys.argv[1]
sameDay = 0
issueFlag = 0





def makePlot (repos, myGitHistory):
    import pandas as pd # under the assumption that these are not imported if new plots are not generated? 
    import matplotlib.pyplot as plt
    
    
    
    

    for myRepo in repos:
        PlotSubset = []
        for item in myGitHistory:
            #print (myGitHistory[item])
            if (item != "RepoURLs") and (myRepo in myGitHistory[item]):
            
                PlotDict = {}
                PlotDict['timestamp'] = item
                PlotDict['value'] = myGitHistory[item][myRepo]['myDownloads']
                PlotSubset.append(PlotDict)


        df = pd.DataFrame(PlotSubset)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d")
        df = df.set_index("timestamp").sort_index()
        
        # plotting
        df['value'].plot()
        #ax.set(xlabel=None)
        plt.style.use('seaborn-poster')
        plt.xlabel('', fontsize=18)
        plt.ylabel('Downloads', fontsize=16)
        plt.title(f"{myRepo}", fontsize=18)       
        plt.savefig(f'{CACHE_FOLDER_IMAGES}/{myRepo}.png')
        #df.to_csv(f'cache/{myRepo}.csv')
        plt.clf()


def FetchGithub (myName, myToken, myLocalGitHistory):
 
    repos_url = 'https://api.github.com/user/repos?per_page=100'
    # added the number per page, since default is 30
    # https://stackoverflow.com/questions/27331849/github-api-v3-doesnt-show-all-user-repositories
    
    myGithubHub = {}
    myURLs = {}
    myRepos = []

    # create a re-usable session object with the user creds in-built
    gh_session = requests.Session()
    gh_session.auth = (username, token)

    # get the list of repos 
    repos = json.loads(gh_session.get(repos_url).text)
    #log ("_________________here")
    for myRepo in repos:
        myURL = myRepo['releases_url']
        myURL = myURL.replace("{/id}", "")
        myGithubHub [myRepo["name"]] = {}
        myRepos.append(myRepo["name"]) #saving a list of repos names to be used with the plot function
        # computing total downloads
        downl = json.loads(gh_session.get(myURL).text)
        #print (myRepo["name"])
        if downl:
            totalDown = 0
            for asset in downl:
                repoDwon = (asset['assets'][0]['download_count'])
                totalDown = totalDown + repoDwon
            myGithubHub [myRepo["name"]]['myDownloads'] = totalDown
        else:
            myGithubHub [myRepo["name"]]['myDownloads'] = 0
        
        myGithubHub [myRepo["name"]]['myWatchers'] = myRepo['watchers_count']
        myGithubHub [myRepo["name"]]['myIssues'] = myRepo['open_issues_count']
        myGithubHub [myRepo["name"]]['myStars'] = myRepo['stargazers_count']
        myGithubHub [myRepo["name"]]['myForks'] = myRepo['forks_count']
        myURLs [myRepo["name"]] = myRepo['html_url']
        myGithubHub = dict(sorted(myGithubHub.items(), reverse = True, key = lambda x: (x[1]['myDownloads'],x[1]['myIssues'])))


    myLocalGitHistory[d1] = myGithubHub
    myLocalGitHistory['RepoURLs'] = myURLs
        
    if chartPref == "1":
        makePlot(myRepos,myLocalGitHistory)

    file2 = open(HISTORY_FILE, "w") 
    file2.write(json.dumps(myLocalGitHistory, indent = 4))
    file2.close()

    return myGithubHub, myURLs

#########
#MAIN CODE
#########

checkingTime()

   # Loading the JSON history file
f = open(HISTORY_FILE)
myGitHistory = json.load(f)
f.close()



# getting the most recent historic
myKeys = list(myGitHistory.keys())

if len(myKeys) == 2:
    myPrevious = sorted (myKeys,reverse = True)[1] #0 is the URL list
else:

    myPrevious = sorted (myKeys,reverse = True)[1] #0 is the URL list
    if myPrevious == d1:
        myPrevious = sorted (myKeys,reverse = True)[2] #takes the previous one if it was checked already today
        sameDay = 1



myGithubHub = myGitHistory[myPrevious]
myURLs = myGitHistory['RepoURLs']

if sameDay == 1:
    subString = f"Last updated earlier today, compared to {myPrevious}"
else:
    subString = f"Last updated on {myPrevious}"
    
myPreviousD = myGitHistory[myPrevious]    

forkString = {}
downString = {}
issueString = {} 
starString = {}
watchString = {}

# comparing to most recent counts
for myRepo in myGithubHub:
    downString[myRepo] = ""
    issueString[myRepo] = ""
    starString[myRepo] = ""
    forkString[myRepo] = ""
    watchString[myRepo] = ""


    # DOWNLOADS
    if downCheck == "1":
        myDelta_downloads = myGithubHub[myRepo]['myDownloads'] - myPreviousD[myRepo]['myDownloads']
        if myDelta_downloads == 0: mySymbol_D = "–"
        if myDelta_downloads > 0: mySymbol_D = f"⬆️+{myDelta_downloads}"
        if myDelta_downloads < 0: mySymbol_D = f"⬇️{myDelta_downloads}" # impossible? 
        downString[myRepo] = f"⬇{myGitHistory[d1][myRepo]['myDownloads']} ({mySymbol_D})"
    
    # STARS
    if starCheck == "1":
        myDelta_stars = myGithubHub[myRepo]['myStars'] - myPreviousD[myRepo]['myStars']
        if myDelta_stars == 0: mySymbol_S = "–"
        if myDelta_stars > 0: mySymbol_S = f"⬆️+{myDelta_stars}"
        if myDelta_stars < 0: mySymbol_S = f"⬇️{myDelta_stars}" 
        starString[myRepo] = f"⭐{myGitHistory[d1][myRepo]['myStars']}({mySymbol_S}) "  
    
    # ISSUES
    if issueCheck == "1":
        myDelta_issues = myGithubHub[myRepo]['myIssues'] - myPreviousD[myRepo]['myIssues']
        if myDelta_issues == 0: mySymbol_I = "–"
        if myDelta_issues > 0: mySymbol_I = f"⬆️+{myDelta_issues}"
        if myDelta_issues < 0: mySymbol_I = f"⬇️{myDelta_issues}" 
        issueString[myRepo] = f"🚨{myGitHistory[d1][myRepo]['myIssues']}({mySymbol_I})"  
    
    # FORKS
    if forkCheck == "1":
        myDelta_forks = myGithubHub[myRepo]['myForks'] - myPreviousD[myRepo]['myForks']
        if myDelta_forks == 0: mySymbol_F = "-"
        if myDelta_forks > 0: mySymbol_F = f"⬆️+{myDelta_forks[myRepo]}"
        if myDelta_forks < 0: mySymbol_F = f"⬇️{myDelta_forks[myRepo]}" 
        forkString[myRepo] = f"🌿{myGitHistory[d1][myRepo]['myForks']}({mySymbol_F})"
    
    # WATCHERS
    if watchCheck == "1":
        myDelta_watchers = myGithubHub[myRepo]['myWatchers'] - myPreviousD[myRepo]['myWatchers']
        if myDelta_watchers == 0: mySymbol_W = "–"
        if myDelta_watchers > 0: mySymbol_W = f"⬆️+{myDelta_watchers}"
        if myDelta_watchers < 0: mySymbol_W = f"⬇️{myDelta_watchers}" # impossible? 
        watchString[myRepo] = f"👀{myGitHistory[d1][myRepo]['myWatchers']} ({mySymbol_W})"
    
    
 
countR = 0
myResLen = len (myGithubHub)

if "--i" in MYINPUT:
    myGithubHub = dict(sorted(myGithubHub.items(), reverse = True, key = lambda x: (x[1]['myIssues'])))
    MYINPUT = MYINPUT.replace ('--i','')
    issueFlag = 1


for myRepo in myGithubHub:
    ## setting the quicklook based on user's preference
    if QUICKLOOK_PREF == "Repo":
        myQuickLook = f"{myURLs[myRepo]}"
    elif QUICKLOOK_PREF == "Issues":
        myQuickLook = f"{myURLs[myRepo]}/issues"
    else:
        myQuickLook = f"{CACHE_FOLDER_IMAGES}/{myRepo}.png"

    if issueFlag == 1:
        myQuickLook = f"{myURLs[myRepo]}/issues"
    
    countR += 1
    
    if MYINPUT.casefold() in myRepo.casefold():
    
        result["items"].append({
            
            "title": (
                f"{myRepo}: {downString[myRepo]}  "  
                f"{issueString[myRepo]}  " 
                f"{starString[myRepo]}  "  
                f"{forkString[myRepo]}  "
                f"{watchString[myRepo]}"
                ),
            "subtitle": f"{countR}/{myResLen} {subString}", 
            "arg": myURLs[myRepo],
            "quicklookurl": myQuickLook
                    
                
        })

print (json.dumps(result))

    






"""
    ## Converting the older history file to the new format

    f = open('/Users/giovanni.coppola/Library/CloudStorage/OneDrive-RegeneronPharmaceuticals,Inc/MyScripts/myGitHubRepos/alfred-GitHubHub/src/myHistory backup.json')
    myOldGit = json.load(f)
    f.close()

    for xx in myOldGit:
        myNewDict[xx] = {}
        for yy in myOldGit[xx]:
            myNewDict [xx][yy] = {}
            myNewDict [xx][yy]['myDownloads'] = myOldGit[xx][yy]



    file2 = open("myNewDict.json", "w") 
    file2.write(json.dumps(myNewDict, indent = 4))
    file2.close()

"""