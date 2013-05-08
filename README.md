AutoDailyReport
===============

##What's this?
Automatically fetch commits history from github and upload SIE daily report system.

##How to install?
* sudo pip install selenium
* install your Selenium Server, in SIE network environment, you can use hadoop cluster machine,
it has already been deployed!

##How to use?
1. edit config.py, fill your github username and repo name;
1. fill your username and password in SIE Daily Report System.
1. run it in python environment, like
    > python run.py 
1. you can write cron script to run this script automatically!

##Related Technical
* Github API v3
* urllib2, urllib in python
* Selenium RC, a powerful test tool
