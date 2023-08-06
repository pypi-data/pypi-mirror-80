#!/usr/bin/env python
import subprocess
import os
import signal
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3


class Indicator():
    def __init__(self):
        self.app = 'Exit I3 For n00bs'
        self.exit_indicator = AppIndicator3.Indicator.new(self.app,
                                                          Gtk.STOCK_QUIT,
                                                          AppIndicator3.IndicatorCategory.OTHER)
        self.exit_indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.exit_indicator.set_menu(self.create_menu())

    def create_menu(self):
        menu = Gtk.Menu()
        item_quit = Gtk.MenuItem(label='Exit i3')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def quit(self, source):
        cmd = ["i3-msg", "exit"]
        subprocess.run(cmd)


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
