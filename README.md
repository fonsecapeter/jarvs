## Jarvs

#### Jarvs is a personal assistant living the terminal that was initially built to be a 'JARVIS' for rvs management.

 > The code written to support the rvs program is immortalized within jarvs, containing a clone of the real rvs server with fake names and data. See the rvs repository for more detail on rvs-related code.

Jarvs is currently programmed to also contain a number of utilities, such as the current date, gcoogle calendar appointments, and weather information (in San Francisco). I sourced all of these utilities from pre-existing tools, just putting them together in an easily accessible way. More utilities are in the works. My work computer runs a Linux operating system and I use a mac-book at home, so Jarvs is fully Linux/Mac cross-compatibile.

Here is Jarvs helping me out while I'm at work:

![screenshot_linux.png](app/design/screenshot_linux.png)

Here is Jarvs helping me out from home:

![screenshot_mac.png](app/design/screenshot_mac.png)

Jarvs also remembers a few basic preferences that can be changed.

At work, Jarvs will pull the real rvs data and commands, but at home, Jarvs works off of the clone. A detailed description of the rvs program (what an rvs is and what the rvs manager does) can be explained by jarvs as below:

![what_is_rvs.png](app/design/what_is_rvs.png)
![what_is_rvs_manager_1.png](app/design/what_is_rvs_manager_1.png)
<a href="url"><img src="https://github.com/fonsecapeter/jarvs/blob/master/app/rvs/sample_docs/rvs_lifecycle.png" width="600"></a>
![what_is_rvs_manager_2.png](app/design/what_is_rvs_manager_2.png)
![figure_1.png](app/rvs/sample_docs/figure_1.png)

A gui is in the works...

![jarvs_gui.png](app/design/jarvs_gui.png)

> dependencies:
mac os x or linux-based operating system, bash shell, python 2, matplotlib, pandas, recommend  anaconda (comes with all python libraries and more), gcalcli
>> if using linux: weather-util, weather-util-data
>>
>> if using mac: coreutils, recommend also using homebrew package manager
