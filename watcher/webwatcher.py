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
import os.path, os

import sys
from os.path import expanduser
sys.path.append( expanduser("~/.notifyTools") )
from siteconfig import WEBWATCHER_SITES

LYNX="/usr/bin/lynx -force_html -nocolor -dump -nolist -nobold -pseudo_inlines=0 -display_charset=utf8 %s"
STORAGE_PATH=".notify-webwatcher/%s"

class Webwatcher:

    def getNotifications( self, notifierList ):
        """ checks all sites and generates a notifcation based on the 
            changes observed """

        assert isinstance(notifierList, tuple) or isinstance(notifierList, list)
        changes = {}
        for url, minChangePercentage in WEBWATCHER_SITES.items():
            change = self.getChange( url )
            if change  > minChangePercentage:
                for notifier in notifierList:
                    notifier.addNotification("%s changed" % url, "Webwatcher detected a %d change at <a href=\"%s\">%s</a>" % (100*change, url, url) )


    def getChange( self, url ):
        """ returns the percentage to which this url has changed
            @param[in] url
            @returns change (in %)
        """
        old = self._loadHashSet( url )
        new = self._getPageHashSet( url )
        self._saveHashSet( url, new )

        return float( len(new.difference( old )) )/len(new)

    @staticmethod
    def getStorageFname( url ):
        """ returns the storage location for the given url 
            @param[in] url
            @returns fname 
        """
        return STORAGE_PATH % ( sha1(url).hexdigest() )

    @staticmethod
    def _saveHashSet( url, hashSet ):
        """ saves the saved hashSet for the given url 
            @param[in] url
            @param[in] hashSet
        """
        fname = Webwatcher.getStorageFname( url )
        if not os.path.exists( os.path.dirname(fname) ):
            os.makedirs( os.path.dirname(fname) )
        dump( hashSet, open(fname, "w") )
 
    @staticmethod
    def _loadHashSet( url ):
        """ returns the saved hashSet for the given url 
            @param[in] url
            @returns a set of hashs describing the url
        """
        fname = Webwatcher.getStorageFname( url )
        if os.path.exists(fname):
            return load( open(fname) )
        else:
            return set()
    
    @staticmethod
    def _getPageHashSet( url ):
        """ returns the hashSet for the given page 
            @param[in] url
            @returns a set of hashs describing one line of the page each 
        """

        assert "http" in url or "https" in url
        hashSet = set()
        for line in getoutput(LYNX % url).split("\n"):
            hashSet.add( sha1(line).hexdigest() )

        return hashSet


class TestWebWatcher(object):
    """ tests the Webwatcher object """

    def testGetPageHashSet(self):
        hS = Webwatcher._getPageHashSet( "http://www.heise.de" )
        print hS
        asdf


if __name__ == '__main__':
    print Webwatcher().getChange("http://www.heise.de")
