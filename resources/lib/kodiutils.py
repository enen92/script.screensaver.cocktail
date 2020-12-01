'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

import xbmc
import xbmcaddon
import xbmcgui
from contextlib import contextmanager

ADDON = xbmcaddon.Addon(id='script.screensaver.cocktail')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ICON = ADDON.getAddonInfo('icon')


def translate(text):
    return ADDON.getLocalizedString(text).encode('utf-8')


def log(message):
    try:
        xbmc.log("{}: {}".format(ADDON_NAME, message), level=xbmc.LOGDEBUG)
    except UnicodeEncodeError:
        xbmc.log("{}: {}".format(ADDON_NAME, message).encode(
            'utf-8', 'ignore'), xbmc.LOGDEBUG)

def notification(message_idx):
    xbmcgui.Dialog().notification(
        translate(32000),
        translate(message_idx),
        icon = ADDON_ICON,
        time = 1500
    )

@contextmanager
def busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    try:
        yield
    finally:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
