# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

import xbmcaddon
import xbmcgui
import xbmc
import os
from resources.lib.common_cocktail import *

#Window controls
ingredientlabel = 32609
ingredientthumb = 32610
ingredientdescription = 32611


class Ingredientdetails(xbmcgui.WindowXMLDialog):


    def __init__( self, *args, **kwargs ):
        self.info = eval(args[3])
        self.ingredient_title = self.info[0]
        self.ingredient_thumb = self.info[1]
        self.ingredient_description = self.info[2]


    def onInit(self):
        self.getControl(ingredientlabel).setLabel(self.ingredient_title)
        self.getControl(ingredientthumb).setImage(self.ingredient_thumb)
        self.setIngredientDescription()


    def setIngredientDescription(self):
        description = cocktailsdb_api.Search().ingredient(self.ingredient_title)
        if description:
            self.getControl(ingredientdescription).setText(description)
        else:
            self.getControl(ingredientdescription).setText(self.ingredient_description)


    def onAction(self,action):
        if action.getId() == ACTION_RETURN or action.getId() == ACTION_ESCAPE:
            self.close()


def start(name,thumb,description):
    argm = str([name,thumb,description])
    ingrdts = Ingredientdetails(
        'script-cocktail-ingredientdetails.xml',
        addon_path,
        'default',
        argm,
    )
    ingrdts.doModal()
    del ingrdts
