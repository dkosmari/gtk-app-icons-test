#!/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import os
import gi
import inspect

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Pango", "1.0")
from gi.repository import Gtk, Gdk, Gio, Pango


"""
Usage:
    ./main.py
    ./main.py light
    ./main.py dark
"""


def get_gtk_version():
    return "{}.{}.{}".format(Gtk.get_major_version(),
                             Gtk.get_minor_version(),
                             Gtk.get_micro_version())


class App(Gtk.Application):

    def add_icon(self, icon_name, notes):
        self.grid.attach(Gtk.Label(label = icon_name),
                         0, self.current_row, 1, 1)
        self.grid.attach(Gtk.Image(icon_name = icon_name,
                                   icon_size = Gtk.IconSize.LARGE),
                         1, self.current_row, 1, 1)
        self.grid.attach(Gtk.Label(label = inspect.cleandoc(notes),
                                   halign = Gtk.Align.START,
                                   ellipsize = Pango.EllipsizeMode.END),
                         2, self.current_row, 1, 1)

        self.current_row += 1


    def add_gficon(self, filename, notes):
        self.grid.attach(Gtk.Label(label = filename),
                         0, self.current_row, 1, 1)
        f = Gio.File.new_for_path(filename)
        icon = Gio.FileIcon.new(f)
        self.grid.attach(Gtk.Image(gicon = icon,
                                   icon_size = Gtk.IconSize.LARGE),
                         1, self.current_row, 1, 1)
        self.grid.attach(Gtk.Label(label = inspect.cleandoc(notes),
                                   halign = Gtk.Align.START,
                                   ellipsize = Pango.EllipsizeMode.END),
                         2, self.current_row, 1, 1)

        self.current_row += 1


    def do_activate(self):

        self.grid = Gtk.Grid(column_spacing = 12,
                             row_spacing = 24,
                             halign = Gtk.Align.CENTER,
                             valign = Gtk.Align.CENTER,
                             margin_top = 12,
                             margin_bottom = 12,
                             margin_start = 12,
                             margin_end = 12)

        self.current_row = 0

        self.add_icon("printer-symbolic",
                      """
                      ✅ loaded from the system/global theme
                      """)

        self.add_icon("real-printer-symbolic",
                      """
                      ❌ used filesystem search path
                      """)

        self.add_icon("resource-printer-1-symbolic",
                      """
                      ✅ used default resource path (APP_ID/icons)
                      ❌ directory structure is for unthemed icons
                      """)

        self.add_icon("resource-printer-2-symbolic",
                      """
                      ✅ used default resource path (APP_ID/icons)
                      ✅ themed directory structure
                      """)

        self.add_icon("resource-printer-3-symbolic",
                      """
                      ✅ used non-default resource path
                      ✅ non-default resource path was added to IconTheme
                      ✅ themed directory structure
                      """)

        self.add_icon("real-target-symbolic",
                      """
                      ❌ used filesystem search path
                      """)

        self.add_icon("resource-target-symbolic",
                      """
                      ✅ used default resource path (APP_ID/icons)
                      ✅ themed directory structure
                      ✅ using symbolic colors
                      """)

        self.add_icon("resource-target-mono-symbolic",
                      """
                      ✅ used default resource path (APP_ID/icons)
                      ✅ themed directory structure
                      ✅ one color
                      """)

        self.add_gficon("icons/real-printer-symbolic.svg",
                        """
                        ❓ used Gio.FileIcon, depends on GTK 4 version,
                        works on 4.14, fails on 4.10, using {} right now
                        """.format(get_gtk_version()))

        win = Gtk.ApplicationWindow(application = app,
                                    child = self.grid)
        win.present()


if __name__ ==  "__main__":

    settings = Gtk.Settings.get_default()
    if "light" in sys.argv[1:]:
        settings.set_property("gtk-application-prefer-dark-theme", False)
    if "dark" in sys.argv[1:]:
        settings.set_property("gtk-application-prefer-dark-theme", True)

    theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())

    base_path = os.path.dirname(os.path.realpath(__file__))


    # This method does not search sub-directories, and does not recolor.
    theme.add_search_path(base_path + "/icons")


    try:
        resource = Gio.Resource.load(base_path + "/icons.gresource")
    except:
        print("icons.gresource not loaded, did you compile it?")
        sys.exit(1)

    Gio.resources_register(resource)


    # Gtk.Application will search for resource icons under APP_ID/icons/ automatically.


    # Resource paths that are not APP_ID/icons must be included explicitly.
    theme.add_resource_path("/some/random/path")


    app = App(application_id = "org.gtk.app_icons_test",
              flags = Gio.ApplicationFlags.NON_UNIQUE)
    app.run()
