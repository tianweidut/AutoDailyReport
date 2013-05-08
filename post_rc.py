# coding: UTF-8
"""
Created on 2013-5-8

Author: tianwei

Description: Simulate web browser with Selenium RC
"""

import os
import config

from selenium import webdriver, selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


class DailyPost(object):
    def __init__(self):
        self.base_url = config.host
        self.login_url = "/Account/Login.aspx"
        self.report_url = "/ReportDetail.aspx?ID=3b363280-091e-4a79-b272-d5a0b981269a"

        self.selenium = selenium("192.168.2.90", 4444, "*firefox",
                                 self.base_url)
        self.selenium.start()

    def post(self, info=None):
        if info is None:
            return False

        br = self.selenium

        # login
        br.open(self.login_url)
        br.type("ctl00$Main$txtUsername", config.username)
        br.type("ctl00$Main$txtPWD", config.password)
        br.click("ctl00$Main$btnLogin")
        br.wait_for_page_to_load(20000)

        # jump
        br.open(self.report_url)
        br.type("ctl00$Main$txtPost", info)
        br.click("Sidebar_lbSubmit")

    def unistall(self):
        self.selenium.stop()

if __name__ == "__main__":
    a = DailyPost()
    a.post(info="Test Test new ")
    a.unistall()
