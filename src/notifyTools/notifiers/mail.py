#!/usr/bin/env python

''' @package notifytools.notifiers.smtp '''

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

from mailer import Mailer, Message
from datetime import datetime

from notifyTools.notifiers import Notifier

class MailNotifier(Notifier):
    ''' an RSS output object '''

    def __init__(self, sender, recipients, subject, mailhost):
        ''' @param[in] feed title
            @param[in] feed description
        '''
        self.sender = sender
        self.recipients = recipients
        self.subject = subject
        self.mailhost = mailhost
        self.notifications = []



    def formatNotification(self, notification):
        ''' ::param notifications: provides a text representation of the
                                   given notficiation
        '''
        return '''* %(title)s (%(date)s) *

Link: %(link)s
%(date)s''' % (notification)

    def notify(self):
        ''' publishs the rss feed at the given url
            @param[in] fname
            @param[in] url
        '''
        if not self.notifications:
            return

        message = Message(From=self.sender,
                          To=self.recipients,
                          Subject=self.subject)
        message.Body = '\n\n'.join( map(self.formatNotification, 
                                        self.notifications) )
        Mailer(self.mailhost).send(message)
        self.notifiers = []

