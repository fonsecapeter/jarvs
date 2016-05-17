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

class AttendingsDialog(Gtk.Dialog):
  __gtype_name__ = "AttendingsDialog"

  def __new__(cls):
    """Special static method that's automatically called by Python when 
    constructing a new instance of this class.
    
    Returns a fully instantiated AttendingsDialog object.
    """
    builder = get_builder('AttendingsDialog')
    new_object = builder.get_object('attendings_dialog')
    new_object.finish_initializing(builder)
    return new_object

  def finish_initializing(self, builder):
    """Called when we're finished initializing.

    finish_initalizing should be called after parsing the ui definition
    and creating a AttendingsDialog object with it in order to
    finish initializing the start of the new AttendingsDialog
    instance.
    """
    # Get a reference to the builder and set up the signals.
    self.builder = builder
    self.ui = builder.get_ui(self)

    # access entry pane objects
    self.id_label = builder.get_object("id_label")
    self.fname_entry = builder.get_object("fname_entry")
    self.lname_entry = builder.get_object("lname_entry")
    self.dirname_entry = builder.get_object("dirname_entry")
    self.email_entry = builder.get_object("email_entry")

    # build treeview and store        
    self.attendings_treeview = builder.get_object("attendings_treeview") # view
    self.attendings_store = Gtk.ListStore(int, str, str) # model
    self.populate_attendings_store()
    self.attendings_treeview.set_model(self.attendings_store)
    
    # render store in treeview
    for i, column_title in enumerate(["ID", "First Name", "Last Name"]):
      renderer = Gtk.CellRendererText()
      column = Gtk.TreeViewColumn(column_title, renderer, text = i)
      self.attendings_treeview.append_column(column)

    # get reference to treeview selection
    self.select = self.attendings_treeview.get_selection()
    self.select.connect("changed", self.on_attendings_treeview_selection_changed)

  # Gui Events
  # ---------------------------------------------------------------------
  def on_btn_ok_clicked(self, widget, data=None):
    """The user has elected to save the changes.

    Called before the dialog returns Gtk.ResponseType.OK from run().
    """
    self.save_attendings()

  def on_btn_cancel_clicked(self, widget, data=None):
    """The user has elected cancel changes.

    Called before the dialog returns Gtk.ResponseType.CANCEL for run()
    """
    pass

  def on_btn_delete_clicked(self, widget, data=None):
    self.delete_attending()

  def on_attendings_treeview_selection_changed(self, selection):
    model, treeiter = selection.get_selected()
    if treeiter != None:
      selection = model[treeiter][0]
      self.populate_entry_fields(selection)


  # Implicit Helper Methods
  # ---------------------------------------------------------------------
  def populate_attendings_store(self):
    for Attending_ID in range(rvsdata.attending_ids[-1] + 1):
      try:
        self.attendings_store.append([rvsdata.attending_ids[Attending_ID], rvsdata.attending_fnames[Attending_ID], rvsdata.attending_lnames[Attending_ID]])
      except:
        pass
    self.attendings_store.append([len(self.attendings_store), "+", ""])

  def populate_entry_fields(self, selection):
    if selection < len(rvsdata.attending_ids):
      self.id_label.set_text(str(rvsdata.attending_ids[selection]))
      self.fname_entry.set_text(rvsdata.attending_fnames[selection])
      self.lname_entry.set_text(rvsdata.attending_lnames[selection])
      self.dirname_entry.set_text(rvsdata.attending_dirnames[selection])
      self.email_entry.set_text(rvsdata.attending_emails[selection])
    else:
      self.id_label.set_text(str(selection))
      self.fname_entry.set_text("First Name")
      self.lname_entry.set_text("Last Name")
      self.dirname_entry.set_text("Directory Name")
      self.email_entry.set_text("Email")

  def delete_attending(self):
      current_attending_id = int(self.id_label.get_text())
      # TODO: Add a popup dialog asking for confirmation
      rvsdata.delete_attending(current_attending_id)
      reload(rvsdata)

  def save_attendings(self):
      current_attending_id = int(self.id_label.get_text())
      new_attending_fname = self.fname_entry.get_text()
      new_attending_lname = self.lname_entry.get_text()
      new_attending_dirname = self.dirname_entry.get_text()
      new_attending_email = self.email_entry.get_text()

      # update existing row in db if editting existing attending
      # ASSUMPTION: attending_id's sorted and greatest integer value id is at last position of array
      #   okay because: only creating new attenidng if at (last attenidng id) + 1
      if current_attending_id <= rvsdata.attending_ids[-1]:
        rvsdata.update_attending_fname(new_attending_fname, current_attending_id)
        rvsdata.update_attending_lname(new_attending_lname, current_attending_id)
        rvsdata.update_attending_dirname(new_attending_dirname, current_attending_id)
        rvsdata.update_attending_email(new_attending_email, current_attending_id)
      # insert new attending if not
      else:
        rvsdata.insert_new_attending(new_attending_fname, new_attending_lname, new_attending_dirname, new_attending_email)
        reload(rvsdata)

if __name__ == "__main__":
  dialog = AttendingsDialog()
  dialog.show()
  Gtk.main()
