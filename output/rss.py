#!/usr/bin/env python

""" @package notifytools.rss """

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
from datetime import datetime
from cPickle import load, dump
import os.path
import PyRSS2Gen

FEED_MAX_BACKLOG = 5

class RSS(object):
    """ an RSS output object """

    __slots__ = ('feed_title', 'feed_description', 'notifications', 'url', 'fname', 'storagePath', 'lastBuildDate', )

    def __init__(self, title, url, description, fname, lastBuildDate=None, storagePath=None):
        """ @param[in] feed title
            @param[in] feed description
        """
        self.lastBuildDate     = lastBuildDate
        self.feed_title        = title
        self.feed_description  = description
        self.url               = url
        self.fname             = fname
        self.storagePath       = storagePath

        self._loadNotifications()


    def _loadNotifications(self):
        """ loads the list of notifications """
        if not self.storagePath:
            self.notifications = []
            return

        fname = os.path.join( self.storagePath, sha1( self.url).hexdigest() )
        if os.path.exists( fname ):
            self.notifications = load( open(fname) )
        else:
            self.notifications = []


    def _saveNotifications(self):
        """ saves the list of notifications """
        fname = os.path.join( self.storagePath, sha1( self.url).hexdigest() )
        dump( self.notifications, open(fname, "w" ) )


    def addNotification(self, title, link, description, date=datetime.now()):
        """ @param[in] title The entry's title
            @param[in] link  A link to the entry
            @param[in] description
            @param[in] date
        """
        self.notifications.append(
              PyRSS2Gen.RSSItem(
                title = title,
                link = link,
                description = description , 
                pubDate = date,
              )
           )

        if len(self.notifications) > FEED_MAX_BACKLOG:
            self.notifications = self.notifications[1:]
        
        if self.storagePath:
            self._saveNotifications()


    def notify(self):
        """ publishs the rss feed at the given url
            @param[in] fname
            @param[in] url
        """
        rss = PyRSS2Gen.RSS2(
            title         = self.feed_title,
            link          = self.url,
            description   = self.feed_description,
            lastBuildDate = self.lastBuildDate or datetime.now(),
            items         = self.notifications,)

        rss.write_xml(open(self.fname, "w"))
        self.notifications = []

