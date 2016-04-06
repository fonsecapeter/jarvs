# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2016 Peter <pfonseca@mac-cloud-vm-163-239.ucsf.edu>
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

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('jarvs')

from jarvs_lib import Window
from jarvs.AboutJarvsDialog import AboutJarvsDialog
from jarvs.PreferencesJarvsDialog import PreferencesJarvsDialog

# See jarvs_lib.Window.py for more details about how this class works
class JarvsWindow(Window):
    __gtype_name__ = "JarvsWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JarvsWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJarvsDialog
        self.PreferencesDialog = PreferencesJarvsDialog

        # Code for other initialization actions should be added here.
        self.conversation = self.builder.get_object("conversation")
        self.input = self.builder.get_object("input")
        
        self.runbutton = self.builder.get_object("runbutton")
        self.emailbutton = self.builder.get_object("emailbutton")
        self.visualizebutton = self.builder.get_object("visualizebutton")
            
    def on_runbutton_clicked(self, widget, data = None):
        print "run pressed"

    def on_emailbutton_clicked(self, widget, data = None):
        print "email pressed"

    def on_visualizebutton_clicked(self, widget, data = None):
        print "visualize pressed"

    def on_input_activate(self, widget, data = None):
        input_content = widget.get_text() + "\n"
        self.conversation.set_editable(True)
        buffer = self.conversation.get_buffer()
        # get contents of buffer
        ##current_content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        # insert to buffer
        buffer.insert(buffer.get_end_iter(), input_content)
        # replace text in entry with nothing
        self.input.set_text("")
        self.conversation.set_editable(False)
        
      
