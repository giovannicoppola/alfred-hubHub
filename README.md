# GitHubHub 🖥️
### A customizable [Alfred](https://www.alfredapp.com/) hub for your GitHub repositories



<a href="https://github.com/giovannicoppola/alfred-GitHubHub/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-GitHubHub/total?color=purple&label=Downloads"><br/>
</a>

![](alfred-GitHubHub.gif)


<!-- MarkdownTOC autolink="true" bracket="round" depth="3" autoanchor="true" -->

- [Motivation](#motivation)
- [Setting up](#setting-up)
- [Basic Usage](#usage)
- [Known Issues](#known-issues)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Feedback](#feedback)

<!-- /MarkdownTOC -->



<h1 id="motivation">Motivation ✅</h1>

- Quickly check the status of your Github repositories (Downloads, Issues) 
- Save download data over time to generate plots

<h1 id="setting-up">Setting up ⚙️</h1>

- Alfred with Powerpack license
- Python3 (howto [here](https://www.freecodecamp.org/news/python-version-on-mac-update/))
- a [GitHub](https://github.com/) account
- a [GitHub](https://github.com/) API token instructions on how to obtain one are [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- Optional: `matplotlib` library (`python -m pip install -U matplotlib`)


## Default settings 
- In Alfred, open the 'Configure Workflow and Variables' window in `alfred-audible` preferences
	<img src='images/alfred_prefs.png' width="500">
	
	- _Optional:_ set the emoji you want to show to mark when a record is in your library (`LIBRARY_SYMBOL`, default: 📗) or in your wishlist(`WISHLIST_SYMBOL`, default: 📕)
	- _Optional:_ set the worklow variable `CATALOG_RESULTS` to control the max number of returned results (default and max is 50)
	- _Optional:_ Change the keyword to launch library/wishlist search (currently set to `@a`), or set a hotkey
	- _Optional:_ Change the keyword to launch catalog search (currently set to `@c`), or set a hotkey
	- _Optional:_ Change the database refresh frequency in days (`UPDATE_DAYS` default: 30 days)




<h1 id="usage">Basic Usage 📖</h1>
- launch with keyword (default: `hubhub`)
- `enter` ↩️ will open the repositoy on `github.com/`



## Refreshing the database 🔄
- database will refresh as indicated by the `UPDATE_DAYS` variable. 
- launch `hubhub:refresh` to force database refresh

<h1 id="known-issues">Limitations & Known issues ⚠️</h1>
# 
- None for now, but I have not done extensive testing, let me know if you see anything!
- tested with Python 3.8.9


<h1 id="acknowledgments">Acknowledgments 😀</h1>

- The [Alfred forum](https://www.alfredforum.com) community.

<h1 id="changelog">Changelog 🧰</h1>

- 12-02-2022: version 0.9


<h1 id="feedback">Feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 
