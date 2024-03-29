# alfred-hubHub 🖥️
### A customizable [Alfred 5](https://www.alfredapp.com/) hub for your GitHub repositories



<a href="https://github.com/giovannicoppola/alfred-GitHubHub/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-GitHubHub/total?color=purple&label=Downloads"><br/>
</a>

![](images/hubhub.gif)


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

- Quickly check the status of your Github repositories (downloads, issues, forks, etc) 
- Save download data over time to generate plots

<h1 id="setting-up">Setting up ⚙️</h1>

- Alfred 5 with Powerpack license
- Python3 (howto [here](https://www.freecodecamp.org/news/python-version-on-mac-update/))
- a [GitHub](https://github.com/) account
- a [GitHub](https://github.com/) API token (Instructions on how to obtain one are [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- Optional: `matplotlib` and `pandas` libraries (`python3 -m pip install -U matplotlib` and `python3 -m pip install -U pandas`) are needed to get download charts.



## Default settings 
- In Alfred, open the 'Configure Workflow' menu in `alfred-hubHub` preferences
	- set GitHub username and token (**required**)
	- select the relevant checkbox, if you want to show:
		- Downloads ⬇️ (across all versions)
		- Issues 🚨
		- Stars ⭐
		- Forks 🌿
		- Watchers 👀
	- _Optional:_ Change the database refresh frequency in days (default: 1 day)
	- _Optional:_ Change the location of the database (default: workflow cache folder)
	- _Optional:_ Change the Quicklook behavior (Repo main page, Repo Issues, Downloads chart). Default: download charts, or repo main page if charts disables. When sorted by issues (`--i` tag) Quicklook and Enter go to repo issues page. 
	- _Optional:_ Disable chart generation
	- _Optional:_ Set to show only changed items upon launching (`--a` to override) 
	- _Optional:_ Change workflow keywords



<h1 id="usage">Basic Usage 📖</h1>

- launch with keyword (default: `hubhub`), or custom hotkey
- use the tag `--i` to sort by number of issues
- `--c` will only show changed repositories from previous save
- `enter` ↩️ will open the repository on `github.com/`, unless the `--i` tag is used, in which case it open repo issues
- `shift` ⇧ will show a preview based on user's preferences (default: download charts, or repo page if no charts)
- every time you use the workflow, the counts are stored in a JSON file, which can then be used to create plots of downloads



## Refreshing the database 🔄
- database will refresh as indicated by the `UPDATE_DAYS` variable. 
- launch `hubhub:refresh` to force database refresh

<h1 id="known-issues">Limitations & known issues ⚠️</h1>

- None for now, but I have not done extensive testing, let me know if you see anything!
- It looks like GitHub counts together issues and pull requests? 
- tested with Python 3.9.13


<h1 id="acknowledgments">Acknowledgments 😀</h1>

- Thanks to the [Alfred forum](https://www.alfredforum.com) community!

<h1 id="changelog">Changelog 🧰</h1>

- 09-28-2023: version 0.9.6, fixed watchers count again (API change?)
- 09-09-2023: version 0.9.5, fixed watchers count, matplotlib style
- 08-07-2023: version 0.9.4, added option to show changed items only upon opening (`--a` to override), hidden issues with 0 counts for `--i` tag
- 06-11-2023: version 0.9.3, added `--c` tag to show changed repositories only
- 12-03-2022: version 0.9


<h1 id="feedback">Feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 
