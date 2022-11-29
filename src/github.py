#!/usr/bin/env python3
# Light drizzle, mist 🌦   🌡️+49°F (feels +47°F, 90%) 🌬️←7mph 🌒 Wed May  4 05:26:13 2022


import requests
import json
from datetime import date
import sys
import os

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)

####
# inputs
####
username = os.getenv("myUsername")
token = os.getenv("myAPIkey")
today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")

 
# Opening JSON file
f = open('myHistory.json')
 
# returns JSON object as
# a dictionary
myHistoryDownloads = json.load(f)
f.close()



myGithubHub = {}
myGitHubHistory = {} 

myDownloads = {}
myIssues = {}
myStars = {}
myURLs = {}


repos_url = 'https://api.github.com/user/repos?per_page=100'
# added the number per page, since default is 30
# https://stackoverflow.com/questions/27331849/github-api-v3-doesnt-show-all-user-repositories


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
        myDownloads [myRepo["name"]] = totalDown
        myGithubHub [myRepo["name"]]['myDownloads'] = totalDown
    else:
        myGithubHub [myRepo["name"]]['myDownloads'] = 0
    
    myGithubHub [myRepo["name"]]['myIssues'] = myRepo['open_issues_count']
    myGithubHub [myRepo["name"]]['myStars'] = myRepo['stargazers_count']
    myGithubHub [myRepo["name"]]['myURLs'] = myRepo['html_url']
    myGithubHub [myRepo["name"]]['myForks'] = myRepo['forks_count']

    
    myIssues [myRepo["name"]] = myRepo['open_issues_count']
    myStars [myRepo["name"]] = myRepo['stargazers_count']
    myURLs [myRepo["name"]] = myRepo['html_url']
            

myDownloads = dict(sorted(myDownloads.items(), reverse = True, key=lambda item: item[1]))
myGithubHub = sorted(myGithubHub.items(), reverse = True, key = lambda x: (x[1]['myIssues'],x[1]['myDownloads']))


# getting the most recent historic
myKeys = list(myHistoryDownloads.keys())
myPrevious = sorted (myKeys,reverse=True)[0]
myPreviousD = myHistoryDownloads[myPrevious]

#log (myPrevious)


myHistoryDownloads[d1] = myDownloads
myGitHubHistory[d1] = myGithubHub
#print (myHistoryDownloads)

file2 = open("myHistoryNew.json", "w") 
file2.write(json.dumps(myGitHubHistory, indent = 4))
file2.close()


# Append-adds at last
file1 = open("myHistory.json", "w") 
file1.write(json.dumps(myHistoryDownloads, indent = 4))
file1.close()

countR =0
myResLen = len (myDownloads)
result = {"items": []}
for myItem in myDownloads:
    countR += 1

    # comparing to previous
    if myItem in myPreviousD:
        myDelta = myDownloads[myItem] - myPreviousD[myItem]
        if myDelta == 0: mySymbol = "↔️"
        if myDelta > 0: mySymbol = "⬆️" + "+" + str(myDelta)
        if myDelta < 0: mySymbol = "⬇️" + "-" + str(myDelta) # impossible? 

    result["items"].append({
        "title": f"{myItem}: {myDownloads[myItem]} ({mySymbol}) 🐛{myIssues[myItem]}, ⭐{myStars[myItem]}",
        "subtitle": f"{countR}/{myResLen}", 
        "arg": myURLs[myItem],
                
        
    })


print (json.dumps(result))


# Github token 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