#!/usr/bin/env python3
# Light drizzle, mist 🌦   🌡️+49°F (feels +47°F, 90%) 🌬️←7mph 🌒 Wed May  4 05:26:13 2022
# Overcast ☁️   🌡️+34°F (feels +32°F, 75%) 🌬️↘4mph 🌓 Tue Nov 29 08:56:35 2022


import requests
import json
from datetime import datetime, date

import sys
import os
import json
from config import CACHE_FOLDER_IMAGES, QUICKLOOK_PREF, HISTORY_FILE

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)



def checkingTime ():
## Checking if the database needs to be built or rebuilt
    timeToday = date.today()
    if not os.path.exists(HISTORY_FILE):
        log ("History File missing ... building")
        myGitHistory = {}
        myGithubHub, myURLs = FetchGithub (username,token,myGitHistory)
    else: 
        databaseTime= (int(os.path.getmtime(HISTORY_FILE)))
        dt_obj = datetime.fromtimestamp(databaseTime).date()
        time_elapsed = (timeToday-dt_obj).days
        log (str(time_elapsed)+" days from last update")
        if time_elapsed >= refRate:
            log ("rebuilding database ⏳...")
               # Loading the JSON history file
            f = open(HISTORY_FILE)
            myGitHistory = json.load(f)
            f.close()
            FetchGithub (username,token, myGitHistory)
            log ("done 👍")
            
    
    
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
openPref = os.getenv("openPref")

result = {"items": []}
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")
MYINPUT= sys.argv[1]

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
        plt.style.use('seaborn-v0_8-poster')
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
    #log (repos)
    #log ("_________________here")
    for myRepo in repos:
        myURL = myRepo['releases_url']
        myURL = myURL.replace("{/id}", "")

        myRepoURL = myRepo['url']
        myGithubHub [myRepo["name"]] = {}
        myRepos.append(myRepo["name"]) #saving a list of repos names to be used with the plot function
        # computing total downloads
        downl = json.loads(gh_session.get(myURL).text)
        #log (myRepo["name"])
        watchers = json.loads(gh_session.get(myRepoURL).text)
        
        watchersCount = watchers ['subscribers_count']
        
        if downl:
            totalDown = 0
            for asset in downl:
                repoDwon = (asset['assets'][0]['download_count'])
                totalDown = totalDown + repoDwon
            myGithubHub [myRepo["name"]]['myDownloads'] = totalDown
        else:
            myGithubHub [myRepo["name"]]['myDownloads'] = 0
        
        myGithubHub [myRepo["name"]]['myWatchers'] = watchersCount
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

if len(myKeys) == 2: #first time running, no previous data
    myPrevious = sorted (myKeys,reverse = True)[1] #0 is the URL list
    myCurrent = myPrevious
else:
    myCurrent = sorted (myKeys,reverse = True)[1] #most recent, 0 is the URL list
    myPrevious = sorted (myKeys,reverse = True)[2] #0 is the URL list
    
        




myGithubHub = myGitHistory[myCurrent]
myPreviousD = myGitHistory[myPrevious]    
myURLs = myGitHistory['RepoURLs']


if myCurrent == d1: #updated the same day
    subString = f"Last updated earlier today, compared to {myPrevious}"
else:
    subString = f"Last updated on {myCurrent}, compared to {myPrevious}"



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
    if (downCheck == "1") and (myRepo in myPreviousD):
        myDelta_downloads = myGithubHub[myRepo]['myDownloads'] - myPreviousD[myRepo]['myDownloads']
        if myDelta_downloads == 0: mySymbol_D = ""
        if myDelta_downloads > 0: mySymbol_D = f"(⬆️+{myDelta_downloads})"
        if myDelta_downloads < 0: mySymbol_D = f"⬇️{myDelta_downloads}" # impossible? 
        downString[myRepo] = f"⬇{myGitHistory[d1][myRepo]['myDownloads']} {mySymbol_D}"
    elif downCheck == "1":
        downString[myRepo] = f"⬇{myGitHistory[d1][myRepo]['myDownloads']}"

    # STARS
    if (starCheck == "1") and (myRepo in myPreviousD):
        myDelta_stars = myGithubHub[myRepo]['myStars'] - myPreviousD[myRepo]['myStars']
        if myDelta_stars == 0: mySymbol_S = ""
        if myDelta_stars > 0: mySymbol_S = f"(⬆️+{myDelta_stars})"
        if myDelta_stars < 0: mySymbol_S = f"(⬇️{myDelta_stars})" 
        starString[myRepo] = f"⭐{myGitHistory[d1][myRepo]['myStars']} {mySymbol_S}"  
    elif (starCheck == "1"):
        starString[myRepo] = f"⭐{myGitHistory[d1][myRepo]['myStars']}"  

    # ISSUES
    if (issueCheck == "1") and (myRepo in myPreviousD):
        myDelta_issues = myGithubHub[myRepo]['myIssues'] - myPreviousD[myRepo]['myIssues']
        if myDelta_issues == 0: mySymbol_I = ""
        if myDelta_issues > 0: mySymbol_I = f"(⬆️+{myDelta_issues})"
        if myDelta_issues < 0: mySymbol_I = f"(⬇️{myDelta_issues})" 
        issueString[myRepo] = f"🚨{myGitHistory[d1][myRepo]['myIssues']} {mySymbol_I}"  
    elif (issueCheck == "1"):
        issueString[myRepo] = f"🚨{myGitHistory[d1][myRepo]['myIssues']}"  

    # FORKS
    if (forkCheck == "1") and (myRepo in myPreviousD):
        myDelta_forks = myGithubHub[myRepo]['myForks'] - myPreviousD[myRepo]['myForks']
        if myDelta_forks == 0: mySymbol_F = ""
        if myDelta_forks > 0: mySymbol_F = f"(⬆️+{myDelta_forks})"
        if myDelta_forks < 0: mySymbol_F = f"(⬇️{myDelta_forks})" 
        forkString[myRepo] = f"🌿{myGitHistory[d1][myRepo]['myForks']} {mySymbol_F}"
    elif (forkCheck == "1"):
        forkString[myRepo] = f"🌿{myGitHistory[d1][myRepo]['myForks']}"

    # WATCHERS
    if (watchCheck == "1") and (myRepo in myPreviousD):
        myDelta_watchers = myGithubHub[myRepo]['myWatchers'] - myPreviousD[myRepo]['myWatchers']
        if myDelta_watchers == 0: mySymbol_W = ""
        if myDelta_watchers > 0: mySymbol_W = f"(⬆️+{myDelta_watchers})"
        if myDelta_watchers < 0: mySymbol_W = f"(⬇️{myDelta_watchers})" # impossible? 
        watchString[myRepo] = f"👀{myGitHistory[d1][myRepo]['myWatchers']} {mySymbol_W}"
    elif (watchCheck == "1"):
        watchString[myRepo] = f"👀{myGitHistory[d1][myRepo]['myWatchers']}"
    
    
 
countR = 0


if "--i" in MYINPUT:
    
    myGithubHub = dict(sorted(((key, value) for key, value in myGithubHub.items() if value['myIssues'] != 0), reverse=True, key=lambda x: x[1]['myIssues']))

    MYINPUT = MYINPUT.replace ('--i','')
    issueFlag = 1


if "--c" in MYINPUT:
    different_apps = {}
    for app, values in myGithubHub.items():
        if values != myPreviousD.get(app, {}):
            different_apps[app] = values
    MYINPUT = MYINPUT.replace ('--c','')
    myGithubHub = different_apps

if openPref == "1" and issueFlag == 0:
    different_apps = {}
    for app, values in myGithubHub.items():
        if values != myPreviousD.get(app, {}):
            different_apps[app] = values
    if "--a" in MYINPUT:
        # overriding prefs
        MYINPUT = MYINPUT.replace ('--a','')
    else:
        myGithubHub = different_apps

    


myResLen = len (myGithubHub)
for myRepo in myGithubHub:
    myArg = myURLs[myRepo]
    
    ## setting the quicklook based on user's preference
    if QUICKLOOK_PREF == "Repo":
        myQuickLook = f"{myURLs[myRepo]}"
    elif QUICKLOOK_PREF == "Issues":
        myQuickLook = f"{myURLs[myRepo]}/issues"
    else:
        myQuickLook = f"{CACHE_FOLDER_IMAGES}/{myRepo}.png"

    if issueFlag == 1: #forcing issues if sorted by issues
        myQuickLook = f"{myURLs[myRepo]}/issues"
        myArg = f"{myURLs[myRepo]}/issues"
    
    countR += 1
    
    
    if MYINPUT.casefold().strip() in myRepo.casefold():
    
        result["items"].append({
            
            "title": (
                f"{myRepo}: {downString[myRepo]}  "  
                f"{issueString[myRepo]}  " 
                f"{starString[myRepo]}  "  
                f"{forkString[myRepo]}  "
                f"{watchString[myRepo]}"
                ),
            "subtitle": f"{countR}/{myResLen} {subString}", 
            "arg": myArg,
            "quicklookurl": myQuickLook
                    
                
        })

if (len(result['items']) > 0):
    print (json.dumps(result))
else:
    resultErr= {"items": [{
        "title": "No matches",
        "subtitle": "Try a different query",
        "arg": "",
        "icon": {
            "path": "icons/Warning.png"
            }
            }]}
    print (json.dumps(resultErr))
    





