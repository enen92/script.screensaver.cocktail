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
from common_cocktail import FAVOURITE_DRINK_FOLDER
from kodiutils import notification

def add_to_favourite_drinks(drink_name, drink_id, drink_image):
    content = "{}|{}|{}".format(drink_name, str(drink_id), drink_image)
    filename = os.path.join(FAVOURITE_DRINK_FOLDER, str(drink_id) + '.txt')
    save(filename, content)
    notification(32022)


def remove_from_favourites(drink_id):
    filename = os.path.join(FAVOURITE_DRINK_FOLDER, str(drink_id) + '.txt')
    if os.path.exists(filename):
        os.remove(filename)
        notification(32023)
    else:
        notification(32024)


def has_favourites():
    drinks = os.listdir(FAVOURITE_DRINK_FOLDER)
    if drinks:
        return True
    else:
        notification(32026)
        return False


def is_favourite(drink_id):
    return os.path.exists(
        os.path.join(
            FAVOURITE_DRINK_FOLDER, str(drink_id) + '.txt'))


def get_favourites():
    favourite_cocktails = []
    drinks = os.listdir(FAVOURITE_DRINK_FOLDER)
    if drinks:
        for drink in drinks:
            drink_file = os.path.join(FAVOURITE_DRINK_FOLDER, drink)
            drink_info = readfile(drink_file).split('|')
            drink_dict = {
                          "idDrink" : drink_info[1],
                          "strDrink" : drink_info[0],
                          "strDrinkThumb": drink_info[2]
            }
            favourite_cocktails.append(thecocktaildb.Cocktail_lite(drink_dict))
    return favourite_cocktails


def save(filename,contents):
    with open(filename, 'w') as fh:
        fh.write(contents)


def readfile(filename):
    with open(filename, "r") as f:
        string = f.read()
        return string
