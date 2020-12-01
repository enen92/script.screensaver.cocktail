# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''
import xbmc
import sys
import xbmcgui
from resources.lib.common_cocktail import *

class ScreensaverPreview(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):
        self.exit_monitor = self.ExitMonitor(self.exit)
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.ContextMenu", "id": 1}')

    def exit(self):
        self.close()
        # Call the screensaver asynchronously and die
        xbmc.executebuiltin('RunAddon(script.screensaver.cocktail)')

if __name__ == '__main__':
    if not xbmc.getCondVisibility('Window.IsActive(script-cocktail-Cocktailplayer.xml)'):
        #Start preview window
        screensaver = ScreensaverPreview(
            'script-cocktail-preview.xml',
            addon_path,
            'default',
            '',
        )
        screensaver.doModal()
        xbmc.sleep(100)
        del screensaver

    else:
        sys.exit(0)
