#!/usr/bin/env python3
#
#
#Partly cloudy ⛅️  🌡️+36°F (feels +26°F, 50%) 🌬️→11mph 🌓 Thu Dec  1 06:41:21 2022

import os



CACHE_FOLDER = os.getenv('alfred_workflow_cache')
CACHE_FOLDER_IMAGES = CACHE_FOLDER+"/images"
QUICKLOOK_PREF = os.getenv('PreviewPref')

if os.getenv('HISTORY_FOLDER'):
    HISTORY_FOLDER = os.getenv('HISTORY_FOLDER')
else:
    HISTORY_FOLDER = CACHE_FOLDER


if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)
if not os.path.exists(CACHE_FOLDER_IMAGES):
    os.makedirs(CACHE_FOLDER_IMAGES)

