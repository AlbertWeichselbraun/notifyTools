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


from datetime import datetime
import PyRSS2Gen

class RSS(object):
    """ an RSS output object """

    __slots__ = ('feed_title', 'feed_description', 'notifications', 'url', 'fname' )

    def __init__(self, title, url, description, fname):
        """ @param[in] feed title
            @param[in] feed description
        """
        self.notifications    = []
        self.feed_title       = title
        self.feed_description = description
        self.url              = url
        self.fname            = fname

    def addNotification(title, link, description, date=datetime.now()):
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

    def notify(self):
        """ publishs the rss feed at the given url
            @param[in] fname
            @param[in] url
        """
        rss = PyRSS2Gen.RSS2(
            title         = self.feed_title,
            link          = self.url,
            description   = self.feed_description,
            lastBuildDate = datetime.now(),
            items         = self.notifications,)

        rss.write_xml(open(self.fname, "w"))
        self.notifications = []

