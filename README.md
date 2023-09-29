## Jarvs

#### Jarvs is a research visist summary management system, build with large-scale clinical research in mind.

Resarch visit summaries (RVSs) are written descriptions of a patient's clinical visit. An RVS is written by the research-doctor-on-point for a given participant after they undergo strenuous participation in a clinical reserach program. For the one I worked for at UCSF, this involved a 40-hour week of being questioned, tested, poked, prodded, and scanned, often after a flight across the country. So this summary is full of personal health insights that a traditional hospital usually doesn't have the resources to offer and is deeply valuable to patients and their families.

In a busy program such as this, it's important to write, review and send out these summaries in a timely fashion. One of my many responsiblities during my time at UCSF was managing this process and ensuring it ran smoothly. I was having a hard time staying on top of this manually and, under my hands, it sometimes took almost a full year for folks to get their summaries, right before their next visit. At the time, I was also teaching myself how to write code in my free time, so I saw an opportunity to automate it, and hopefully get them in patients hands quicker.

I'm proud to say it did – we were even able to reduce our "red metric" of > 6 months after I automated my RVS responsiblities with JARVS and am told it's still being used today. As a now professional software engineer, I look back on the things about this that I would implement differently, but more than that, I'm proud of the way I was able to learn by doing something that offered tangible benefits to the peolpe around me, and how I put in the work to package + open-source it in case other research programs needed something similar.

This project is also special to me becuase it showed me how much I loved software engineering and motivated me to figure out how to do it for a living.

## Note:
At the moment, the master branch works on both os x and linux operating systems, but was being depreciated for an Ubuntu-specific version. I am not activitely developing this, but if you are using this and something is broken or missing, please let me know and I'd be happy to make improvements.

## Installation
You have two options:
* Use the tkinter-based master branch version with `git clone http://github.com/fonsecapeter/jarvs` in your home directory (os x or linux)
  * Enter the project `cd ~/jarvs/app` then `./gui.py` to run the program
  * Dependencies may be needed (see more information below)

or

* Use the GTK-based [Ubuntu release](http://launchpad.net/jarvs) with a more familiar:
```bash
sudo add-apt-reposoity ppa:peter-nfonseca/jarvs
sudo apt-get update
sudo apt-get install jarvs
```
  * Updates are as simple as `sudo apt-get update` then `sudo apt-get upgrade`
  * Running is as simple as clicking the icon (in accessories) or typing `jarvs` into a terminal
    * The first startup may take a littel extra time, just be patient - using the terminal on this first startup will give some helpful details about what is happening (building ~/.jarvs and it's contents)
    > if anything goes wrong, you may need to `sudo apt-get python-gobject` and/or change the software source to match `universe trusty`

> you can also grab the latest tar.gz by navigating to the [Releases Tab](https://github.com/fonsecapeter/jarvs/releases)

## Usage
Either way, the first order of business will be configuring settings. Jarvs has a terminal-like text display, which operates through natural language commands (all lower-case for now), as well as standard gui main-menu drop downs.

![jarvs_prefs](docs/jarvs_prefs.png)

(RVS Directory takes an absolute path, ending in "/" - file chooser dialog to come.)
> Spaces are currently not supported in this path

After that, just set the attendings

![jarvs_attends](docs/jarvs_attends.png)

("Directory Name" should end in "/" - this is the name of the folder inside RVS Directory)
> Spaces also not currently supported

The optional directory set-up feature is still in the works, but at this point you should either already have or should go set up your RVS directory, which should have a folder for each attending. Each of these folders will hold the RVSs (usually .doc or .docx). It is very important that each RVS is named exactly under the convention `Lname, Fname_pidn_yyyy.mm.dd_RVS`

Once you are all set, you can run your first report.

![jarvs_report](docs/jarvs_report.png)

After that, Jarvs can visualize the latest entry in that report - which is great for just keeping an eye on the attendings or even using as a motivational tool (if you work with a friednly, competitive group).

![jarvs_vis](docs/jarvs_vis.png)

If there are a lot of RVSs waiting for approval, it might be a good idea to let Jarvs email a friendly reminder to the attendings who have outstanding RVSs. If this is the first time, you might want to send out some test emails that only go to your email (the one you provided in your preferences)

![jarvs_test_email](docs/jarvs_test_email.png)

If that looks good to you, give jarvs the green-light to send them out to the attenings.

![jarvs_email](docs/jarvs_email.png)

Because these core features run off of bash scripts (in ~/.jarvs) - you can set up some very helpful crontab jobs. I keep a weekly email every monday at 10:00 am and a matching report. To set this up, just open a terminal and type `crontab -e` - this will open the crontab in nano. Go to the bottom (after all the lines beginning with `#`) and add your commands. I added:
```bash
0 10 * * mon /home/peter/.jarvs/RVS_emailer.sh
0 10 * * mon /home/peter/.jarvs/RVS_reporter.sh
```

This translates in english to: at 0 minutes after 10am (any day of month, any month of year) on every Monday, run the emailer and reporter scripts in the ~/.jarvs directory. When you are done adding those lines, press `<ctrl^O>` to save, `<enter>` to select the right place to save (will auto-choose the right spot), then `<ctrl^X>` to exit nano. You can verify that it saved by typing `crontab -l` into the terminal.

You can also always add a `#` before the line that you want to "turn-off" if you need to.

> ubuntu version dependencies (will resolve with install): python 2, matplotlib 1.5, pandas, numpy

> github version dependencies:
mac os x or linux-based operating system, bash shell, python 2, matplotlib, pandas, numpy, recommend  anaconda (comes with all python libraries and more), gcalcli
>> if using linux: weather-util, weather-util-data
>>
>> if using mac: coreutils, recommend also using homebrew package manager
