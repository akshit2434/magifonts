# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:11:50 2021

@author: akshit Singh
"""

def sample_responses(input_text):
    user_message = str(input_text).lower()
    if ("hello" in user_message) or ("hey" in user_message) or ("hi" in user_message):
        return "Hello Sar!"
    if "good morning" in user_message:
        return "Good Morning Sar!"
    if "good night" in user_message:
        return "Good Night Sar!"
    if "bye" in user_message:
        return "See you soon Sar!"
    
    return ""
