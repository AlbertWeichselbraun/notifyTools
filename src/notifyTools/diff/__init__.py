#!/usr/bin/env python

""" @package notifyTools.diff
    provides helper routines for text comparison
"""
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

from difflib import Differ

class TextDiff(object):
    '''
    Compares text objects
    '''

    def __init__(self, source, dest):
        d = Differ()
        old = source.split("\n")
        new = dest.split("\n")

        self.new_lines = [ t[2:] for t in d.compare(old, new) if t.startswith("+ ") 
                                                              or t.startswith("- ") ]
        self.old_lines = [ t[2:] for t in d.compare(old,new) if t.startswith("  ") ]


    def get_change_text(self):
        ''' ::returns: the changed text '''
        return "\n".join(self.new_lines)


    def get_change_percentage(self):
        ''' ::returns: the percentag of the text that has changed '''
        return float(len(self.new_lines)) / (len(self.new_lines) + len(self.old_lines))

