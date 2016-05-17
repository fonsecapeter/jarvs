# -*- Mode: Python; coding: utf-8; indent-tabs-mode: spaces; tab-width: 2 -*-
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

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.jarvs.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from locale import gettext as _

import logging
logger = logging.getLogger('jarvs')

from jarvs_lib.PreferencesDialog import PreferencesDialog

import rvsdata

class PreferencesJarvsDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesJarvsDialog"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesJarvsDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        ###settings = Gio.Settings("net.launchpad.jarvs")
        ###widget = self.builder.get_object('example_entry')
        ###settings.bind("example", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.

