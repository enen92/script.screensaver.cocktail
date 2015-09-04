# -*- coding: utf-8 -*-
'''
    script.screensaver.cocktail - A random cocktail recipe screensaver for kodi 
    Copyright (C) 2015 enen92

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmcaddon
import xbmcgui
import xbmc
import sys
import os
import urllib
from resources.lib import thecocktaildb
from resources.lib.common_cocktail import *

if addon.getSetting('ingredient-switch') == '0': switch_percentage = 20
elif addon.getSetting('ingredient-switch') == '1': switch_percentage = 10

#Window controls
drinklabel = 32603
drinkthumb = 32602
drinksublabel = 32604
drinkrecipe = 32606
ingredient1thumb = 32607
ingredient1name = 32608
ingredient1measure = 32609
ingredient2thumb = 32610
ingredient2name = 32611
ingredient2measure = 32612
ingredient3thumb = 32613
ingredient3name = 32614
ingredient3measure = 32615
ingredient4thumb = 32616
ingredient4name = 32617
ingredient4measure = 32618
ingredient5thumb = 32619
ingredient5name = 32620
ingredient5measure = 32621
ingredient6thumb = 32622
ingredient6name = 32623
ingredient6measure = 32624


class Screensaver(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		self.canceled = False
		self.mode = args[3]
		if self.mode:
			self.screensaver_mode = False
			self.cocktail_id = str(self.mode)
		else:
			self.screensaver_mode = True
	
	def onInit(self):
		self.drink_id = 0
		
		if self.screensaver_mode:
			if addon.getSetting('enable-instructions') == 'true':
				xbmc.executebuiltin("SetProperty(instructions,1,home)")
				wait_time = int(addon.getSetting('wait-time-instructions'))
				xbmc.sleep(wait_time*1000)
				
		next_random = int(addon.getSetting('next-time'))*1000
		
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
			xbmc.executebuiltin("SetProperty(loading,1,home)")
			cocktails_list = cocktailsdb_api.Lookup().cocktail(self.cocktail_id)
			xbmc.executebuiltin("ClearProperty(loading,Home)")
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
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		cocktails_list = cocktailsdb_api.Search().random()
		xbmc.sleep(200)
		xbmc.executebuiltin("ClearProperty(instructions,Home)")
		if int(cocktails_list[0].id) != self.drink_id:
			xbmc.sleep(200)
			xbmc.executebuiltin("ClearProperty(loading,Home)")
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
		if cocktail.thumb: self.getControl(drinkthumb).setImage(cocktail.thumb)
		else: self.getControl(drinkthumb).setImage(os.path.join(addon_path,"resources","skins","default","media","cocktail.jpg"))
		self.getControl(drinkrecipe).setText(cocktail.recipe)
		self.getControl(drinksublabel).setText(cocktail.category + ' - ' + cocktail.alcoholic + ' - ' + cocktail.glass)
		self.set_first_ingredients(cocktail)
		return
		
	def set_first_ingredients(self,cocktail):
		self.position = 0
		
		if cocktail.ingredient1.rstrip():
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient1))+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient1)
			if cocktail.measure1.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure1.rstrip()+')')
		if cocktail.ingredient2.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient2))+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient2)
			if cocktail.measure2.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure2.rstrip()+')')
		if cocktail.ingredient3.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient3))+'.png')
			self.getControl(ingredient3name).setText(cocktail.ingredient3)
			if cocktail.measure3.rstrip(): self.getControl(ingredient3measure).setText('('+cocktail.measure3.rstrip()+')')
		if cocktail.ingredient4.rstrip():
			self.getControl(ingredient4thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient4))+'.png')
			self.getControl(ingredient4name).setText(cocktail.ingredient4)
			if cocktail.measure4.rstrip(): self.getControl(ingredient4measure).setText('('+cocktail.measure4.rstrip()+')')
		if cocktail.ingredient5.rstrip():
			self.getControl(ingredient5thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient5))+'.png')
			self.getControl(ingredient5name).setText(cocktail.ingredient5)
			if cocktail.measure5.rstrip(): self.getControl(ingredient5measure).setText('('+cocktail.measure5.rstrip()+')')
		if cocktail.ingredient6.rstrip():
			self.getControl(ingredient6thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient6))+'.png')
			self.getControl(ingredient6name).setText(cocktail.ingredient6)
			if cocktail.measure6.rstrip(): self.getControl(ingredient6measure).setText('('+cocktail.measure6.rstrip()+')')
		if cocktail.ingredient7.rstrip(): self.pages = 2
		return
	
	def set_second_ingredients(self,cocktail):
		self.position = 1
		
		if cocktail.ingredient7.rstrip():
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient7))+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient7)
			if cocktail.measure7.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure7.rstrip()+')')
		if cocktail.ingredient8.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient8))+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient8)
			if cocktail.measure8.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure8.rstrip()+')')
		if cocktail.ingredient9.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient9))+'.png')
			self.getControl(ingredient3name).setText(cocktail.ingredient9)
			if cocktail.measure9.rstrip(): self.getControl(ingredient3measure).setText('('+cocktail.measure9.rstrip()+')')
		if cocktail.ingredient10.rstrip():
			self.getControl(ingredient4thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient10))+'.png')
			self.getControl(ingredient4name).setText(cocktail.ingredient10)
			if cocktail.measure10.rstrip(): self.getControl(ingredient4measure).setText('('+cocktail.measure10.rstrip()+')')
		if cocktail.ingredient11.rstrip():
			self.getControl(ingredient5thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient11))+'.png')
			self.getControl(ingredient5name).setText(cocktail.ingredient11)
			if cocktail.measure11.rstrip(): self.getControl(ingredient5measure).setText('('+cocktail.measure11.rstrip()+')')
		if cocktail.ingredient12.rstrip():
			self.getControl(ingredient6thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient12))+'.png')
			self.getControl(ingredient6name).setText(cocktail.ingredient12)
			if cocktail.measure12.rstrip(): self.getControl(ingredient6measure).setText('('+cocktail.measure12.rstrip()+')')
		if cocktail.ingredient13.rstrip(): self.pages = 3
		return
		
	def set_third_ingredients(self,cocktail):
		self.position = 2
		
		if cocktail.ingredient13.rstrip():
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient13))+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient13)
			if cocktail.measure13.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure13.rstrip()+')')
		if cocktail.ingredient14.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient14))+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient14)
			if cocktail.measure14.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure14.rstrip()+')')
		if cocktail.ingredient15.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(removeNonAscii(cocktail.ingredient14))+'.png')
			self.getControl(ingredient3name).setText(cocktail.ingredient14)
			if cocktail.measure15.rstrip(): self.getControl(ingredient3measure).setText('('+cocktail.measure14.rstrip()+')')
		return
		
	def clear_all(self):
		self.getControl(drinklabel).setLabel('')
		self.getControl(drinkthumb).setImage('')
		self.getControl(drinkrecipe).setText('')
		self.getControl(drinksublabel).setText('')
		self.clear_ingredients()
		return
		
	def clear_ingredients(self):
		self.getControl(ingredient1thumb).setImage('')
		self.getControl(ingredient1name).setText('')
		self.getControl(ingredient1measure).setText('')
		self.getControl(ingredient2thumb).setImage('')
		self.getControl(ingredient2name).setText('')
		self.getControl(ingredient2measure).setText('')
		self.getControl(ingredient3thumb).setImage('')
		self.getControl(ingredient3name).setText('')
		self.getControl(ingredient3measure).setText('')
		self.getControl(ingredient4thumb).setImage('')
		self.getControl(ingredient4name).setText('')
		self.getControl(ingredient4measure).setText('')
		self.getControl(ingredient5thumb).setImage('')
		self.getControl(ingredient5name).setText('')
		self.getControl(ingredient5measure).setText('')
		self.getControl(ingredient6thumb).setImage('')
		self.getControl(ingredient6name).setText('')
		self.getControl(ingredient6measure).setText('')
		return
		
	def close_screensaver(self):
		self.canceled = True
		self.close()
		return
		
	def onAction(self,action):
		
		if action.getId() == ACTION_RIGHT:
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
		
		elif action.getId() == ACTION_LEFT:
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
			if (keyb.isConfirmed()):
				search_parameter = urllib.quote_plus(keyb.getText())
				if not search_parameter: xbmcgui.Dialog().ok(translate(32000),translate(32010))
				else:
					cocktails_list = cocktailsdb_api.Search().cocktail(search_parameter)
					if not cocktails_list: xbmcgui.Dialog().ok(translate(32000),translate(32011))
					else:
						cocktails_name = []
						for cocktail in cocktails_list:
							cocktails_name.append(cocktail.name)
						if len(cocktails_name) == 1:
							self.set_cocktail(cocktails_list[0])
						else:
							choose = xbmcgui.Dialog().select(translate(32000),cocktails_name)
							if choose > -1:
								self.set_cocktail(cocktails_list[choose])
							
		else:
			if self.screensaver_mode:
				self.close_screensaver()
			else:
				if action.getId() == ACTION_RETURN or action.getId() == ACTION_ESCAPE:
					self.close_screensaver()


if __name__ == '__main__':

	#note pass id of the drink to open a given cocktail
	
	screensaver = Screensaver(
		'script-cocktail-Cocktailplayer.xml',
		addon_path,
		'default',
		'',
	)
	screensaver.doModal()
	del screensaver
	sys.modules.clear()
