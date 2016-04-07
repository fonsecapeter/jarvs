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

from gi.repository import Pango
from gi.repository import Gtk, Gdk # pylint: disable=E0611
import logging
logger = logging.getLogger('jarvs')

from jarvs_lib import Window
from jarvs.AboutJarvsDialog import AboutJarvsDialog
from jarvs.PreferencesJarvsDialog import PreferencesJarvsDialog
import jarvisms
import rvsdata


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

        ##self.background_rgba = self.hex_to_rgba(rvsdata.background_color)        
        ##self.background_color = Gdk.RGBA(self.background_rgba)
        ##self.conversation.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.background_color = Gdk.RGBA()
        self.background_color.parse(rvsdata.background_color)
        self.user_color = Gdk.RGBA()
        self.user_color.parse(rvsdata.user_color)
        self.jarvs_color = Gdk.RGBA()
        self.jarvs_color.parse(rvsdata.jarvs_color)
        
        self.conversation.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.input.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.input.override_color(Gtk.StateType.NORMAL, self.user_color)
        self.conversation.override_color(Gtk.StateType.NORMAL, self.jarvs_color)
        
        self.jarvs_say(jarvisms.greeting_1())
        self.jarvs_say(jarvisms.greeting_2())

    # Gui Events
    # ---------------------------------------------------------------------
    def on_runbutton_clicked(self, widget, data = None):
        print "run pressed"

    def on_emailbutton_clicked(self, widget, data = None):
        print "email pressed"

    def on_visualizebutton_clicked(self, widget, data = None):
        print "visualize pressed"

    def on_input_activate(self, widget, data = None):
        self.input_content = self.input.get_text()
        self.user_say(self.input_content)

    # Implicit Helper Methods
    # ---------------------------------------------------------------------
    def jarvs_say(self, text):
        self.conversation.set_editable(True)
        buffer = self.conversation.get_buffer()
        buffer.insert(buffer.get_end_iter(), text + "\n")
        self.conversation.set_editable(False)

    def user_say(self, text):            
        self.conversation.set_editable(True)
        buffer = self.conversation.get_buffer()
        buffer.insert(buffer.get_end_iter(), text + "\n")
        self.input.set_text("")
        self.conversation.set_editable(False)

    # Explicit Helper Methods
    # ---------------------------------------------------------------------
    def hex_to_rgba(self, value):
        value = value.lstrip("#")
        if len(value) == 3:
            value = "".join*([v*2 for v in list(value)])
        (r1, g1, b1, a1) = tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))+(1,)
        (r1, g1, b1, a1) = (r1/255.00000, g1/255.00000, b1/255.00000, a1)

        return (r1, g1, b1, a1)
