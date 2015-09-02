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

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
addon_name = addon.getAddonInfo('name')
cocktailsdb_api = thecocktaildb.Api('1')

if addon.getSetting('ingredient-switch') == '0': switch_percentage = 20
elif addon.getSetting('ingredient-switch') == '1': switch_percentage = 10

#Window controls
drinklabel = 30003
drinkthumb = 30002
drinksublabel = 30004
drinkrecipe = 30006
ingredient1thumb = 30007
ingredient1name = 30008
ingredient1measure = 30009
ingredient2thumb = 30010
ingredient2name = 30011
ingredient2measure = 30012
ingredient3thumb = 30013
ingredient3name = 30014
ingredient3measure = 30015
ingredient4thumb = 30016
ingredient4name = 30017
ingredient4measure = 30018
ingredient5thumb = 30019
ingredient5name = 30020
ingredient5measure = 30021
ingredient6thumb = 30022
ingredient6name = 30023
ingredient6measure = 30024


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
		
		if self.screensaver_mode or addon.getSetting('quioske-mode') == 'false':
			if self.screensaver_mode:
				self.set_random()
			else:
				pass
				#TODO set specific
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
			#TODO set specific
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
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient1)+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient1)
			if cocktail.measure1.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure1.rstrip()+')')
		if cocktail.ingredient2.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient2)+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient2)
			if cocktail.measure2.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure2.rstrip()+')')
		if cocktail.ingredient3.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient3)+'.png')
			self.getControl(ingredient3name).setText(cocktail.ingredient3)
			if cocktail.measure3.rstrip(): self.getControl(ingredient3measure).setText('('+cocktail.measure3.rstrip()+')')
		if cocktail.ingredient4.rstrip():
			self.getControl(ingredient4thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient4)+'.png')
			self.getControl(ingredient4name).setText(cocktail.ingredient4)
			if cocktail.measure4.rstrip(): self.getControl(ingredient4measure).setText('('+cocktail.measure4.rstrip()+')')
		if cocktail.ingredient5.rstrip():
			self.getControl(ingredient5thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient5)+'.png')
			self.getControl(ingredient5name).setText(cocktail.ingredient5)
			if cocktail.measure5.rstrip(): self.getControl(ingredient5measure).setText('('+cocktail.measure5.rstrip()+')')
		if cocktail.ingredient6.rstrip():
			self.getControl(ingredient6thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient6)+'.png')
			self.getControl(ingredient6name).setText(cocktail.ingredient6)
			if cocktail.measure6.rstrip(): self.getControl(ingredient6measure).setText('('+cocktail.measure6.rstrip()+')')
		if cocktail.ingredient7.rstrip(): self.pages = 2
		return
	
	def set_second_ingredients(self,cocktail):
		self.position = 1
		
		if cocktail.ingredient7.rstrip():
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient7)+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient7)
			if cocktail.measure7.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure7.rstrip()+')')
		if cocktail.ingredient8.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient8)+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient8)
			if cocktail.measure8.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure8.rstrip()+')')
		if cocktail.ingredient9.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient9)+'.png')
			self.getControl(ingredient3name).setText(cocktail.ingredient9)
			if cocktail.measure9.rstrip(): self.getControl(ingredient3measure).setText('('+cocktail.measure9.rstrip()+')')
		if cocktail.ingredient10.rstrip():
			self.getControl(ingredient4thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient10)+'.png')
			self.getControl(ingredient4name).setText(cocktail.ingredient10)
			if cocktail.measure10.rstrip(): self.getControl(ingredient4measure).setText('('+cocktail.measure10.rstrip()+')')
		if cocktail.ingredient11.rstrip():
			self.getControl(ingredient5thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient11)+'.png')
			self.getControl(ingredient5name).setText(cocktail.ingredient11)
			if cocktail.measure11.rstrip(): self.getControl(ingredient5measure).setText('('+cocktail.measure11.rstrip()+')')
		if cocktail.ingredient12.rstrip():
			self.getControl(ingredient6thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient12)+'.png')
			self.getControl(ingredient6name).setText(cocktail.ingredient12)
			if cocktail.measure12.rstrip(): self.getControl(ingredient6measure).setText('('+cocktail.measure12.rstrip()+')')
		if cocktail.ingredient13.rstrip(): self.pages = 3
		return
		
	def set_third_ingredients(self,cocktail):
		self.position = 2
		
		if cocktail.ingredient13.rstrip():
			self.getControl(ingredient1thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient13)+'.png')
			self.getControl(ingredient1name).setText(cocktail.ingredient13)
			if cocktail.measure13.rstrip(): self.getControl(ingredient1measure).setText('('+cocktail.measure13.rstrip()+')')
		if cocktail.ingredient14.rstrip():
			self.getControl(ingredient2thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient14)+'.png')
			self.getControl(ingredient2name).setText(cocktail.ingredient14)
			if cocktail.measure14.rstrip(): self.getControl(ingredient2measure).setText('('+cocktail.measure14.rstrip()+')')
		if cocktail.ingredient15.rstrip():
			self.getControl(ingredient3thumb).setImage('http://www.thecocktaildb.com/images/ingredients/'+urllib.quote(cocktail.ingredient14)+'.png')
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
		
		if action.getId() == 2:
			if self.position == 0 and self.pages > 1:
				self.clear_ingredients()
				self.set_second_ingredients(self.cocktail_obj)
			elif self.position == 1 and self.pages > 2:
				self.clear_ingredients()
				self.set_third_ingredients(self.cocktail_obj)
			else:
				if addon.getSetting('quioske-mode') == 'false':
					self.current_time = 0
					self.set_random()
		
		elif action.getId() == 1:
			if self.position == 2 and self.pages <= 3:
				self.clear_ingredients()
				self.set_second_ingredients(self.cocktail_obj)
			elif self.position == 1 and self.pages <= 2:
				self.clear_ingredients()
				self.set_first_ingredients(self.cocktail_obj)
			else:
				if addon.getSetting('quioske-mode') == 'false':
					self.current_time = 0
					self.set_random()
		
		elif action.getId() == 117:
			keyb = xbmc.Keyboard('', 'Search cocktail')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search_parameter = urllib.quote_plus(keyb.getText())
				if not search_parameter: xbmcgui.Dialog().ok("Cocktail","Cocktail name can't be empty")
				else:
					cocktails_list = cocktailsdb_api.Search().cocktail(search_parameter)
					if not cocktails_list: xbmcgui.Dialog().ok("Cocktail","No matching cocktails found!")
					else:
						cocktails_name = []
						for cocktail in cocktails_list:
							cocktails_name.append(cocktail.name)
						if len(cocktails_name) == 1:
							self.set_cocktail(cocktails_list[0])
						else:
							choose = xbmcgui.Dialog().select('Cocktail',cocktails_name)
							if choose > -1:
								self.set_cocktail(cocktails_list[choose])
							
		else:
			if self.screensaver_mode:
				self.close_screensaver()
			else:
				if action.getId() == 92 or action.getId() == 10:
					self.close_screensaver()


if __name__ == '__main__':

	#note pass id to open a given cocktail

	screensaver = Screensaver(
		'script-cocktail-Main.xml',
		addon_path,
		'default',
		'',
	)
	screensaver.doModal()
	del screensaver
	sys.modules.clear()
