# coding: UTF-8
"""
Created on 2013-5-8

Author: tianwei

Description: Main Program 
"""
import os
import sys
import config
from post_rc import DailyPost
from getApi import GetRepoCommits


def make_beautiful(info=None):
    """
    make beautiful format
    In:
        a list
    Out:
        a formatted string text
    """
    if info is None:
        return "Today I don't code anything!"

    ret_string = ""

    cnt = 0
    for k, v in info.iteritems():
        for i in info[k]:
            ret_string += "%d. %s \n" % (cnt, i)
            cnt = cnt + 1

    return ret_string


def run():
    """
    Main programming run
    """
    print "[Start] get commits from Github!"
    info = GetRepoCommits()
    a = info.getInfo()
    s = make_beautiful(a)
    print "-"*10
    print s
    print "^"*15

    print "[Start] post daily report!"
    post = DailyPost()
    post.post(info=s)
    post.unistall()
    print "^"*15


if __name__ == "__main__":
    run()


