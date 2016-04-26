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
from jarvs.AttendingsDialog import AttendingsDialog
import jarvisms
import subprocess # Popopen, PIPE
import rvsdata
import RVS_vis


# See jarvs_lib.Window.py for more details about how this class works
class JarvsWindow(Window):
    __gtype_name__ = "JarvsWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JarvsWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJarvsDialog
        self.PreferencesDialog = PreferencesDialog
        self.AttendingsDialog = AttendingsDialog

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

    def on_email_activate(self, widget, data=None):
        self.email()

    def on_test_email_activate(self, widget, data=None):
        self.test_email()   

    def on_mnu_report_activate(self, widget, data=None):
        self.report()

    def on_mnu_visual_activate(self, widget, data=None):
        self.vis()

    def on_mnu_preferences_activate(self, widget, data=None):
        self.set_preferences()

    def on_mnu_attendings_activate(self, widget, data=None):
        self.set_attendings()
        reload(rvsdata)

    # Implicit Helper Methods
    # ---------------------------------------------------------------------
    def jarvs_say(self, text):
        self.conversation.set_editable(True)
        self.conversation_buffer = self.conversation.get_buffer()
        self.conversation_buffer.insert(self.conversation_buffer.get_end_iter(), text + "\n")
        
        self.conversation.set_editable(False)
        self.conversation.scroll_mark_onscreen(self.conversation_buffer.get_insert())

    def set_preferences(self):
            prefs = self.PreferencesDialog()
            prefs.run()
            prefs.destroy()
            reload(rvsdata)
            self.update_colors()

    def set_attendings(self):
            attends = self.AttendingsDialog()
            attends.run()
            attends.destroy()

    def user_test_say(self, text):
        self.conversation.set_editable(True)
        self.conversation_buffer = self.conversation.get_buffer()
        self.conversation_buffer.insert_with_tags(self.conversation_buffer.get_end_iter(), text, self.user_tag)

        self.entry_buffer.set_text("")
        self.conversation.set_editable(False)
        self.conversation.scroll_mark_onscreen(self.conversation_buffer.get_insert())

        self.interpret(text)

    def update_colors(self):
        # define colors
        self.no_color = Gdk.RGBA(255,255, 255,0)
        self.background_color = Gdk.RGBA()
        self.background_color.parse(rvsdata.background_color)
        self.user_color = Gdk.RGBA()
        self.user_color.parse(rvsdata.user_color)
        self.jarvs_color = Gdk.RGBA()
        self.jarvs_color.parse(rvsdata.jarvs_color)
        
        # define widget colors
        self.conversation.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.conversation.override_color(Gtk.StateType.NORMAL, self.jarvs_color)
        self.user_tag.set_property("foreground", rvsdata.user_color)

        self.entry_test.override_background_color(Gtk.StateType.NORMAL, self.background_color)
        self.entry_test.override_color(Gtk.StateType.NORMAL, self.user_color)

    def end_jarvs(self):
        self.jarvs_say(jarvisms.signoff())
        time.sleep(1)
        Gtk.main_quit()

    # Implicit RVS Bash Script Calls
    # ---------------------------------------------------------------------
	def vis(self):
        self.jarvs_say("")
        self.jarvs_say("No problem, let me crunch the numbers.")
        self.jarvs_say("I'll show you a slick bar-chart of the most recent report.")

        RVS_vis.main()

	def report(self):
        self.jarvs_say("")
        self.jarvs_say("No problem, I'll just pop into" + rvsdata.root_dir + " and have a look around.")
        self.jarvs_say("I'll generate a report of all the RVSs currently waiting for approval in ~/.jarvs/RVS_report.csv.")
        self.jarvs_say("Just ask if you'd like me to visualize that data.")

    	pipe = subprocess.Popen(["bash ~/.jarvs/RVS_reporter.sh"], shell=True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

	def email(self):
        self.jarvs_say("")
        self.jarvs_say("Time to lay down the hammer, eh? I'll send an email directly to each attending that has any outstatnding RVSs.")
		pipe = subprocess.Popen(["bash ~/.jarvs/RVS_emailer.sh"], shell = True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

	def test_email(self):
        self.jarvs_say("")
        self.jarvs_say("I'll take a look and see which attendings have any outstanding RVSs. I'll email you this time, but just ask if you want me to email the attendings diretly")
		pipe = subprocess.Popen(["bash ~/.jarvs/RVS_test_emailer.sh"], shell = True, stdout=subprocess.PIPE).stdout
        self.jarvs_say("")
        self.jarvs_say(pipe.read())

    # Command Interpretation
    # ---------------------------------------------------------------------
    def interpret(self, command):
        if 'vis' in command:
	        self.vis()
        elif 'report' in command:
	        self.report()
        elif 'email' in command:
            if 'test' in command:
                self.test_email()
            else:
                self.email()
        elif 'attendings' in command:
            self.set_attendings()
        elif 'preferences' in command:
            self.set_preferences()
        elif 'bye' in command:
	        self.end_jarvs()
        # conversational only
        elif 'thank' in command:
	        self.jarvs_say(jarvisms.yourewelcome())
        elif 'you' in command:
	        self.jarvs_say(jarvisms.thankyou())
        else:
	        self.jarvs_say(jarvisms.response())
            
