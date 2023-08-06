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


from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gtk

import ampd

from gampc import plugin
from gampc.utils import action
from gampc.utils import omenu
from gampc.utils import ssde

import songlist


class PlayQueue(songlist.SongListWithTotals, songlist.SongListWithAdd):
    title = _("Play Queue")
    name = 'playqueue'
    key = '1'

    duplicate_test_columns = ['Title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions.add_action(action.Action('playqueue-high-priority', self.action_priority_cb))
        self.actions.add_action(action.Action('playqueue-normal-priority', self.action_priority_cb))
        self.actions.add_action(action.Action('playqueue-choose-priority', self.action_priority_cb))
        self.actions.add_action(action.Action('playqueue-shuffle', self.action_shuffle_cb, restrict=True, shared=self.shared))
        self.actions.add_action(action.Action('playqueue-go-to-current', self.action_go_to_current_cb))
        self.signal_handler_connect(self.shared.ampd_server_properties, 'notify::current-song', self.notify_current_song_cb)
        for name in self.actions.list_actions():
            if name.startswith('playqueue-ext-'):
                self.actions.remove(name)

    @ampd.task
    async def client_connected_cb(self, client):
        while True:
            self.set_records(await self.ampd.playlistinfo())
            await self.ampd.idle(ampd.PLAYLIST)

    def data_func(self, column, renderer, store, i, j):
        super().data_func(column, renderer, store, i, j)
        if self.shared.ampd_server_properties.state != 'stop' and store.get_record(i).Id == self.shared.ampd_server_properties.current_song.get('Id'):
            renderer.set_property('font', 'italic bold')
            bg = self._mix_colors(1, 1, 1)
            renderer.set_property('background-rgba', bg)
        else:
            renderer.set_property('font', None)
        if column.field.name == 'FormattedTime' and store.get_record(i).Prio is not None:
            bg = self._mix_colors(0, int(store.get_record(i).Prio) / 255.0, 0)
            renderer.set_property('background-rgba', bg)

    @ampd.task
    async def action_priority_cb(self, action, parameter):
        songs, refs = self.treeview.get_selection_rows()
        if not songs:
            return

        if '-choose-' in action.get_name():
            priority = sum(int(song.get('Prio', 0)) for song in songs) // len(songs)
            struct = ssde.Integer(default=priority, min_value=0, max_value=255)
            priority = await struct.edit_async(self.win)
            if priority is None:
                return
        else:
            priority = 255 if '-high-' in action.get_name() else 0
        if songs:
            await self.ampd.prioid(priority, *(song['Id'] for song in songs))

    @ampd.task
    async def action_shuffle_cb(self, action, parameter):
        await self.ampd.shuffle()

    def action_go_to_current_cb(self, action, parameter):
        if self.shared.ampd_server_properties.current_song:
            p = Gtk.TreePath.new_from_string(self.shared.ampd_server_properties.current_song['Pos'])
            self.treeview.set_cursor(p)
            self.treeview.scroll_to_cell(p, None, True, 0.5, 0.0)

    def notify_current_song_cb(self, *args):
        self.treeview.queue_draw()

    def record_new_cb(self, store, i):
        ampd.task(self.ampd.addid)(store.get_record(i).file, store.get_path(i).get_indices()[0])

    def record_delete_cb(self, store, i):
        song_id = store.get_record(i).Id
        m = int(store.get_string_from_iter(i))
        for n in range(store.iter_n_children()):
            if n != m and store.get_record(store.iter_nth_child(None, n)).Id == song_id:
                ampd.task(self.ampd.command_list)((self.ampd.swap(n, m), self.ampd.delete(m)))
                store.remove(i)
                return
        if not (self.shared.restricted and self.shared.ampd_server_properties.state == 'play' and self.shared.ampd_server_properties.current_song.get('pos') == song_id):
            ampd.task(self.ampd.deleteid)(song_id)
            store.remove(i)

    @ampd.task
    async def treeview_row_activated_cb(self, treeview, p, column):
        if not self.shared.restricted:
            await self.ampd.playid(self.store.get_record(self.store.get_iter(p)).Id)


@ampd.task
async def action_playqueue_add_replace_cb(songlist_, action, parameter):
    filenames = songlist_.get_filenames(parameter.get_boolean())
    replace = '-replace' in action.get_name()
    if replace:
        await songlist_.ampd.clear()
    await songlist_.ampd.command_list(songlist_.ampd.add(filename) for filename in filenames)
    if replace:
        await songlist_.ampd.play()


@ampd.task
async def action_playqueue_add_high_priority_cb(songlist_, action, parameter):
    filenames = songlist_.get_filenames(parameter.get_boolean())
    queue = {song['file']: song for song in await songlist_.ampd.playlistinfo()}
    Ids = []
    for filename in filenames:
        Ids.append(queue[filename]['Id'] if filename in queue else await songlist_.ampd.addid(filename))
    await songlist_.ampd.prioid(255, *Ids)


class PlayQueueExtension(plugin.Extension):
    modules = [PlayQueue]

    def activate(self):
        self.provides['app'] = {}
        self.provides['app']['menubar_items'] = [
            omenu.Item('20#edit/90#playqueue/20', 'mod.playqueue-shuffle', _("Shuffle")),
            omenu.Item('20#edit/90#playqueue/40', 'mod.playqueue-go-to-current', _("Go to current song"), ['<Control>z'])
        ]

        self.provides['songlist'] = {}
        self.provides['songlist']['actions'] = [
            action.ActionModel('playqueue-ext' + verb, action_playqueue_add_replace_cb,
                               restrict=(verb == '-replace'), parameter_type=GLib.VariantType.new('b'), shared=self.shared)
            for verb in ('-add', '-replace')
        ] + [
            action.ActionModel('playqueue-ext-add-high-priority', action_playqueue_add_high_priority_cb,
                               restrict=True, parameter_type=GLib.VariantType.new('b'), shared=self.shared)
        ]
        for name, parameter in (('context_menu_items', '(true)'), ('left_context_menu_items', '(false)')):
            self.provides['songlist'][name] = [
                omenu.Item('10/1', 'mod.playqueue-ext-add' + parameter, _("Add to play queue")),
                omenu.Item('10/2', 'mod.playqueue-ext-replace' + parameter, _("Replace play queue")),
                omenu.Item('10/3', 'mod.playqueue-ext-add-high-priority' + parameter, _("Add to play queue with high priority")),
            ]

        self.provides[PlayQueue.name] = {}
        self.provides[PlayQueue.name]['context_menu_items'] = [
            omenu.Item('90/10#priority', Gio.MENU_LINK_SUBMENU, _("Priority for random mode")),
            omenu.Item('90/10#priority/10', 'mod.playqueue-high-priority', _("High")),
            omenu.Item('90/10#priority/20', 'mod.playqueue-normal-priority', _("Normal")),
            omenu.Item('90/10#priority/30', 'mod.playqueue-choose-priority', _("Choose")),
            omenu.Item('90/30', 'mod.playqueue-shuffle', _("Shuffle")),
        ]
