#!/usr/bin/env python3
# Light drizzle, mist 🌦   🌡️+49°F (feels +47°F, 90%) 🌬️←7mph 🌒 Wed May  4 05:26:13 2022
# Overcast ☁️   🌡️+34°F (feels +32°F, 75%) 🌬️↘4mph 🌓 Tue Nov 29 08:56:35 2022


import requests
import json
from datetime import date
import sys
import os

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)

####################
# inputs          ##
####################
username = os.getenv("myUsername")
token = os.getenv("myAPIkey")
today = date.today()
refRate = int(os.getenv("RefreshRate"))
result = {"items": []}
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")
MYINPUT= sys.argv[1]
sameDay = 0




def FetchGithub (myName, myToken):

    repos_url = 'https://api.github.com/user/repos?per_page=100'
    # added the number per page, since default is 30
    # https://stackoverflow.com/questions/27331849/github-api-v3-doesnt-show-all-user-repositories
    
    myGithubHub = {}
    myURLs = {}

    # create a re-usable session object with the user creds in-built
    gh_session = requests.Session()
    gh_session.auth = (username, token)

    # get the list of repos 
    repos = json.loads(gh_session.get(repos_url).text)

    for myRepo in repos:
        myURL = myRepo['releases_url']
        myURL = myURL.replace("{/id}", "")
        myGithubHub [myRepo["name"]] = {}
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
        
        myGithubHub [myRepo["name"]]['myIssues'] = myRepo['open_issues_count']
        myGithubHub [myRepo["name"]]['myStars'] = myRepo['stargazers_count']
        myGithubHub [myRepo["name"]]['myForks'] = myRepo['forks_count']
        myURLs [myRepo["name"]] = myRepo['html_url']
        myGithubHub = dict(sorted(myGithubHub.items(), reverse = True, key = lambda x: (x[1]['myDownloads'],x[1]['myIssues'])))

    
    myGitHistory[d1] = myGithubHub
    myGitHistory['RepoURLs'] = myURLs
    

    file2 = open("myGitHistory.json", "w") 
    file2.write(json.dumps(myGitHistory, indent = 4))
    file2.close()

    return myGithubHub, myURLs


# Loading the JSON history file
f = open('myGitHistory.json')
myGitHistory = json.load(f)
f.close()


# getting the most recent historic
myKeys = list(myGitHistory.keys())
myPrevious = sorted (myKeys,reverse=True)[1] #0 is the URL list
if myPrevious == d1:
    myPrevious = sorted (myKeys,reverse=True)[2] #takes the previous one if it was checked already today
    sameDay = 1

if refRate < 100: 
    # does not need to update, using cached results
    myGithubHub = myGitHistory[myPrevious]
    myURLs = myGitHistory['RepoURLs']
    
    if sameDay == 1:
        subString = f"Last updated earlier today, compared to {myPrevious}"
    else:
        subString = f"Last updated on {myPrevious}"
else: 
    # needs to be updated and compared with the most recent
    myGithubHub, myURLs = FetchGithub (username,token)
    subString = f"Last updated today, compared to {myPrevious}"
    
myPreviousD = myGitHistory[myPrevious]    
myDelta_downloads = {}
mySymbol_D = {}
myDelta_stars = {}
mySymbol_S = {}
myDelta_issues = {}
mySymbol_I = {}
myDelta_forks = {}
mySymbol_F = {}



# comparing to most recent counts
for myRepo in myGithubHub:
    # DOWNLOADS
    myDelta_downloads[myRepo] = myGithubHub[myRepo]['myDownloads'] - myPreviousD[myRepo]['myDownloads']
    if myDelta_downloads[myRepo] == 0: mySymbol_D[myRepo] = "↔️"
    if myDelta_downloads[myRepo] > 0: mySymbol_D[myRepo] = f"⬆️+{myDelta_downloads[myRepo]}"
    if myDelta_downloads[myRepo] < 0: mySymbol_D[myRepo] = f"⬇️{myDelta_downloads[myRepo]}" # impossible? 

    # STARS
    myDelta_stars[myRepo] = myGithubHub[myRepo]['myStars'] - myPreviousD[myRepo]['myStars']
    if myDelta_stars[myRepo] == 0: mySymbol_S[myRepo] = "↔️"
    if myDelta_stars[myRepo] > 0: mySymbol_S[myRepo] = f"⬆️+{myDelta_stars[myRepo]}"
    if myDelta_stars[myRepo] < 0: mySymbol_S[myRepo] = f"⬇️{myDelta_stars[myRepo]}" 

    # ISSUES
    myDelta_issues[myRepo] = myGithubHub[myRepo]['myIssues'] - myPreviousD[myRepo]['myIssues']
    if myDelta_issues[myRepo] == 0: mySymbol_I[myRepo] = "↔️"
    if myDelta_issues[myRepo] > 0: mySymbol_I[myRepo] = f"⬆️+{myDelta_issues[myRepo]}"
    if myDelta_issues[myRepo] < 0: mySymbol_I[myRepo] = f"⬇️{myDelta_issues[myRepo]}" 

    # FORKS
    myDelta_forks[myRepo] = myGithubHub[myRepo]['myForks'] - myPreviousD[myRepo]['myForks']
    if myDelta_forks[myRepo] == 0: mySymbol_F[myRepo] = "↔️"
    if myDelta_forks[myRepo] > 0: mySymbol_F[myRepo] = f"⬆️+{myDelta_forks[myRepo]}"
    if myDelta_forks[myRepo] < 0: mySymbol_F[myRepo] = f"⬇️{myDelta_forks[myRepo]}" 

countR =0
myResLen = len (myGithubHub)
        
for myRepo in myGithubHub:
        countR += 1
        
        if MYINPUT.casefold() in myRepo.casefold():
        
            result["items"].append({
                
                "title": (
                    f"{myRepo}: ⬇{myGitHistory[d1][myRepo]['myDownloads']} ({mySymbol_D[myRepo]}) "  
                    f" 🐛{myGitHistory[d1][myRepo]['myIssues']}({mySymbol_I[myRepo]})  " 
                    f"⭐{myGitHistory[d1][myRepo]['myStars']}({mySymbol_S[myRepo]}) "  
                    f"🌿{myGitHistory[d1][myRepo]['myForks']}({mySymbol_F[myRepo]})"
                    ),
                "subtitle": f"{countR}/{myResLen} {subString}", 
                "arg": myURLs[myRepo]
                        
                
            })

print (json.dumps(result))

    






"""
#! /usr/bin/env python3

#Tarrytown – Overcast ☁️   🌡️+40°F (feels +35°F, 79%) 🌬️↘4mph 🌓 Wed Nov 30 09:31:23 2022
#W48Q4 – 334 ➡️ 30 – 203 ❇️ 161

#Learning how to plot a comumlative line using matplotlib
# first use: GitHubHub


#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import re
import os
import json


myNewDict = {}



## Converting the older history file to the new fdormat

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



# Loading the JSON history file
f = open('myNewDict.json')
myGitHistory = json.load(f)
f.close()

myRepo = 'alfred-convert'



PlotSubset = []

for item in myGitHistory:
    if (item != "RepoURLs") and (myRepo in myGitHistory[item]):
        PlotDict = {}
        print (item)
        #print (myGitHistory[item][myRepo])
        PlotDict['timestamp'] = item
        PlotDict['value'] = myGitHistory[item][myRepo]['myDownloads']
        PlotSubset.append(PlotDict)


df = pd.DataFrame(PlotSubset)
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d")
df = df.set_index("timestamp").sort_index()
ax = df['value'].plot()

plt.savefig('CumulativeLine.png')



"""