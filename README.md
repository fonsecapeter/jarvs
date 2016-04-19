## Jarvs

#### Jarvs is a research visist summary management system, build with large-scale clinical research in mind.

At the moment, the GitHub version of Jarvs works on both os x and linux operating systems, but it is being transitioned into an Ubuntu application. Development is still underway for the transfer, but users have two options at the moment.
* Use the stable tkinter-based GitHub version with a simple `git clone http://github.com/fonsecapeter/jarvs` in your home directory (os x or linux)
** This will require the user to `cd ~/jarvs/app` then `./gui.py` to run the program

* Patiently follow the development of the GTK-based [Ubuntu release](http://launchpad.net/jarvs) with a more familiar:
```sudo add-apt-reposoity ppa:peter-nfonseca/jarvs
sudo apt-get update
sudo apt-get install jarvs
``` 
  * updates are as simple as `sudo apt-get update` then `sudo apt-get upgrade`

Either way, the first order of business will be configuring settings. Jarvs has a terminal-like text display, which operates through natural language commands (all lower-case for now), ad well as standard gui main-menu drop downs.
"User Email" and "RVS Directory" are the important bits. (RVS Directory takes an absolute path - file chooser dialog to come)

After that, just set the attendings (give their information in the contacts-like dialog - this is where the Ubuntu version is still behind)

Now Jarvs is ready to help save manage research visit summaries (RVSs). There are four main featurs: 
1. Optional directory set-up
2. Reporting (logs which attendings have outstanding RVSs in a spreadshet - RVS_report.csv)
3. Data Visualization (visualizes the most recent entry in RVS_report.csv)
4. Weekly Emails (uses crontab to send weekly emails to the attendings who have outstanding RVSs)

Obligatory screenshot:
![jarvs_16.04_prefs](app/design/jarvs_16.04_prefs.png)
Jarvs started life as a terminal-app, including a quick description of what an RVS is and what an RVS manager has to do:
![what_is_rvs.png](app/design/what_is_rvs.png)
![what_is_rvs_manager_1.png](app/design/what_is_rvs_manager_1.png)
<a href="url"><img src="https://github.com/fonsecapeter/jarvs/blob/master/app/rvs/sample_docs/rvs_lifecycle.png" width="600"></a>
![what_is_rvs_manager_2.png](app/design/what_is_rvs_manager_2.png)
![figure_1.png](app/rvs/sample_docs/figure_1.png)

> dependencies:
mac os x or linux-based operating system, bash shell, python 2, matplotlib, pandas, numpy, recommend  anaconda (comes with all python libraries and more), gcalcli
>> if using linux: weather-util, weather-util-data
>>
>> if using mac: coreutils, recommend also using homebrew package manager
