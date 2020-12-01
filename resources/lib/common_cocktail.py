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
import thecocktaildb
import os

addon = xbmcaddon.Addon(id='script.screensaver.cocktail')
addon_path = addon.getAddonInfo('path')
addon_userdata = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
addon_name = addon.getAddonInfo('name')
cocktailsdb_api = thecocktaildb.Api('1352')
favourite_drinks_folder = os.path.join(addon_userdata,'favourites')

if not os.path.exists(addon_userdata): xbmcvfs.mkdir(addon_userdata)
if not os.path.exists(favourite_drinks_folder): xbmcvfs.mkdir(favourite_drinks_folder)


ACTION_CONTEXT_MENU = 117
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_ESCAPE = 10
ACTION_RETURN = 92
ACTION_ENTER = 7


def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))

def translate(text):
    return addon.getLocalizedString(text).encode('utf-8')
