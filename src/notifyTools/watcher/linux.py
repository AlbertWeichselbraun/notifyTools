#!/usr/bin/env python

""" @package notifyTools.watcher.linux 
    checks whether new linux kernel versions are available
"""

# (C)opyrights 2009 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import urllib
from re import compile
import datetime
from operator import itemgetter

from notifyTools.watcher import Watcher

KERNEL_DIR    = "http://ftp.kernel.org/pub/linux/kernel/v2.6/"
RE_VER        = compile("ChangeLog-(2\.6\.\d+)(\.\d+)?.+(\d{2}-\w{3}-\d{4}\s\d{2}:\d{2})")
RSS_FILE_PATH = "/var/lib/mediawiki/linux.rss"
RSS_FILE_URL  = "http://www.semanticlab.net/linux.rss"

class LinuxWatcher(Watcher):
    """ linux watcher main class """

    def __init__(self, backlog=3):
        """ @param[in] backlog to keep """
        self.backlog = backlog

    def notify(self, notifierList):
        """ checks all sites and generates a notifcation based on the 
            changes observed """

        assert isinstance(notifierList, tuple) or isinstance(notifierList, list)

        kernel_listing    = self._get_kernel_listing()
        relevant_versions = self._parse_kernel_versions( kernel_listing ).values()

        relevant_versions = sorted([ (int(major.split(".")[2]), major, date) for minor, major, date in relevant_versions ], reverse=True)
        for notifier in notifierList:
            for major, kernel_version, date in relevant_versions[:self.backlog]:
                notifier.addNotification( 
                    title = kernel_version,
                    link = "%s/ChangeLog-%s" % (KERNEL_DIR, kernel_version),
                    description = """The latest stable version of the Linux kernel is: 
                                     <a href="%slinux-%s.tar.bz2">%s</a>,
                                     <a href="%sChangeLog-%s">ChangeLog</a>""" % (KERNEL_DIR, kernel_version, kernel_version, KERNEL_DIR, kernel_version), 
                    date  = datetime.datetime.strptime(date, "%d-%b-%Y %H:%M"),
                  )
    
    @staticmethod
    def _get_kernel_listing():
        f=urllib.urlopen( KERNEL_DIR )
        return f.read()
    
    @staticmethod
    def _parse_kernel_versions(kernel_listing):
        vers={}
        for line in kernel_listing.split("\n"):
            m = RE_VER.search(line) 
            if not m: continue
    
            major, minor, date = m.groups()
            if not minor:
                minor = ".0"
    
            minor = int( minor[1:] )
            if vers.get(major, (0,0,0))[0] < minor:
                vers[major] = (minor, major+"."+str(minor), date)
    
        return vers
    

