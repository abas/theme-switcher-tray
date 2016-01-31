#!/usr/bin/python
from gi.repository import Gtk
import os
import dbus


bus = dbus.SessionBus()
remote_object = bus.get_object("org.xfce.Xfconf",  # Connection name
                               "/org/xfce/Xfconf")  # Object's path

iface = dbus.Interface(remote_object, "org.xfce.Xfconf")


class SwitcherTray(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_icon_name("emblem-system-symbolic")
        self.set_visible(True)
        self.set_has_tooltip(True)
        self.set_tooltip_text("Quick switch theme")
        self.connect("activate", self.on_icon_clicked)
        self.connect("popup-menu", self.on_icon_rclicked)
        self.traySettings = SwitcherSettings()
        self.About = AboutDialog()

    def on_icon_clicked(self, event):
        self.Menu = Gtk.Menu()

        devmode = Gtk.MenuItem()
        devmode.connect("activate", self.dev_clicked)
        devmode.set_label("Developer Mode")
        self.Menu.append(devmode)

        usermode = Gtk.MenuItem()
        usermode.connect("activate", self.normal_clicked)
        usermode.set_label("Normal Mode")
        self.Menu.append(usermode)

        self.Menu.show_all()
        self.Menu.popup(None,
                        None,
                        Gtk.StatusIcon.position_menu,  # position function
                        self,  # data to be passed to position function
                        0,
                        Gtk.get_current_event_time())  # this method must use () or it will error

    def on_icon_rclicked(self, icon, button, time):
        self.Menu = Gtk.Menu()

        setting = Gtk.MenuItem()
        setting.connect("activate", self.settings_clicked)
        setting.set_label("Settings")
        self.Menu.append(setting)

        about = Gtk.MenuItem()
        about.connect("activate", self.about_clicked)
        about.set_label("About")
        self.Menu.append(about)
        self.Menu.show_all()

        def pos(menu, icon):
            return Gtk.StatusIcon.position_menu(menu, icon)

        self.Menu.popup(None, None, pos, self, button, time)

    @staticmethod
    def dev_clicked(user_data):
        dev = [iface.GetProperty('tealinux', '/switcher/DevTheme'),
               iface.GetProperty('tealinux', '/switcher/DevWindow'),
               iface.GetProperty('tealinux', '/switcher/DevIcon')]

        iface.SetProperty('xsettings', '/Net/ThemeName', dev[0])
        iface.SetProperty('xfwm4', '/general/theme', dev[1])
        iface.SetProperty('xsettings', '/Net/IconThemeName', dev[2])

    @staticmethod
    def normal_clicked(user_data):
        normal = [iface.GetProperty('tealinux', '/switcher/NormalTheme'),
                  iface.GetProperty('tealinux', '/switcher/NormalWindow'),
                  iface.GetProperty('tealinux', '/switcher/NormalIcon')]

        iface.SetProperty('xsettings', '/Net/ThemeName', normal[0])
        iface.SetProperty('xfwm4', '/general/theme', normal[1])
        iface.SetProperty('xsettings', '/Net/IconThemeName', normal[2])

    def about_clicked(self, user_data):
        self.About.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.About.show_all()

    def settings_clicked(self, user_data):
        self.traySettings.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.traySettings.window.show_all()


class AboutDialog(Gtk.AboutDialog):
    def __init__(self):
        Gtk.AboutDialog.__init__(self)
        self.set_destroy_with_parent(True)
        self.set_name("Theme Switcher")
        self.set_version("0.0.1")
        self.set_authors(["Nurul Irfan"])
        self.set_program_name("Theme Switcher")
        self.set_copyright("CC-BY-SA")
        self.set_comments("Quick way to switch theme")
        self.connect("delete-event", self.on_window_destroy)
        self.connect("response", self.on_window_destroy)  # when 'close' button clicked

    def on_window_destroy(self, *args):
        self.hide()
        return True


class SwitcherSettings:
    path = "switcher.ui"

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.path)
        self.window = self.builder.get_object("settings_window")
        self.window.connect("delete-event", self.on_window_destroy)
        self.cancel = self.builder.get_object("cancel")
        self.cancel.connect("clicked", self.on_cancel_clicked)
        self.ok = self.builder.get_object("ok")
        self.ok.connect("clicked", self.on_ok_clicked)

        global iface
        self.iface = iface

        self.current_gtk_theme_dev = self.iface.GetProperty('tealinux', '/switcher/DevTheme')
        self.current_window_theme_dev = self.iface.GetProperty('tealinux', '/switcher/DevWindow')
        self.current_icon_theme_dev = self.iface.GetProperty('tealinux', '/switcher/DevIcon')

        self.current_gtk_theme_normal = self.iface.GetProperty('tealinux', '/switcher/NormalTheme')
        self.current_window_theme_normal = self.iface.GetProperty('tealinux', '/switcher/NormalWindow')
        self.current_icon_theme_normal = self.iface.GetProperty('tealinux', '/switcher/NormalIcon')

        self.new_combo('combobox_dev_gtk',
                       self.get_themes,
                       self.current_gtk_theme_dev,
                       self.on_gtk_dev_changed)
        self.new_combo('combobox_dev_window',
                       self.get_window,
                       self.current_window_theme_dev,
                       self.on_window_dev_changed)
        self.new_combo('combobox_dev_icon',
                       self.get_icons,
                       self.current_icon_theme_dev,
                       self.on_icon_dev_changed)

        self.new_combo('combobox_normal_gtk',
                       self.get_themes,
                       self.current_gtk_theme_normal,
                       self.on_gtk_normal_changed)
        self.new_combo('combobox_normal_window',
                       self.get_window,
                       self.current_window_theme_normal,
                       self.on_window_normal_changed)
        self.new_combo('combobox_normal_icon',
                       self.get_icons,
                       self.current_icon_theme_normal,
                       self.on_icon_normal_changed)

        self.window.set_keep_above(True)
        # self.window.show_all()

    def new_combo(self, combo_name, get_type_function, current, callback_changed):
        list_store = Gtk.ListStore(int, str)
        themes = get_type_function()  # get all available themes / icon (depend on type)
        item_id = 0  # set id for iteration
        for item in themes:  # iterate through available themes
            list_store.append([item_id, item])  # append themes to list
            # print(item_id, item)
            item_id += 1
        combo = self.builder.get_object(combo_name)  # get ComboBox from the ui file
        combo.set_model(list_store)  # set ComboBox's model
        cell = Gtk.CellRendererText()  # create new CellRendererText to place the model on ComboBox
        combo.pack_start(cell, True)  #
        combo.add_attribute(cell, 'text', 1)  # add value to ComboBox with 'cell', type 'text' and column 1 of model
        combo.connect("changed", callback_changed)  # connect signal when the selected value is changed
        active = 0
        # print("current = ", current)
        for s in list_store:  # =================
            if s[1] == current:  # get list item's id
                combo.set_active(active)  # set default value from database
            else:
                active += 1

    @staticmethod
    def check_valid_theme(path):
        if os.path.exists(os.path.join(path, "gtk-2.0")) and os.path.exists(os.path.join(path, "gtk-3.0")):
            return True
        else:
            return False

    @staticmethod
    def check_valid_icon(path):
        if os.path.exists(os.path.join(path, "index.theme")):
            return True
        else:
            return False

    @staticmethod
    def check_valid_window(path):
        if os.path.exists(os.path.join(path, "xfwm4")):
            return True
        else:
            return False

    def get_themes(self):
        valid = []
        dir_ = "/usr/share/themes"
        if os.path.isdir(dir_):
            for theme in os.listdir(dir_):
                if self.check_valid_theme(os.path.join(dir_, theme)):
                    valid.append(theme)
        return valid

    def get_window(self):
        valid = []
        dir_ = "/usr/share/themes"
        if os.path.isdir(dir_):
            for theme in os.listdir(dir_):
                if self.check_valid_window(os.path.join(dir_, theme)):
                    valid.append(theme)
        return valid

    def get_icons(self):
        valid = []
        dir_ = "/usr/share/icons"
        if os.path.isdir(dir_):
            for theme in os.listdir(dir_):
                if self.check_valid_icon(os.path.join(dir_, theme)):
                    valid.append(theme)
        return valid

    def on_gtk_dev_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_gtk_theme_dev = model[tree_iter][1]

    def on_icon_dev_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_icon_theme_dev = model[tree_iter][1]

    def on_window_dev_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_window_theme_dev = model[tree_iter][1]

    def on_gtk_normal_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_gtk_theme_normal = model[tree_iter][1]

    def on_icon_normal_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_icon_theme_normal = model[tree_iter][1]

    def on_window_normal_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            model = combobox.get_model()
            self.current_window_theme_normal = model[tree_iter][1]

    def on_cancel_clicked(self, user_data):
        self.window.hide()

    def on_ok_clicked(self, user_data):
        self.iface.SetProperty('tealinux', '/switcher/DevTheme', self.current_gtk_theme_dev)
        self.iface.SetProperty('tealinux', '/switcher/DevWindow', self.current_window_theme_dev)
        self.iface.SetProperty('tealinux', '/switcher/DevIcon', self.current_icon_theme_dev)

        self.iface.SetProperty('tealinux', '/switcher/NormalTheme', self.current_gtk_theme_normal)
        self.iface.SetProperty('tealinux', '/switcher/NormalWindow', self.current_window_theme_normal)
        self.iface.SetProperty('tealinux', '/switcher/NormalIcon', self.current_icon_theme_normal)
        self.window.hide()

    def on_window_destroy(self, *args):
        self.window.hide()
        return True  # if not returned True, all children will be destroyed

    def __del__(self):
        print("window deleted")


SwitcherTray()
Gtk.main()
