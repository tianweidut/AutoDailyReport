# coding: UTF-8
"""
Created on 2013-5-7

Author: tianwei

Description: Get Repo infomation from Github API
"""
import os
import sys
import config
import datetime
import urllib
import urllib2
import simplejson


class GetRepoCommits(object):
    def __init__(self):
        self.username = config.github_username
        self.headers = self.make_headers()
        self.url = config.github
        self.repos = self.get_repos(config.repos)
        self.proxy_settings()

    def make_headers(self):
        """
        make python like a read webbrowser
        """
        return {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;\
                rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def get_repos(self, repo):
        result = []
        for k, v in repo.iteritems():
            result.append(k)

        return result

    def proxy_settings(self):
        """
        Proxy setting, because github maybe broken in China
        """
        if config.proxy_host is None or config.proxy_host == "":
            return

        proxy = urllib2.ProxyHandler({"http": config.proxy_host})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    def process_factory(self, info=None):
        """
        Process the Github API JSON data into the specific information
        In:
            Github API JSON data, it is already a python object
        Out:
            if it is empty, return empty list;
            elif it return the commits history.
            Of course, it only get today information!
        """
        return [item["commit"]["message"] for item in info]

    def make_args(self, args):
        """
        make args in GET method
        In:
            args: it is a dict
        Out:
            GET method string, like "?author='tianweidut'&since='2013-05-10'"
        """
        result_str = "?"
        for k, v in args.iteritems():
            result_str = result_str + k + "=" + v + "&"
        return result_str

    def get_details(self, repo=None):
        """
        Get detail from API according by repo name
        In:
            repo name, it is the postfix of github URL,
            if one repo is in https://github.com/tianweidut/Linux-Configuration
            so the repo is "tianwei/Linux-Configuration"
        Out:
            Github API JSON, it is a python object
        """
        api_json = []

        #get all branches from this repo
        branches = self.make_branches(self.getBranch(repo))

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(2)

        for branch in branches:
            args = {"per_page": "100",
                    "sha": branch,
                    "author": self.username,
                    "since": yesterday.isoformat()}
            args = self.make_args(args)
            repo_url = "/".join([self.url, "repos", repo, "commits"])
            repo_url = repo_url + args

            request = urllib2.Request(repo_url, headers=self.headers)
            response = urllib2.urlopen(request)
            raw_data = response.read()
            commits_info = self.process_factory(simplejson.loads(raw_data))
            api_json = api_json + commits_info

            print repo_url

        print api_json
        return api_json

    def getBranch(self, repo=None):
        """
        Get all branches from repo
        In:
            repo, repo name
        Out:
            Github API Json string
        """
        repos_list_url = "/".join([self.url, "repos", repo, "branches"])
        print repos_list_url
        request = urllib2.Request(repos_list_url, headers=self.headers)
        response = urllib2.urlopen(request)

        return response.read()

    def make_branches(self, api_json=None):
        """
        Convert API JSON into a repo name list
        In:
            api_json, from Github API
        Out:
            a list which contains branch name
        """
        if api_json is None:
            return []

        obj = simplejson.loads(api_json)
        branches = [item["commit"]["sha"] for item in obj]

        print branches

        return branches

    def getInfo(self):
        """
        Get infomation from Github API
        Out:
            a dict of specific repo comments,
            key is the repo name
            value is a list of commits history today
        """
        # get repos name
        result = {}
        for item in self.repos:
            info = self.get_details(repo=item)
            result[item] = info

        return result


if __name__ == "__main__":
    t = GetRepoCommits()
    print t.getInfo()
