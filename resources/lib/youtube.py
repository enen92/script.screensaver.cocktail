# -*- coding: utf-8 -*-
'''
   Copyright (C) 2015-2020 enen92,Zag
   This file is part of script.screensaver.cocktail

   SPDX-License-Identifier: GPL-2.0-only
   See LICENSE for more information.
'''

from common_cocktail import *
import urllib
import json
import re

# BROKEN
def return_youtubevideos(query):
    foundAll = False
    ind = 1
    video_list = []
    inp = urllib.urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+urllib.quote_plus(query)+'&maxResults='+str(ADDON.getSetting('youtube-max-results'))+'&key=AIzaSyAxaHJTQ5zgh86wk7geOwm-y0YyNMcEkSc')
    resp = json.load(inp)
    if resp and "items" in resp.keys():
        for item in resp["items"]:
            try:
                label = item["snippet"]["title"]
                thumb = item["snippet"]["thumbnails"]["high"]["url"]
                video = item["id"]["videoId"]
                video_item = (label, thumb,video)
                video_list.append(video_item)
            except: pass
    return video_list
