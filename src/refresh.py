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



    
####################
# inputs          ##
####################
username = os.getenv("myUsername")
token = os.getenv("myAPIkey")

myGitHistory = {}
today = date.today()

chartPref = os.getenv("chartPref")

result = {"items": []}
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")

sameDay = 0





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
    #log ("_________________here")
    for myRepo in repos:
        myURL = myRepo['releases_url']
        myURL = myURL.replace("{/id}", "")
        myRepoURL = myRepo['url']
        myGithubHub [myRepo["name"]] = {}
        myRepos.append(myRepo["name"]) #saving a list of repos names to be used with the plot function
        # computing total downloads
        downl = json.loads(gh_session.get(myURL).text)
        #print (myRepo["name"])
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

if not os.path.exists(HISTORY_FILE):
    log ("History File missing ... building")
    myGitHistory = {}
    FetchGithub (username,token,myGitHistory)
else: 
    log ("rebuilding database ⏳...")

# Loading the JSON history file
    f = open(HISTORY_FILE)
    myGitHistory = json.load(f)
    f.close()

    FetchGithub (username,token, myGitHistory)
    log ("done 👍")

    


result= {"items": [{
    "title": "Done!" ,
    "subtitle": "ready to search now",
    "arg": "",
    "icon": {

            "path": "icons/done.png"
        }
    }]}
print (json.dumps(result))

