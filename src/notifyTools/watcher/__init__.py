#!/usr/bin/env python

''' 
@package notifyTools.watcher
         Watcher Interface 
'''

# (C)opyrights 2009-2013 by Albert Weichselbraun <albert@weichselbraun.net>
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

import sys
from os.path import expanduser, join, dirname
from os import makedirs
from hashlib import sha1
from json import load, dump

sys.path.append( expanduser('~/.notifyTools') )
from notifyTools.diff import TextDiff
from siteconfig import WATCHER_STORAGE_PATH

class Watcher(object):
    ''' the watcher interface '''

    def __init__(self, url):
        self.url  = url
        self.link = url

    def getTitle(self):
        return "[notifier] Changes for %s." % (self.url, )

    def notify(self, notifierList):
        ''' checks all sites and generates a notifcation based on the 
            changes observed 
            ::param notifierList: a list of notifiers to notify
        '''

        assert isinstance(notifierList, tuple) or isinstance(notifierList, list)

        for notifier in notifierList:
                notifier.addNotification( 
                    title = self.title,
                    link = self.link,
                    description = getDiff(self.url)[0]
                    date  = datetime.datetime.strptime(date, "%d-%b-%Y %H:%M"),
                  )
 
    def getDiff(self, url):
        ''' 
            * compute the difference between the old and new version.
            * update the locally stored version of the content

            ::param url: the url to test

            ::returns: the difference between the locally stored (old)
                       and current (new) version of the given url.
        '''
        old_content = self.getDiskContent(url)
        new_content = self.getUrl(url)
        self.saveDiskContent(new_content)

        d = TextDiff(self.getTextContent(old_content),
                     self.getTextContent(new_content))
        return d.get_change_text(), d.get_change_percentage()

    @staticmethod
    def getUrl(url):
        ''' ::returns: the content for the given url 
        '''
        f=urllib.urlopen(self.url)
        return f.read()

    @classmethod
    def loadDiskContent(cls, url):
        fname = cls.getStorageFname(url)
        if not exists(fname):
            return ""
        with open(fname) as f:
            return load(f) 

    @classmethod
    def saveDiskContent(cls, obj):
        fname = cls.getStorageFname(url)
        with open(fname) as f:
            return dump(obj, f) 

    @staticMethod
    def getStorageFname(url):
        fname = join(WATCHER_STORAGE_PATH, ( sha1(url).hexdigest() ))
        if not os.path.exists( dirname(fname) ):
            makedirs( dirname(fname) )
        return fname

    @staticmethod
    def getTextContent(input_content):
        '''
        ::param input_text: 
        ::returns: the text representation used for the diff of the
                   given content
        '''
        raise NotImplemented

    title = property(getTitle)

        
