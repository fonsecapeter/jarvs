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

from gi.repository import Gtk # pylint: disable=E0611

from jarvs_lib.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('jarvs')

import rvsdata

class PreferencesDialog(Gtk.Dialog):
  __gtype_name__ = "PreferencesDialog"

  def __new__(cls):
    """Special static method that's automatically called by Python when 
    constructing a new instance of this class.
    
    Returns a fully instantiated PreferencesDialog object.
    """
    builder = get_builder('PreferencesDialog')
    new_object = builder.get_object('preferences_dialog')
    new_object.finish_initializing(builder)
    return new_object

  def finish_initializing(self, builder):
    """Called when we're finished initializing.

    finish_initalizing should be called after parsing the ui definition
    and creating a PreferencesDialog object with it in order to
    finish initializing the start of the new PreferencesDialog
    instance.
    """
    # Get a reference to the builder and set up the signals.
    self.builder = builder
    self.ui = builder.get_ui(self)

    self.set_title("Jarvs Preferences")
    
    self.user_name_entry = builder.get_object("user_name_entry")
    self.user_name_entry.set_text(rvsdata.user_name)


    self.user_email_entry = builder.get_object("user_email_entry")
    self.user_email_entry.set_text(rvsdata.user_email)


    self.root_dir_entry = builder.get_object("root_dir_entry")
    self.root_dir_entry.set_text(rvsdata.root_dir)

    self.user_color_entry = builder.get_object("user_color_entry")
    self.user_color_entry.set_text(rvsdata.user_color)

    self.jarvs_color_entry = builder.get_object("jarvs_color_entry")
    self.jarvs_color_entry.set_text(rvsdata.jarvs_color)

    self.background_color_entry = builder.get_object("background_color_entry")
    self.background_color_entry.set_text(rvsdata.background_color)

  def on_btn_ok_clicked(self, widget, data=None):
    """The user has elected to save the changes.

    Called before the dialog returns Gtk.ResponseType.OK from run().
    """
    rvsdata.update_user_name(self.user_name_entry.get_text().rstrip())
    rvsdata.update_user_email(self.user_email_entry.get_text().rstrip())
    rvsdata.update_user_color(self.user_color_entry.get_text().rstrip())
    rvsdata.update_jarvs_color(self.jarvs_color_entry.get_text().rstrip())
    rvsdata.update_background_color(self.background_color_entry.get_text().rstrip())
    rvsdata.update_root_dir(self.root_dir_entry.get_text().rstrip())

  def on_btn_cancel_clicked(self, widget, data=None):
    """The user has elected cancel changes.

    Called before the dialog returns Gtk.ResponseType.CANCEL for run()
    """
    pass


if __name__ == "__main__":
  dialog = PreferencesDialog()
  dialog.show()
  Gtk.main()
