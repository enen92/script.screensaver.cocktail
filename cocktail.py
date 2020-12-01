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
import sys
import os
import urllib
from resources.lib import thecocktaildb
from resources.lib import ingredient_details
from resources.lib.common_cocktail import *
from resources.lib.kodiutils import translate

if ADDON.getSetting('ingredient-switch') == '0':
    switch_percentage = 20
elif ADDON.getSetting('ingredient-switch') == '1':
    switch_percentage = 10

# Window controls
drinklabel = 32603
drinkthumb = 32602
drinksublabel = 32604
drinkrecipe = 32606
INGREDIENT_PANEL_CONTROL = 32607
FICTIONAL_PANEL_CONTROL = 32608
BACK_BACKGROUND_CONTROL = 32609
BACK_ICON_CONTROL = 32610

# TODO: refactor all this crap
class Screensaver(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
        self.monitor = xbmc.Monitor()
        self.canceled = False
        self.mode = args[3]

        # screensaver mode?
        if self.mode:
            self.screensaver_mode = False
            self.cocktail_id = str(self.mode)
        else:
            self.screensaver_mode = True


    def onInit(self):
        # Enable back button for touch devices
        if ADDON.getSetting('enable-back') == "false":
            self.getControl(BACK_BACKGROUND_CONTROL).setVisible(False)
            self.getControl(BACK_ICON_CONTROL).setVisible(False)

        # initiate fictional controler
        ingredient = xbmcgui.ListItem('scipt.screensaver.cocktail')
        self.getControl(FICTIONAL_PANEL_CONTROL).addItem(ingredient)
        self.drink_id = 0

        if self.screensaver_mode:
            if ADDON.getSetting('enable-instructions') == 'true':
                self.setProperty("instructions", "1")
                wait_time = int(ADDON.getSetting('wait-time-instructions'))
                self.monitor.waitForAbort(wait_time)

        next_random = int(ADDON.getSetting('next-time')) * 1000

        if self.screensaver_mode:
            self.set_random()
            self.current_time = 0
            while not self.canceled:
                if self.current_time >= next_random:
                    self.set_random()
                    self.current_time = 0
                else:
                    if ((float(self.current_time)/next_random)*100) % switch_percentage == 0.0 and ((float(self.current_time)/next_random)*100) != 0.0:
                        if self.position == 0 and self.pages > 1:
                            self.clear_ingredients()
                            self.set_second_ingredients(self.cocktail_obj)
                        elif self.position == 1:
                            self.clear_ingredients()
                            if self.pages == 3:
                                self.set_third_ingredients(self.cocktail_obj)
                            else:
                                self.set_first_ingredients(self.cocktail_obj)
                        elif self.position == 2:
                            self.clear_ingredients()
                            self.set_first_ingredients(self.cocktail_obj)
                        xbmc.sleep(200)
                        self.current_time += 200
                    else:
                        xbmc.sleep(200)
                        self.current_time += 200

        else:
            self.setProperty("loading", "1")
            cocktails_list = COCKTAIL_API.Lookup().cocktail(self.cocktail_id)
            self.clearProperty("loading")
            if cocktails_list:
                self.set_cocktail(cocktails_list[0])
            else:
                xbmcgui.Dialog().ok(translate(32000),translate(32011))
                self.close()
            self.current_time = 0
            while not self.canceled:
                if ((float(self.current_time)/next_random)*100) % switch_percentage == 0.0 and ((float(self.current_time)/next_random)*100) != 0.0:
                    if self.position == 0 and self.pages > 1:
                        self.clear_ingredients()
                        self.set_second_ingredients(self.cocktail_obj)
                    elif self.position == 1:
                        self.clear_ingredients()
                        if self.pages == 3:
                            self.set_third_ingredients(self.cocktail_obj)
                        else:
                            self.set_first_ingredients(self.cocktail_obj)
                    elif self.position == 2:
                        self.clear_ingredients()
                        self.set_first_ingredients(self.cocktail_obj)
                    xbmc.sleep(200)
                    self.current_time += 200
                else:
                    xbmc.sleep(200)
                    self.current_time += 200

    def set_random(self):
        self.setProperty("loading", "1")
        cocktails_list = COCKTAIL_API.Lookup().random()
        self.clearProperty("instructions")
        if int(cocktails_list[0].id) != self.drink_id:
            self.clearProperty("loading")
            self.drink_id = int(cocktails_list[0].id)
            self.set_cocktail(cocktails_list[0])
        else:
            self.set_random()
        return

    def set_cocktail(self,cocktail):
        self.cocktail_obj = cocktail
        self.pages = 1
        self.clear_all()
        self.getControl(drinklabel).setLabel(cocktail.name)
        if cocktail.thumb:
            self.getControl(drinkthumb).setImage(cocktail.thumb)
        else:
            self.getControl(drinkthumb).setImage(os.path.join(MEDIA_FOLDER, "cocktail.jpg"))
        self.getControl(drinkrecipe).setText(cocktail.recipe)
        self.getControl(drinksublabel).setText(cocktail.category + ' - ' + cocktail.alcoholic + ' - ' + cocktail.glass)
        self.set_first_ingredients(cocktail)
        return

    def set_first_ingredients(self, cocktail):
        self.position = 0

        ingredient_list = []

        if cocktail.ingredient1.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient1)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient1))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient1))+'.png')
            if cocktail.measure1 and cocktail.measure1.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure1.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient2 and cocktail.ingredient2.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient2)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient2))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient2))+'.png')
            if cocktail.measure2 and cocktail.measure2.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure2.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient3 and cocktail.ingredient3.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient3)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient3))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient3))+'.png')
            if cocktail.measure3 and cocktail.measure3.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure3.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient4 and cocktail.ingredient4.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient4)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient4))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient4))+'.png')
            if cocktail.measure4 and cocktail.measure4.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure4.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient5 and cocktail.ingredient5.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient5)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient5))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient5))+'.png')
            if cocktail.measure5 and cocktail.measure5.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure5.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient6 and cocktail.ingredient6.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient6)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient6))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient6))+'.png')
            if cocktail.measure6 and cocktail.measure6.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure6.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        self.getControl(INGREDIENT_PANEL_CONTROL).addItems(ingredient_list)
        if cocktail.ingredient7.rstrip(): self.pages = 2
        return

    def set_second_ingredients(self,cocktail):
        self.position = 1

        ingredient_list = []

        if cocktail.ingredient7 and cocktail.ingredient7.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient7)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient7))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient7))+'.png')
            if cocktail.measure7 and cocktail.measure7.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure7.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient8 and cocktail.ingredient8.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient8)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient8))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient8))+'.png')
            if cocktail.measure8 and cocktail.measure8.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure8.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient9 and cocktail.ingredient9.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient9)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient9))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient9))+'.png')
            if cocktail.measure9 and cocktail.measure9.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure9.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient10 and cocktail.ingredient10.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient10)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient10))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient10))+'.png')
            if cocktail.measure10 and cocktail.measure10.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure10.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient11 and cocktail.ingredient11.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient11)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient11))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient11))+'.png')
            if cocktail.measure11 and cocktail.measure11.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure11.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient12 and cocktail.ingredient12.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient12)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient12))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient12))+'.png')
            if cocktail.measure12 and cocktail.measure12.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure12.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        self.getControl(INGREDIENT_PANEL_CONTROL).addItems(ingredient_list)
        if cocktail.ingredient13.rstrip(): self.pages = 3
        return

    def set_third_ingredients(self,cocktail):
        self.position = 2

        if cocktail.ingredient13 and cocktail.ingredient13.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient13)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient13))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient13))+'.png')
            if cocktail.measure13 and cocktail.measure13.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure13.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient14 and cocktail.ingredient14.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient14)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient14))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient14))+'.png')
            if cocktail.measure14 and cocktail.measure14.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure14.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)

        if cocktail.ingredient15 and cocktail.ingredient15.rstrip():
            ingredient = xbmcgui.ListItem(cocktail.ingredient15)
            ingredient.setArt({ 'thumb': 'http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient15))+'.png' })
            ingredient.setProperty('ingredient_thumb','http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient15))+'.png')
            if cocktail.measure15 and cocktail.measure15.rstrip():
                ingredient.setProperty('measure','('+cocktail.measure15.rstrip()+')')
            else: ingredient.setProperty('measure','')
            ingredient_list.append(ingredient)
        return

    def set_ingredient_description(self,ingredient_name,ingredient_thumb,ingredient_description):
        ingredient_details.start(ingredient_name,ingredient_thumb,ingredient_description)
        return

    def clear_all(self):
        self.getControl(drinklabel).setLabel('')
        self.getControl(drinkthumb).setImage('')
        self.getControl(drinkrecipe).setText('')
        self.getControl(drinksublabel).setText('')
        self.clear_ingredients()
        return

    def clear_ingredients(self):
        self.getControl(INGREDIENT_PANEL_CONTROL).reset()
        return

    def close_screensaver(self):
        self.canceled = True
        self.close()
        return

    def onAction(self,action):
        if action.getId() == ACTION_ENTER:

            if not xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
                size = self.getControl(INGREDIENT_PANEL_CONTROL).size()
                if size > 0:
                    self.setFocusId(INGREDIENT_PANEL_CONTROL)
                    self.getControl(INGREDIENT_PANEL_CONTROL).selectItem(0)
            else:
                ingredient_name = self.getControl(INGREDIENT_PANEL_CONTROL).getSelectedItem().getLabel()
                ingredient_thumb = self.getControl(INGREDIENT_PANEL_CONTROL).getSelectedItem().getProperty('ingredient_thumb')
                #TODO get ingredient description when available
                ingredient_description = translate(32029)
                self.set_ingredient_description(ingredient_name,ingredient_thumb,ingredient_description)

        if action.getId() == ACTION_RIGHT and not xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
            if self.position == 0 and self.pages > 1:
                self.clear_ingredients()
                self.set_second_ingredients(self.cocktail_obj)
            elif self.position == 1 and self.pages > 2:
                self.clear_ingredients()
                self.set_third_ingredients(self.cocktail_obj)
            else:
                if self.screensaver_mode:
                    self.current_time = 0
                    self.set_random()

        elif action.getId() == ACTION_LEFT and not xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
            if self.position == 2 and self.pages <= 3:
                self.clear_ingredients()
                self.set_second_ingredients(self.cocktail_obj)
            elif self.position == 1 and self.pages <= 2:
                self.clear_ingredients()
                self.set_first_ingredients(self.cocktail_obj)
            else:
                if self.screensaver_mode:
                    self.current_time = 0
                    self.set_random()

        elif action.getId() == ACTION_CONTEXT_MENU:
            keyb = xbmc.Keyboard('', translate(32009))
            keyb.doModal()
            if keyb.isConfirmed():
                search_parameter = urllib.quote_plus(keyb.getText())
                if not search_parameter:
                    xbmcgui.Dialog().ok(translate(32000), translate(32010))
                else:
                    cocktails_list = COCKTAIL_API.Search().cocktail(search_parameter)
                    if not cocktails_list:
                        xbmcgui.Dialog().ok(translate(32000), translate(32011))
                    else:
                        cocktails_name = []
                        for cocktail in cocktails_list:
                            cocktails_name.append(cocktail.name)

                        if len(cocktails_name) == 1:
                            self.set_cocktail(cocktails_list[0])
                        else:
                            choose = xbmcgui.Dialog().select(translate(32000), cocktails_name)
                            if choose > -1:
                                self.set_cocktail(cocktails_list[choose])

        else:
            if action.getId() != 7:
                if self.screensaver_mode:
                    if not xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
                        self.close_screensaver()
                    else:
                        if action.getId() == ACTION_RETURN or action.getId() == ACTION_ESCAPE:
                            if xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
                                self.setFocusId(FICTIONAL_PANEL_CONTROL)
                else:
                    if action.getId() == ACTION_RETURN or action.getId() == ACTION_ESCAPE:
                        if xbmc.getCondVisibility("Control.HasFocus("+str(INGREDIENT_PANEL_CONTROL)+")"):
                            self.setFocusId(FICTIONAL_PANEL_CONTROL)
                        else:
                            self.close_screensaver()

    def onClick(self,controlId):
        if controlId == INGREDIENT_PANEL_CONTROL:
            ingredient_name = self.getControl(INGREDIENT_PANEL_CONTROL).getSelectedItem().getLabel()
            ingredient_thumb = self.getControl(INGREDIENT_PANEL_CONTROL).getSelectedItem().getProperty('ingredient_thumb')
            # TODO get ingredient description when available
            ingredient_description = translate(32029)
            self.set_ingredient_description(ingredient_name,ingredient_thumb,ingredient_description)



if __name__ == '__main__':

    #note pass id of the drink to open a given cocktail
    screensaver = Screensaver(
        'script-cocktail-Cocktailplayer.xml',
        ADDON_PATH,
        'default',
        '',
    )
    screensaver.doModal()
    del screensaver
