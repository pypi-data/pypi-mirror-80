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


from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Peas
import sys
import os
import asyncio

import ampd

from .utils import config
from .utils.logger import logger


class AppShared(GObject.Object):
    want_to_connect = GObject.Property(type=bool, default=False)
    restricted = GObject.Property(type=bool, default=False)
    dark = GObject.Property(type=bool, default=False)
    enable_fragile_accels = GObject.Property(type=bool, default=True)
    server_label = GObject.Property(type=str, default='')
    server_profile = GObject.Property(type=str)

    CONFIG_EDIT_DIALOG_SIZE = 'edit-dialog-size'
    SEPARATOR_FILE = 'separator.mp3'
    STICKER_PROPERTIES = ('restricted', 'dark')

    def __init__(self):
        super().__init__()
        self.uidefs = {}
        self.excepthook_orig, sys.excepthook = sys.excepthook, self.excepthook

        self.ampd_client = ampd.ClientGLib()
        self.ampd_client.connect('client-connected', self.client_connected_cb)
        self.ampd_client.connect('client-disconnected', self.client_disconnected_cb)
        self.ampd_server_properties = ampd.ServerPropertiesGLib(self.ampd_client)
        self.ampd_server_properties.connect('server-error', self.server_error_cb)
        for option in ampd.OPTION_NAMES:
            self.ampd_server_properties.connect('notify::' + option, self.notify_option_cb)
        self.ampd_server_properties.connect('notify::updating-db', self.set_server_label)

        self.ampd_host = None
        self.ampd_port = 6600
        self.ampd = self.ampd_client.executor.sub_executor()

        self.peas_engine = Peas.Engine.get_default()
        self.peas_engine.enable_loader('python3')
        self.peas_extension_set = Peas.ExtensionSet.new(self.peas_engine, Peas.Activatable, [], [])
        self.peas_engine.add_search_path(os.path.join(os.path.dirname(__file__), 'plugins'))
        self.peas_engine.rescan_plugins()

        self.config = config.ConfigDict.load('config')

        LOCAL_HOST = _("Local host")
        self.config.server.access('profiles',
                                  [
                                      {
                                          'name': LOCAL_HOST,
                                          'host': 'localhost',
                                          'port': 6600,
                                      },
                                  ])
        self.connect('notify::server-profile', self.ampd_connect)
        self.dynamic_profiles = dict()
        self.server_profile = self.config.server.access('profile', LOCAL_HOST)

        self.separator_song = {'file': self.SEPARATOR_FILE}
        self.connect('notify', self.notify_sticker_cb)
        self.connect('notify::restricted', self.notify_restricted_cb)
        self.connect('notify::dark', self.notify_dark_cb)

    def __del__(self):
        logger.debug('Deleting {}'.format(self))

    def close(self):
        logger.debug("Closing shared")
        self.config.save()
        self.want_to_connect = False
        self.ampd_client.close()
        sys.excepthook = self.excepthook_orig
        del self.excepthook_orig
        self.disconnect_by_func(self.notify_restricted_cb)
        self.disconnect_by_func(self.notify_dark_cb)
        self.disconnect_by_func(self.notify_sticker_cb)
        self.disconnect_by_func(self.ampd_connect)
        self.ampd_server_properties.disconnect_by_func(self.set_server_label)
        del self.peas_extension_set
        del self.ampd_client
        del self.ampd_server_properties

    def build_ui(self, uiname):
        if uiname in self.uidefs:
            uidef = self.uidefs[uiname]
        else:
            uidef = open(os.path.join(os.path.dirname(__file__), uiname + '.ui')).read()
            self.uidefs[uiname] = uidef
        builder = Gtk.Builder(translation_domain='gampc')
        builder.add_from_string(uidef)
        return builder

    def client_connected_cb(self, client):
        logger.info(_("Connected to {profile} [protocol version {protocol}]").format(profile=self.config.server.profile, protocol=self.ampd.get_protocol_version()))
        self.idle_database()
        self.idle_sticker()
        # self.idle_debug()

    @ampd.task
    async def client_disconnected_cb(self, client, reason, message):
        self.separator_song.clear()
        self.separator_song['file'] = self.SEPARATOR_FILE
        if reason == ampd.Client.DISCONNECT_RECONNECT:
            return
        elif reason == ampd.Client.DISCONNECT_PASSWORD:
            logger.error(_("Invalid password for {}").format(self.config.server.profile))
            return
        elif reason == ampd.Client.DISCONNECT_FAILED_CONNECT:
            logger.error(_("Connection to {} failed: {}").format(self.config.server.profile, message or _("reason unknown")))
        else:
            logger.info(_("Disconnected from {}").format(self.config.server.profile))
        if self.want_to_connect:
            reply = await self.ampd.idle(ampd.CONNECT, timeout=1)
            if reply & ampd.TIMEOUT:
                self.ampd_client.connect_to_server(self.ampd_host, self.ampd_port)

    def server_error_cb(self, client, error):
        logger.error(_("Server error: {error}").format(error=error))

    @ampd.task
    async def notify_option_cb(self, properties, param):
        if self.restricted:
            await getattr(self.ampd, param.name)(0)

    @staticmethod
    def notify_restricted_cb(self, param):
        if self.restricted:
            for option in ampd.OPTION_NAMES:
                self.ampd_server_properties.set_property(option, False)

    @staticmethod
    def notify_dark_cb(self, param):
        css = Gtk.CssProvider.get_named('Adwaita', 'dark' if self.dark else None)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    @staticmethod
    @ampd.task
    async def notify_sticker_cb(self, param):
        if param.name in self.STICKER_PROPERTIES:
            try:
                await self.ampd.sticker_set('song', self.SEPARATOR_FILE, param.name, str(self.get_property(param.name)))
            except ampd.errors.ReplyError:
                pass

    @ampd.task
    async def idle_database(self):
        while True:
            song = await self.ampd.find('file', self.SEPARATOR_FILE)
            if song:
                self.separator_song.update(song[0])
            else:
                GLib.idle_add(self.separator_missing)
            await self.ampd.idle(ampd.DATABASE)
            logger.info(_("Database changed"))

    def separator_missing(self):
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text=_("Some features require a file named '{separator}' at the music root directory.  Such a file, consisting of a three second silence, is provided.").format(separator=self.SEPARATOR_FILE))
        dialog.run()
        dialog.destroy()
        return GLib.SOURCE_REMOVE

    @ampd.task
    async def idle_debug(self):
        import time
        import gc
        import pprint
        import types
        context = GLib.MainContext.default()
        while True:
            await self.ampd.idle(0, timeout=1)
            t1 = time.time()
            dispatched = context.iteration(False)
            t2 = time.time()
            await asyncio.sleep(0)
            t3 = time.time()
            print("Iteration: {} tasks {} {} / {}".format(len(asyncio.Task.all_tasks()), (t2 - t1) * 1000, (t3 - t2) * 1000, dispatched))
            continue
            tasks = []
            for t in asyncio.Task.all_tasks():
                tasks.append(repr((t.done(), t, id(t)))[1:-1])
                if t.done():
                    print(t)
                    for f in gc.get_referrers(t):
                        if isinstance(f, types.FrameType):
                            print(f.f_lineno, f.f_code.co_filename)
                        else:
                            pprint.pprint((type(f), f))
                        f = None
                    print()
                t = None
            tasks.sort()
            print('\n'.join(tasks))
            print()

    @ampd.task
    async def idle_sticker(self):
        while True:
            self.handler_block_by_func(self.notify_sticker_cb)
            try:
                stickers = await self.ampd.sticker_list('song', self.SEPARATOR_FILE)
            except ampd.errors.ReplyError:
                stickers = []
            pdict = dict(stricker.split('=', 1) for stricker in stickers)
            for key in self.STICKER_PROPERTIES:
                self.set_property(key, pdict.get(key) == 'True')
            self.handler_unblock_by_func(self.notify_sticker_cb)
            await self.ampd.idle(ampd.STICKER)

    def ampd_connect(self, *args):
        self.want_to_connect = True
        self.config.server.profile = self.server_profile
        self.set_server_label()
        if self.server_profile in self.dynamic_profiles:
            self.ampd_host = self.dynamic_profiles[self.server_profile].server
            self.ampd_port = self.dynamic_profiles[self.server_profile].port
        else:
            for profile in self.config.server.profiles:
                if profile['name'] == self.server_profile:
                    self.ampd_host = profile['host']
                    self.ampd_port = profile['port']
                    break
            else:
                return
        self.ampd_client.connect_to_server(self.ampd_host, self.ampd_port)

    def ampd_disconnect(self, *args):
        self.want_to_connect = False
        asyncio.ensure_future(self.ampd_client.disconnect_from_server())
        self.set_server_label()

    def set_server_label(self, *args):
        if self.want_to_connect:
            self.server_label = self.config.server.profile
            if self.ampd_server_properties.updating_db:
                self.server_label += " [{}]".format(_("database update"))
        else:
            self.server_label = ''

    @staticmethod
    def excepthook(*args):
        if args[0] == ampd.errors.ReplyError:
            logger.error(args[1])
        else:
            logger.error(args[1], exc_info=args)
        try:
            del sys.last_type, sys.last_value, sys.last_traceback
        except AttributeError:
            pass

    def collect_plugin_provides(self, targets):
        provides = {}
        self.peas_extension_set.foreach(self.collect_plugin_provides_worker, targets, provides)
        return provides

    @staticmethod
    def collect_plugin_provides_worker(extension_set, info, extension, targets, provides):
        for target, target_provides in extension.provides.items():
            if target in targets:
                for key, value in target_provides.items():
                    key_provides = provides.setdefault(key, [])
                    key_provides += value

    def get_extension(self, name):
        return self.peas_extension_set.get_extension(self.peas_engine.get_plugin_info(name))
