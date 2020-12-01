# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

import os
import xbmc
import thecocktaildb
from common_cocktail import *

def add_to_favourite_drinks(drink_name,drink_id,drink_image):
    content = drink_name + '|' + str(drink_id) + '|' + drink_image
    filename = os.path.join(favourite_drinks_folder,str(drink_id)+'.txt')
    save(filename,content)
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(32000), translate(32022),1,os.path.join(addon_path,"icon.png")))
    return


def remove_from_favourites(drink_id):
    filename = os.path.join(favourite_drinks_folder,str(drink_id)+'.txt')
    if os.path.exists(filename):
        os.remove(filename)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(32000), translate(32023),1,os.path.join(addon_path,"icon.png")))
    else:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(32000), translate(32024),1,os.path.join(addon_path,"icon.png")))
    return


def has_favourites():
    drinks = os.listdir(favourite_drinks_folder)
    if drinks:
        return True
    else:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(32000), translate(32026),1,os.path.join(addon_path,"icon.png")))
        return False


def is_favourite(drink_id):
    filename = os.path.join(favourite_drinks_folder,str(drink_id) + '.txt')
    if os.path.exists(filename): return True
    else: return False


def get_favourites():
    favourite_cocktails = []
    drinks = os.listdir(favourite_drinks_folder)
    if drinks:
        for drink in drinks:
            drink_file = os.path.join(favourite_drinks_folder,drink)
            drink_info = readfile(drink_file).split('|')
            drink_dict = { "idDrink" : drink_info[1], "strDrink" : drink_info[0], "strDrinkThumb": drink_info[2] }
            favourite_cocktails.append(thecocktaildb.Cocktail_lite(drink_dict ))
    return favourite_cocktails

def save(filename,contents):
    with open(filename, 'w') as fh:
        fh.write(contents)


def readfile(filename):
    with open(filename, "r") as f:
        string = f.read()
        return string
