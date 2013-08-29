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
from watcher.webwatcher import WebWatcher
from watcher.linux import LinuxWatcher
from datetime import datetime

import sys
from os.path import expanduser, dirname
sys.path.extend( (expanduser("~/.notifyTools"), dirname( __file__ ),) )
from siteconfig import RSS_FEEDS, OUTPUT_STORAGE_PATH, WATCHER_STORAGE_PATH, LINUX_WATCHER_OUTPUT


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
    oL = [ RSS('Website Watcher', url, 'Website Watcher', fname, storagePath=OUTPUT_STORAGE_PATH) for url, fname in RSS_FEEDS.items() ] 
    wL = ( WebWatcher(WATCHER_STORAGE_PATH), )
    Watcher(wL, oL).watch()

    oL = ( RSS('Latest stable linux kernel versions', 'http://www.semanticlab.net/linux.rss', "A list of the latest kernel versions.", fname=LINUX_WATCHER_OUTPUT, lastBuildDate = datetime.now()), )
    wL = ( LinuxWatcher(backlog=3), )
    Watcher(wL, oL).watch()

