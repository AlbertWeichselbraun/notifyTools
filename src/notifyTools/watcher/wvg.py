#!/usr/bin/env python

''' 
    @package notifyTools.watcher.wvg
    checks whether new linux kernel versions are available
'''

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


import urllib
from re import compile
import datetime
from operator import itemgetter
from pyquery import PyQuery 
from lxml import etree

from notifyTools.watcher import Watcher

RE_WHITESPACE = compile("\s{2,}")

clean = lambda txt: RE_WHITESPACE.sub(" ", txt.encode("utf8")).strip()

class WVG(Watcher):
    ''' linux watcher main class '''
   
    @staticmethod
    def getTextContent(input_content):
        '''
        ::param input_text: 
        ::returns: the text representation used for the diff of the
                   given content
        '''
        page = PyQuery(input_content)
        content = []
        for top_info in map(PyQuery, page('.top-caption')):
            top_title   = clean(top_info('.top-title').text())
            top_details = clean(top_info('.top-details').text())
            top_price   = clean(top_info('.top-price').text())

            content.append("# %s\n- %s\n- %s\n" % (top_title, 
                                                   top_details, 
                                                   top_price))
        return '\n'.join(content)


if __name__ == '__main__':
    pass
    # html = open('tests/21Leo2').read()
