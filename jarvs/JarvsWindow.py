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
from jarvs.PreferencesDialog import PreferencesDialog
import jarvisms
import rvsdata
import subprocess # Popopen, PIPE


# See jarvs_lib.Window.py for more details about how this class works
class JarvsWindow(Window):
    __gtype_name__ = "JarvsWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JarvsWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJarvsDialog
        self.PreferencesDialog = PreferencesDialog     

        # define colors
        self.no_color = Gdk.RGBA(255,255, 255,0)
        self.background_color = Gdk.RGBA()
        self.background_color.parse(rvsdata.background_color)
        self.user_color = Gdk.RGBA()
        self.user_color.parse(rvsdata.user_color)
        self.jarvs_color = Gdk.RGBA()
        self.jarvs_color.parse(rvsdata.jarvs_color)
        
        # initialize widgits and edit appearance
        self.conversation = self.builder.get_object("conversation_main") 
        self.conversation.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.conversation.override_color(Gtk.StateType.NORMAL, self.jarvs_color)
        self.conversation.set_border_width(4)
        self.conversation_buffer = self.conversation.get_buffer()
        self.user_tag = self.conversation_buffer.create_tag("user", foreground = rvsdata.user_color)

        self.mainvbox = self.builder.get_object("box_main")
        self.scrolledconversationwindow = self.builder.get_object("scrolledwindow_main")

        self.entry_test = self.builder.get_object("entry_test")
        self.entry_test.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.entry_test.override_color(Gtk.StateType.NORMAL, self.user_color)
        self.entry_test.connect("key-release-event", self.on_entry_test_key_release)

        # greet user on startup
        self.jarvs_say(jarvisms.greeting_1())
        self.jarvs_say(jarvisms.greeting_2())

    # Gui Events
    # ---------------------------------------------------------------------
    def on_entry_test_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Return: # if Return pressed, reset text
            self.entry_buffer = self.entry_test.get_buffer()
            self.entry_text = self.entry_buffer.get_text(self.entry_buffer.get_start_iter(), self.entry_buffer.get_end_iter(), False)
            self.user_test_say(self.entry_text)

    def on_mnu_report_activate(self, widget, data=None):
        self.report()

    # Implicit Helper Methods
    # ---------------------------------------------------------------------
    def jarvs_say(self, text):
        self.conversation.set_editable(True)
        self.conversation_buffer = self.conversation.get_buffer()
        self.conversation_buffer.insert(self.conversation_buffer.get_end_iter(), text + "\n")
        
        self.conversation.set_editable(False)
        self.conversation.scroll_mark_onscreen(self.conversation_buffer.get_insert())

    def user_test_say(self, text):
        self.conversation.set_editable(True)
        self.conversation_buffer = self.conversation.get_buffer()
        self.conversation_buffer.insert_with_tags(self.conversation_buffer.get_end_iter(), text, self.user_tag)

        self.entry_buffer.set_text("")
        self.conversation.set_editable(False)
        self.conversation.scroll_mark_onscreen(self.conversation_buffer.get_insert())

        self.interpret(text)

    def end_jarvs():
        self.jarvs_say(jarvisms.signoff())
        time.sleep(1)
        Gtk.main_quit()

    # Implicit RVS Bash Script Calls
    # ---------------------------------------------------------------------
	def vis(self):
        self.jarvs_say("")
        self.jarvs_say("No problem, let me crunch the numbers.")
        self.jarvs_say("I'll show you all the rvs's waiting for approval since the last full report.")
        self.jarvs_say("I won't log the data on this one.")

		pipe = subprocess.Popen(["python", "./jarvs/RVS_vis.py"], stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

	def report(self):
        self.jarvs_say("")
        self.jarvs_say("No problem, let me crunch the numbers.")
        self.jarvs_say("I'll show you all the practice rvs's currently waiting for approval.")
        self.jarvs_say("I will log the data on this one.")

    	pipe = subprocess.Popen(["./jarvs/RVS_reporter.sh"], shell=True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

	def email(self):
		pipe = subprocess.Popen(["./jarvs/RVS_emailer.sh"], shell = True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

	def test_email(self):
		pipe = subprocess.Popen(["./jarvs/RVS_test_emailer.sh"], shell = True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

    # Command Interpretation
    # ---------------------------------------------------------------------
    def interpret(self, command):
        if 'vis' in command:
	        self.vis()
        elif 'report' in command:
	        self.report()
        ##elif 'email' in command:
        ##    if 'test' in command:
        ##    else:
        elif 'bye' in command:
	        self.end_jarvs()
        # conversational only
        elif 'thank' in command:
	        self.jarvs_say(jarvisms.yourewelcome())
        elif 'you' in command:
	        self.jarvs_say(jarvisms.thankyou())
        else:
	        self.jarvs_say(jarvisms.response())
            
