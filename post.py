# coding: UTF-8
"""
Created on 2013-5-7

Author: tianwei

Description: Daily Report post
"""
import sys
import os
import urllib
import urllib2
import httplib
import cookielib
import config
from ClientForm import ParseResponse
import mechanize


class DailyReportPost(object):
    def __init__(self):
        self.login_url = "/".join([config.host, "Account/Login.aspx"])
        self.report_url = "/".join([config.host, "Default.aspx"])

    def post(self, info=None):
        # cookie
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.addheaders = [("User-agent", "Mozilla/4.0")]
        urllib2.install_opener(opener)

        # login args
        args = {"ctl00$Main$txtUsername": config.username,
                "ctl00$Main$txtPWD": config.password}
        login_post_data = urllib.urlencode(args)

        # send request
        request = urllib2.Request(self.login_url, login_post_data)
        response = urllib2.urlopen(request)

        #print response.read()

        conn = urllib2.urlopen(self.report_url)
        print conn.read()
    
    def post_mechine(self):
        br = mechanize.Browser()
        br.open(self.login_url)
        br.select_form(nr=0)
        br["ctl00$Main$txtUsername"] = config.username
        br["ctl00$Main$txtPWD"] = config.password
        response = br.submit()

        br.open("http://192.168.2.36:3279/ReportDetail.aspx?ID=3b363280-091e-4a79-b272-d5a0b981269a")
        br.select_form(nr=0)
        print br.form
        br["ctl00$Main$txtPost"] = "调整页面test"
        print "*"*10
        print br.form
        for link in br.links():
            print link
        repo = br.click_link(nr=4)
        print repo


    def post_clientform(self):
        response = urllib2.urlopen(self.login_url)
        forms = ParseResponse(response, backwards_compat=False)
        form = forms[0]
        form["ctl00$Main$txtUsername"] = config.username
        form["ctl00$Main$txtPWD"] = config.password

        request = form.click()
        response2 = urllib2.urlopen(request)

        print response2.geturl()
        print response2.info()
        print response2.read()

        response2.close()
        response.close()


if __name__ == "__main__":
    t = DailyReportPost()
    #t.post()
    #t.post_clientform()
    t.post_mechine()
