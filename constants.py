# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 09:52:17 2021

@author: akshit singh
"""
from py7zr import unpack_7zarchive

API_KEY = "1751727989:AAGaftex7PLDiIbTwe5_izQMwYwGUS9p8FM"
#API_KEY = "1774841533:AAGjeLwbTwQ-wqvXgUpW9EBIvq1zga6WDf0"
base = "https://api.telegram.org/bot"+API_KEY+"/"
gid = -1001393886080
#gid = -1001370521379

def init():
  shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
  
