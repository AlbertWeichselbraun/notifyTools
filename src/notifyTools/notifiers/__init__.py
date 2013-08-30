#!/usr/bin/env python

''' @package notifytools.notifiers '''

# (C)opyrights 2013 by Albert Weichselbraun <albert@weichselbraun.net>
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

from datetime import datetime

class Notifier(object):
    
    def __init__(self):
        self.notifications = []

    def addNotification(self, title, link, description, date=datetime.now()):
        ''' @param[in] title The entry's title
            @param[in] link  A link to the entry
            @param[in] description
            @param[in] date
        '''
        self.notifications.append(
            {'title': title, 
             'link' : link,
             'description': description,
             'date': date,
            }
          )

    def formatNotification(self, notification):
        ''' Provides a text representation of the given
            notification '''
        raise NotImplemented
   
    def notify(self):
        ''' publishes the notfication '''
        raise NotImplemented


class EchoNotifier(Notifier):
    
    def notify(self):
        print '\n\n'.join( map(self.formatNotification, self.notifications) )
        self.notifications = []

    def formatNotification(self, notification):
        return '''* %(title)s (%(date)s) *

Link: %(link)s
%(description)s''' % (notification)

