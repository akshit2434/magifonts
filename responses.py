# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:11:50 2021

@author: rsran
"""

def sample_responses(input_text):
    user_message = str(input_text).lower()
    if user_message in ("do you know anything?"):
        return "i know nothing rn... but i am gonna get an update soon..."
    
    return "dont say gibberish bRAH"