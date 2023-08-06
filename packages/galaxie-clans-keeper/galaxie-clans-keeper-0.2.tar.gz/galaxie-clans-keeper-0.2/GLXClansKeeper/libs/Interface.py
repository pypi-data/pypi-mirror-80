#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Clans Keeper Team, all rights reserved

import GLXCurses
from GLXClansKeeper import __version__
import sys


class Interface(object):
    def __init__(self):
        self.menu = GLXCurses.MenuBar()
        self.menu.info_label = "Galaxie Clans Keeper v{0}".format(__version__)

        self.main_win = GLXCurses.Window()

        self.application = GLXCurses.Application()

        self.application.add_window(self.main_win)
        self.application.menubar = self.menu

    def start(self):  # pragma: no cover
        GLXCurses.MainLoop().run()
        sys.exit(0)
