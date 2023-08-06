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


from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import PeasGtk
import logging
import dbus
import asyncio
import gbulb
import zeroconf as zeroconf_  # conflict with handler keyword argument
import ampd

from . import window
from . import shared
from . import __program_name__, __version__, __program_description__, __copyright__, __license__
from .utils import omenu
from .utils import action
from .utils import ssde
from .utils.logger import logger


ZEROCONF_MPD_TYPE = '_mpd._tcp.local.'


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='begnac.gampc', flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)

        self.add_main_option('list-actions', 0, GLib.OptionFlags.NONE, GLib.OptionArg.NONE, _("List application actions"), None)
        self.add_main_option('version', 0, GLib.OptionFlags.NONE, GLib.OptionArg.NONE, _("Display version"), None)
        self.add_main_option('copyright', 0, GLib.OptionFlags.NONE, GLib.OptionArg.NONE, _("Display copyright"), None)
        self.add_main_option('non-unique', ord('u'), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, _("Do not start a unique instance"), None)
        self.add_main_option('debug', ord('d'), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, _("Debug messages"), None)
        self.add_main_option(GLib.OPTION_REMAINING, 0, GLib.OptionFlags.NONE, GLib.OptionArg.STRING_ARRAY, '', _("[ACTION...]"))

    def __del__(self):
        logger.debug('Deleting {}'.format(self))

    def run(self, argv):
        try:
            super().run(argv)
        except KeyboardInterrupt:
            pass

    def do_handle_local_options(self, options):
        if options.contains('non-unique'):
            self.set_flags(self.get_flags() | Gio.ApplicationFlags.NON_UNIQUE)
        if options.contains('debug'):
            logging.getLogger().setLevel(logging.DEBUG)
        if options.contains('version'):
            print(_("{program} version {version}").format(program=__program_name__, version=__version__))
        elif options.contains('copyright'):
            print(__copyright__)
            print(__license__)
        elif options.contains('list-actions'):
            self.register()
            for name in sorted(self.list_actions()):
                print(name)
        else:
            return -1
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)
        logger.debug("Starting")
        gbulb.install()
        asyncio.events._set_running_loop(asyncio.get_event_loop())
        self.shared = shared.AppShared()
        self.shared.connect('notify::enable-fragile-accels', self.notify_enable_fragile_accels_cb)

        self.ampd = self.shared.ampd.sub_executor()
        self.shared.ampd_client.connect('client-connected', self.idle_output)
        # self.shared.ampd_client.connect('client-connected', self.idle_partition)

        self.notification = Gio.Notification.new(_("MPD status"))
        self.notification_task = None

        self.session_inhibit_cookie = None
        self.systemd_inhibit_fd = None
        self.shared.ampd_server_properties.connect('notify::state', self.set_inhibit)
        self.shared.connect('notify::restricted', self.set_inhibit)

        self.add_action(action.Action('new-window', self.new_window_cb))
        self.add_action(action.Action('close-window', self.close_window_cb))
        self.add_action(action.Action('new-module', self.new_module_cb, parameter_type=GLib.VariantType.new('s')))
        self.add_action(action.Action('close-module', self.close_module_cb))
        self.add_action(action.Action('help', self.help_cb))
        self.add_action(action.Action('about', self.about_cb))
        self.add_action(action.Action('notify', self.task_hold_app(self.action_notify_cb)))
        self.add_action(action.Action('quit', self.quit))
        self.add_action(action.Action('edit-profiles', self.edit_profiles_cb))
        # self.add_action(action.Action('add-partition', self.add_partition_cb))
        self.add_action(action.Action('manage-plugins', self.action_manage_plugins_cb))

        # self.add_action(action.Action('BAD', self.THIS_IS_BAD_cb))

        self.output_ids = []

        menubar = omenu.OrderedMenu(self.set_accels_for_action)
        self.set_menubar(menubar)
        menubar.insert_path('10#gampc', Gio.MENU_LINK_SUBMENU, _("_GAMPC"))
        menubar.insert_path('10#gampc/10#window/10', 'app.new-window', _("New window"), ['<Control>n'])
        menubar.insert_path('10#gampc/10#window/20', 'app.close-window', _("Close window"), ['<Control>w'])
        menubar.insert_path('10#gampc/10#window/30', 'win.toggle-fullscreen', _("Fullscreen window"), ['<Alt>f'])
        menubar.insert_path('10#gampc/10#window/40', 'win.volume-popup', _("Adjust volume"), ['<Alt>v'])
        menubar.insert_path('10#gampc/90#app/50', 'app.quit', _("Quit"), ['<Control>q'])
        menubar.insert_path('10#gampc/99#BAD/10', 'app.BAD', "BAD", ['<Control><Alt>z'])
        menubar.insert_path('20#edit', Gio.MENU_LINK_SUBMENU, _("_Edit"))
        menubar.insert_path('30#playback', Gio.MENU_LINK_SUBMENU, _("_Playback"))
        menubar.insert_path('40#server', Gio.MENU_LINK_SUBMENU, _("_Server"))
        self.output_menu = menubar.insert_path('40#server/30#output', Gio.MENU_LINK_SECTION, _("Outputs (<Ctrl> to toggle)"))
        # menubar.insert_path('40#server/40#connection/25#partitions', Gio.MENU_LINK_SUBMENU, _("_Partitions"))
        # self.partition_menu = menubar.insert_path('40#server/40#connection/25#partitions/10#partitions', Gio.MENU_LINK_SECTION)
        # menubar.insert_path('40#server/40#connection/25#partitions/20', 'app.add-partition', _("Add a partition"))
        menubar.insert_path('40#server/40#connection/30#profiles', Gio.MENU_LINK_SUBMENU, _("_Profiles"))
        self.dynamic_profile_menu = menubar.insert_path('40#server/40#connection/30#profiles/10#profiles', Gio.MENU_LINK_SECTION)
        self.dynamic_profile_menu_setup()
        self.profile_menu = menubar.insert_path('40#server/40#connection/30#profiles/20#profiles', Gio.MENU_LINK_SECTION)
        self.profile_menu_setup()
        menubar.insert_path('40#server/40#connection/30#profiles/30/10', 'app.edit-profiles', _("Edit profiles"))
        menubar.insert_path('50#modules', Gio.MENU_LINK_SUBMENU, _("_Modules"))
        menubar.insert_path('50#modules/10#modules', Gio.MENU_LINK_SECTION, _("Press <Ctrl> for a new instance"))
        menubar.insert_path('50#modules/20#current/10', 'app.close-module', _("Close module"), ['<Control><Shift>w'])
        menubar.insert_path('90#help', Gio.MENU_LINK_SUBMENU, _("_Help"))
        menubar.insert_path('90#help/10', 'app.help', _("Help"), hidden_when=None)
        menubar.insert_path('90#help/20', 'app.about', _("About"))

        self.shared.app_menu = self.app_menu = omenu.OrderedMenu()
        self.app_menu.insert_path('10#window/10', 'app.new-window', _("New window"), ['<Control>n'])
        self.app_menu.insert_path('10#window/20', 'app.close-window', _("Close window"), ['<Control>w'])
        self.app_menu.insert_path('20#help/10', 'app.help', _("Help"), hidden_when=None)
        self.app_menu.insert_path('20#help/20', 'app.about', _("About"))
        self.app_menu.insert_path('30#plugins/20', 'app.manage-plugins', _("Manage plugins"))
        self.app_menu.insert_path('90#quit/10', 'app.quit', _("Quit"), ['<Control>q'])

        self.module_classes = {}
        self.modules = []

        self.shared.peas_extension_set.connect_after('extension-added', self.peas_extension_added_cb)
        self.shared.peas_extension_set.connect('extension-removed', self.peas_extension_removed_cb)
        self.shared.peas_engine.set_loaded_plugins(['base', 'current', 'playqueue', 'browser', 'search', 'savedsearch', 'playlist', 'tanda', 'command', 'log', 'tango-velours', 'stream'])

    def do_command_line(self, command_line):
        options = command_line.get_options_dict().end().unpack()
        if GLib.OPTION_REMAINING in options:
            for option in options[GLib.OPTION_REMAINING]:
                try:
                    success, name, target = Gio.Action.parse_detailed_name(option)
                except Exception as e:
                    logger.error(e)
                    continue
                if not self.has_action(name):
                    logger.error(_("Action '{name}' does not exist").format(name=name))
                else:
                    self.activate_action(name, target)
        else:
            self.activate()
        return 0

    def do_activate(self, *args):
        win = self.get_active_window()
        if win:
            win.present()
        else:
            self.new_window_cb(None, None)

    def do_shutdown(self):
        logger.debug("Shutting down")
        asyncio.events._set_running_loop(None)
        for module in self.modules:
            module.destroy()
        self.shared.disconnect_by_func(self.notify_enable_fragile_accels_cb)
        self.shared.ampd_server_properties.disconnect_by_func(self.set_inhibit)
        self.shared.disconnect_by_func(self.set_inhibit)
        self.shared.peas_engine.set_loaded_plugins([])
        self.shared.close()
        for name in self.list_actions():
            self.remove_action(name)
        self.set_menubar()
        self.dynamic_profile_menu_cleanup()
        Gtk.Application.do_shutdown(self)

    def task_hold_app(self, f):
        def g(*args, **kwargs):
            retval = f(*args, **kwargs)
            if isinstance(retval, asyncio.Future):
                self.hold()
                retval.add_done_callback(lambda future: self.release())
            return retval
        return g

    def notify_enable_fragile_accels_cb(self, shared, param):
        if shared.enable_fragile_accels:
            self.get_menubar().enable_fragile_accels()
        else:
            self.get_menubar().disable_fragile_accels()

    def peas_extension_added_cb(self, extension_set, info, extension):
        extension.shared = self.shared
        extension.activate()
        for module in extension.modules:
            self.register_module_class(module)
        provides = extension.provides.get('app', {})
        for item in provides.get('menubar_items', []):
            self.get_menubar().insert(item)
        for action_ in provides.get('actions', []):
            self.add_action(action_.create_action(self.task_hold_app, shared=self.shared) if isinstance(action_, action.ActionModel) else action_)

    def peas_extension_removed_cb(self, extension_set, info, extension):
        provides = extension.provides.get('app', {})
        for action_ in provides.get('actions', []):
            self.remove_action(action_.get_name())
        for item in reversed(provides.get('menubar_items', [])):
            self.get_menubar().remove_path(item.path)
        for module in extension.modules:
            self.unregister_module_class(module)
        extension.deactivate()
        del extension.shared

    def register_module_class(self, module_class):
        if module_class.name in self.module_classes:
            module_class.replace = self.module_classes[module_class.name]
            self.unregister_module_class(self.module_classes[module_class.name], restore=False)
        self.module_classes[module_class.name] = module_class
        self.get_menubar().insert_path('50#modules/10#modules/' + module_class.key,
                                       'app.new-module("{}")'.format(module_class.name),
                                       module_class.title,
                                       accels=['<Alt>' + module_class.key, '<Control><Alt>' + module_class.key])

    def unregister_module_class(self, module_class, restore=True):
        del self.module_classes[module_class.name]
        self.get_menubar().remove_path('50#modules/10#modules/' + module_class.key)
        if restore and module_class.replace:
            self.register_module_class(module_class.replace)
            module_class.replace = None

    def new_module_cb(self, action, parameter):
        self.start_module(parameter.unpack(), Gdk.Keymap.get_default().get_modifier_state() & Gdk.ModifierType.CONTROL_MASK, False)

    def close_module_cb(self, action, parameter):
        win = self.get_active_window()
        old_module = win.module
        if old_module is None:
            return
        for module in self.modules:
            if not module.win:
                win.change_module(module)
                break
        else:
            win.change_module(None)
        old_module.destroy()
        self.modules.remove(old_module)

    def new_window_cb(self, action, parameter):
        self.start_module('current', False, True)

    def close_window_cb(self, action, parameter):
        self.get_active_window().destroy()

    def start_module(self, name, new_instance, new_window):
        module = (not new_instance and self.pop_named_module(name)) or self.module_classes[name](self.shared)
        self.modules.append(module)
        win = None if new_window else module.win or self.get_active_window()
        if win is None:
            win = window.Window(self)
        if module.win is None:
            win.change_module(module)
        win.present()

    def pop_named_module(self, name):
        for module in self.modules:
            if module.name == name:
                self.modules.remove(module)
                return module
        return None

    def quit(self, *args):
        logger.debug("Quit")
        for win in self.get_windows():
            win.destroy()
        return True

    def about_cb(self, *args):
        dialog = Gtk.AboutDialog(parent=self.get_active_window(), program_name=__program_name__, version=__version__, comments=__program_description__, copyright=__copyright__, license_type=Gtk.License.GPL_3_0, logo_icon_name='face-cool', website='http://math.univ-lyon1.fr/~begnac', website_label=_("Author's website"))
        dialog.run()
        dialog.destroy()

    def help_cb(self, *args):
        return
        builder = Gtk.Builder()
        win = Gtk.ShortcutsWindow(title='hhh')
        section = Gtk.ShortcutsSection(section_name='a', title='b')
        group = Gtk.ShortcutsGroup(title='yyy')
        shortcut = Gtk.ShortcutsShortcut(title='fwr')
        win.add_child(builder, section, None)
        section.add_child(builder, group, None)
        group.add_child(builder, shortcut, None)
        win.present()
        self.hold()

    def edit_profiles_cb(self, *args):
        struct = ssde.List(
            label=_("Profiles"),
            substruct=ssde.Dict(
                label=_("Profile"),
                substructs=[
                    ssde.Text(name='name', label=_("Name")),
                    ssde.Text(name='host', label=_("Host")),
                    ssde.Integer(name='port', label=_("Port"), default=6600, min_value=0),
                ]))
        value = struct.edit(self.get_active_window(),
                            self.shared.config.server.profiles,
                            self.shared.config.server.access(self.shared.CONFIG_EDIT_DIALOG_SIZE, [500, 500]))
        if value:
            self.shared.config.server.profiles = value
            self.profile_menu_setup()

    def profile_menu_setup(self):
        self.profile_menu.remove_all()
        for profile in self.shared.config.server.profiles:
            self.profile_menu.append(profile['name'], 'app.server-profile("{name}")'.format_map(profile))

    def dynamic_profile_menu_setup(self):
        self.dynamic_profile_browser = zeroconf_.ServiceBrowser(zeroconf_.Zeroconf(), ZEROCONF_MPD_TYPE, handlers=[self.dynamic_profile_menu_handler])

    def dynamic_profile_menu_cleanup(self):
        self.dynamic_profile_browser.cancel()
        del self.dynamic_profile_browser

    def dynamic_profile_menu_handler(self, zeroconf, service_type, name, state_change):
        print(service_type, name, state_change)
        info = zeroconf.get_service_info(service_type, name)
        if name.endswith(ZEROCONF_MPD_TYPE):
            name = name[:-len(ZEROCONF_MPD_TYPE) - 1]
        if ' @ ' in name:
            name = name.split(' @ ', 1)[1]
        if state_change == zeroconf_.ServiceStateChange.Added:
            self.shared.dynamic_profiles[name] = info
            self.dynamic_profile_menu.insert_path(name, 'app.server-profile("{}")'.format(name), name)
            if name == self.shared.server_profile and not self.shared.ampd.get_is_connected():
                GLib.timeout_add(0, self.shared.ampd_connect)
        elif state_change == zeroconf_.ServiceStateChange.Removed:
            if name == self.shared.server_profile and not self.shared.ampd.get_is_connected():
                GLib.timeout_add(0, self.shared.ampd_disconnect)
            self.dynamic_profile_menu.remove_path(name)
            del self.shared.dynamic_profiles[name]

    @ampd.task
    async def action_notify_cb(self, *args):
        if self.notification_task:
            self.notification_task._close()
            self.withdraw_notification('status')
        self.notification_task = asyncio.Task.current_task()
        await self.ampd.idle(ampd.IDLE)
        print(self.shared.ampd_server_properties.current_song)
        if self.shared.ampd_server_properties.state == 'stop':
            icon_name = 'media-playback-stop-symbolic'
            body = 'Stopped'
        else:
            if self.shared.ampd_server_properties.state == 'play':
                icon_name = 'media-playback-start-symbolic'
            else:
                icon_name = 'media-playback-pause-symbolic'
            body = '{0} / {1}'.format(self.shared.ampd_server_properties.current_song.get('Artist', '???'), self.shared.ampd_server_properties.current_song.get('Title', '???'))
            if 'performer' in self.shared.ampd_server_properties.current_song:
                body += ' / ' + self.shared.ampd_server_properties.current_song['Performer']
        self.notification.set_body(body)
        self.notification.set_icon(Gio.Icon.new_for_string(icon_name))
        self.send_notification('status', self.notification)
        await asyncio.sleep(5)
        self.withdraw_notification('status')
        self.notification_task = None

    def set_inhibit(self, *args):
        if self.shared.ampd_server_properties.state == 'play':
            self.session_inhibit_cookie = self.session_inhibit_cookie or self.inhibit(None, Gtk.ApplicationInhibitFlags.SUSPEND | Gtk.ApplicationInhibitFlags.IDLE, __program_name__)
            bus = dbus.SystemBus()
            obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
            self.systemd_inhibit_fd = self.systemd_inhibit_fd or obj.Inhibit('handle-lid-switch', __program_name__, _("Playing"), 'block', dbus_interface='org.freedesktop.login1.Manager')
        else:
            self.session_inhibit_cookie = self.session_inhibit_cookie and self.uninhibit(self.session_inhibit_cookie)
            self.systemd_inhibit_fd = None

    @ampd.task
    async def idle_output(self, client):
        for output_id in self.output_ids:
            self.remove_action('output.' + output_id)
        self.output_ids = []
        self.output_menu.remove_all()
        outputs = await self.ampd.outputs()
        for output in outputs:
            output_id = output['outputid']
            self.output_ids.append(output_id)
            self.output_menu.insert_path(output_id, 'app.output.' + output_id, output['outputname'])
            self.add_action(action.Action('output.' + output_id, self.action_output_activate_cb, state=GLib.Variant.new_boolean(int(output['outputenabled'])), restrict=True, shared=self.shared))
        while True:
            await self.ampd.idle(ampd.OUTPUT)
            outputs = await self.ampd.outputs()
            for output in outputs:
                self.lookup_action('output.' + output['outputid']).set_state(GLib.Variant.new_boolean(int(output['outputenabled'])))

    @ampd.task
    async def action_output_activate_cb(self, action, parameter):
        output_id = action.get_name().split('.', 1)[1]
        if Gdk.Keymap.get_default().get_modifier_state() & Gdk.ModifierType.CONTROL_MASK:
            await self.ampd.toggleoutput(output_id)
        elif all(map(lambda output: output['outputid'] == output_id or output['outputenabled'] == '0', await self.ampd.outputs())) and self.shared.ampd_server_properties.state == 'play':
            await self.ampd.command_list([self.ampd.pause(1), self.ampd.disableoutput(output_id), self.ampd.enableoutput(output_id), self.ampd.pause(0)])
        else:
            await self.ampd.enableoutput(output_id)
            await self.ampd.command_list(self.ampd.disableoutput(x) for x in self.output_ids if x is not output_id)

#     @ampd.task
#     async def idle_partition(self, client):
#         self.partition_menu.remove_all()
#         partitions = await self.ampd.listpartitions()
#         for partition in partitions:
#             self.partition_menu.insert_path(partition, 'app.partition.' + partition, partition)
#             self.add_action(action.Action('partition.' + partition, self.action_partition_activate_cb))
#         print(partitions)
#         print(2)
#         await self.ampd.idle(ampd.PARTITION)
#         print(1)

#     @ampd.task
#     async def add_partition_cb(self, *args):
#         label = _("New partition name")
#         new_name = "<{}>".format(label)
#         struct = ssde.Text(label=label,
#                            default=new_name,
#                            validator=lambda x: x != new_name)
#         value = await struct.edit_async(self.get_active_window())
#         if value:
#             await self.ampd.newpartition(value)
#             # await self.ampd.partition(value)

#     @ampd.task
#     async def action_partition_activate_cb(self, action, parameter):
#         partition = action.get_name().split('.', 1)[1]
#         await self.ampd.partition(partition)

    def action_manage_plugins_cb(self, action, param):
        win = Gtk.Window()
        win.add(PeasGtk.PluginManager.new(self.shared.peas_engine))
        win.show_all()
