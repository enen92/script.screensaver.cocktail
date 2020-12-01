# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

import xbmcgui
from resources.lib.common_cocktail import ADDON_PATH, COCKTAIL_API, ACTION_RETURN, ACTION_ESCAPE


# Window controls
INGREDIENT_LABEL = 32609
INGREDIENT_THUMB = 32610
INGREDIENT_DESCRIPTION = 32611


class Ingredientdetails(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
        self.ingredient_title = kwargs['data']['name']
        self.ingredient_thumb = kwargs['data']['thumb']
        self.ingredient_description = kwargs['data']['description']


    def onInit(self):
        self.getControl(INGREDIENT_LABEL).setLabel(self.ingredient_title)
        self.getControl(INGREDIENT_THUMB).setImage(self.ingredient_thumb)
        self._set_ingredient_description()


    def _set_ingredient_description(self):
        description = COCKTAIL_API.Search().ingredient(self.ingredient_title)
        if description:
            self.getControl(INGREDIENT_DESCRIPTION).setText(description)
        else:
            self.getControl(INGREDIENT_DESCRIPTION).setText(self.ingredient_description)


    def onAction(self,action):
        if action.getId() == ACTION_RETURN or action.getId() == ACTION_ESCAPE:
            self.close()


def start(name, thumb, description):
    argm = str([name, thumb, description])
    ingrdts = Ingredientdetails(
        'script-cocktail-ingredientdetails.xml',
        ADDON_PATH,
        'default',
        '',
        data = {
            'name': name,
            'thumb': thumb,
            'description': description
        }
    )
    ingrdts.doModal()
    del ingrdts
