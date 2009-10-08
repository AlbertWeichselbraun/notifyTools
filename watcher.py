#!/usr/bin/env python

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

from output.rss import RSS
from watcher.webwatcher import Webwatcher

import sys
from os.path import expanduser
sys.path.append( expanduser("~/.notifyTools") )
from siteconfig import RSS_FEEDS


class Watcher(object):
    """ the notifytools main program """

    def __init__(self, watcherList, outputList):
        self.watcherList = watcherList 
        self.outputList  = outputList

    def watch(self):
        """ calls all watchers and sends notifications using the output plugins """
        for watcher in self.watcherList:
            watcher.getNotifications( self.outputList )

        for output in self.outputList:
            output.notify()


if __name__ == '__main__':
    oL = [ RSS('Website Watcher', url, 'Website Watcher', fname) for url, fname in RSS_FEEDS.items() ] 
    wL = ( Webwatcher(), )
    w=Watcher( wL, oL )
    w.watch()
