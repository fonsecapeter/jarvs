# -*- Mode: Python; coding: utf-8; indent-tabs-mode: spaces; tab-width: 2 -*-
### BEGIN LICENSE
# Copyright (C) 2016 Peter <peter.nfonseca@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import optparse

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611

import builder
builder.main() 

from jarvs import JarvsWindow

from jarvs_lib import set_up_logging, get_version

def parse_options():
  """Support for command line options"""
  parser = optparse.OptionParser(version="%%prog %s" % get_version())
  parser.add_option(
    "-v", "--verbose", action="count", dest="verbose",
    help=_("Show debug messages (-vv debugs jarvs_lib also)"))
  (options, args) = parser.parse_args()

  set_up_logging(options)

def main():
  'constructor for your class instances'
  parse_options()

  # Run the application.       
  window = JarvsWindow.JarvsWindow()
  window.show()
  Gtk.main()
