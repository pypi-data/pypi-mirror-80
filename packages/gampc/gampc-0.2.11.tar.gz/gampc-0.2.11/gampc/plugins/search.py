# coding: utf-8
#
# Graphical Asynchronous Music Player Client
#
# Copyright (C) 2015 Itaï BEN YAACOV
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


from gi.repository import Gtk

import ampd

from gampc import plugin
from gampc.utils import action
from gampc.utils import omenu

import songlist


class Search(songlist.SongListWithEditDelFile):
    title = _("Search")
    name = 'search'
    key = '3'

    duplicate_test_columns = ['Title', 'Artist', 'Performer', 'Date']

    sortable = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget = self.get_child()
        self.remove(widget)

        self.entry = Gtk.SearchEntry(visible=True)
        self.entry.connect('activate', self.entry_activate_cb)
        self.entry.connect('focus-in-event', self.entry_focus_cb)
        self.entry.connect('focus-out-event', self.entry_focus_cb)
        self.field_choice = Gtk.ComboBoxText(visible=True)
        self.field_choice.append_text(_("any field"))
        for name in self.fields.names:
            self.field_choice.append_text(name)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, visible=True)
        box.add(widget)
        box.add(self.entry)
        self.add(box)

        self.connect('map', self.action_search_cb)
        self.actions.add_action(action.Action('search', self.action_search_cb))

    def action_search_cb(self, *args):
        self.entry.grab_focus()

    @ampd.task
    async def client_connected_cb(self, client):
        while True:
            self.entry.activate()
            await self.ampd.idle(ampd.DATABASE)

    def action_reset_cb(self, action, parameter):
        super().action_reset_cb(action, parameter)
        self.field_choice.set_active(0)
        self.entry.activate()

    @ampd.task
    async def entry_activate_cb(self, entry):
        query = entry.get_text()
        if not query:
            return
        if query[0] == '!':
            query = query[1:]
            find = True
        else:
            find = False
        condition = sum((['any', s] if '=' not in s else s.split('=', 1) for s in self.parse(query)), [])
        if condition:
            songs = await (self.ampd.find if find else self.ampd.search)(*condition)
            self.set_records(songs)

    def entry_focus_cb(self, entry, event):
        self.shared.enable_fragile_accels = not event.in_
        return False

    @staticmethod
    def parse(s):
        token = None
        for c in s:
            if token is None:
                if c.isspace():
                    continue
                else:
                    token = ''
                    quote = False
                    escape = False
            if escape:
                token += c
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                quote = not quote
            elif c.isspace() and not quote:
                yield token
                token = None
            else:
                token += c
        if token is not None:
            if quote:
                raise ValueError(_("Unbalanced quotes"))
            yield token


class SearchExtension(plugin.Extension):
    modules = [Search]

    def activate(self):
        self.provides['app'] = {}
        self.provides['app']['menubar_items'] = [omenu.Item('20#edit/90#search/10', 'mod.search', _("Search"), ['<Control><Shift>f'])]
