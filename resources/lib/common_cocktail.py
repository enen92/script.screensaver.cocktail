# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

import xbmc
import xbmcaddon
import xbmcvfs
import os

from resources.lib import thecocktaildb

ADDON = xbmcaddon.Addon(id='script.screensaver.cocktail')
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_USERDATA = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')
ADDON_NAME = ADDON.getAddonInfo('name')
FAVOURITE_DRINK_FOLDER = os.path.join(ADDON_USERDATA, 'favourites')
MEDIA_FOLDER = os.path.join(ADDON_PATH, "resources", "skins", "default", "media")
MENU_ITEMS_FOLDER = os.path.join(ADDON_PATH, "resources", "skins", "default", "media", "menuicons")
NOT_AVAILABLE_ICON = os.path.join(MENU_ITEMS_FOLDER, "notavailable.png")

COCKTAIL_API = thecocktaildb.Api('1352')

ACTION_CONTEXT_MENU = 117
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_ESCAPE = 10
ACTION_RETURN = 92
ACTION_ENTER = 7


def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))


def init_folders():
    if not os.path.exists(ADDON_USERDATA):
        xbmcvfs.mkdir(ADDON_USERDATA)

    if not os.path.exists(FAVOURITE_DRINK_FOLDER):
        xbmcvfs.mkdir(FAVOURITE_DRINK_FOLDER)
