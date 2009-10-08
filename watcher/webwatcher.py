#!/usr/bin/env python

""" Webwatcher """

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

__version__ = "$Header$"

from hashlib import sha1
from commands import getoutput
from cPickle import load, dump
from difflib import Differ
import os.path, os

import sys
from os.path import expanduser
sys.path.append( expanduser("~/.notifyTools") )
from siteconfig import WEBWATCHER_SITES

LYNX="/usr/bin/lynx -force_html -nocolor -dump -nolist -nobold -pseudo_inlines=0 -display_charset=utf8 %s"

class Webwatcher:

    def __init__(self, storagePath):
        self.storagePath = storagePath
        self.changes = {}  # a dictionary containing the url, changed text and change percentage


    def getNotifications( self, notifierList ):
        """ checks all sites and generates a notifcation based on the 
            changes observed """

        assert isinstance(notifierList, tuple) or isinstance(notifierList, list)
        changes = {}
        for url, minChangePercentage in WEBWATCHER_SITES.items():
            change = self.getChange( url )
            if change  > minChangePercentage:
                changeText = self.getChangeText( url )
                for notifier in notifierList:
                    notifier.addNotification("%s changed by %d %%" % (url, 100*change), url, "%s<br/><a href=\"%s\">more...</a>" % (changeText, url) )


    def _computeChange(self, url):
        """ computes the changes for the given url """
        if url in self.changes:
            return

        d = Differ()
        old = self._loadWebsite( url )
        new = self._getPageWebsite( url )
        self._saveWebsite( url, new )

        newLines = [ t[2:] for t in d.compare(old, new) if t.startswith("+ ")  ]
        oldLines = [ t[2:] for t in d.compare(old, new) if t.startswith("  ")  ]

        self.changes[url] = ("\n".join(newLines), float(len(newLines) ) / ( len(newLines) + len(oldLines) ) )


    def getChange( self, url ):
        """ returns the percentage to which this url has changed
            @param[in] url
            @returns change (in %)
        """
        self._computeChange( url ) 
        return self.changes[url][1]

    
    def getChangeText( self, url ):
        """ returns the new text added to the web site 
            @param[in] url
            @returns the changed text 
        """
        self._computeChange( url )
        return self.changes[url][0]
        

    def getStorageFname( self, url ):
        """ returns the storage location for the given url 
            @param[in] url
            @returns fname 
        """
        return os.path.join(self.storagePath, ( sha1(url).hexdigest() ) )

    def _saveWebsite( self, url, website ):
        """ saves the saved Website for the given url 
            @param[in] url
            @param[in] Website
        """
        fname = self.getStorageFname( url )
        if not os.path.exists( os.path.dirname(fname) ):
            os.makedirs( os.path.dirname(fname) )
        dump( website, open(fname, "w") )
 
    def _loadWebsite( self, url ):
        """ returns the saved Website for the given url 
            @param[in] url
            @returns a set of hashs describing the url
        """
        fname = self.getStorageFname( url )
        if os.path.exists(fname):
            return load( open(fname) )
        else:
            return list()
    
    @staticmethod
    def _getPageWebsite( url ):
        """ returns the Website for the given page 
            @param[in] url
            @returns a set of hashs describing one line of the page each 
        """
        assert "http" in url or "https" in url
        return [ line for line in getoutput(LYNX % url).split("\n") ]


class TestWebWatcher(object):
    """ tests the Webwatcher object """

    def testGetPageWebsite(self):
        wS = Webwatcher._getPageWebsite( "http://www.heise.de" )
        print wS


if __name__ == '__main__':
    print Webwatcher().getChange("http://www.heise.de")
    print Webwatcher().getChangeText("http://www.heise.de")
