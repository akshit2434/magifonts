# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:11:50 2021

@author: akshit Singh
"""

def sample_responses(input_text):
    user_message = str(input_text).lower()
    
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
  
    # Removing punctuations in string
    # Using loop + punctuation string
    for ele in user_message: 
        if ele in punc: 
            user_message = user_message.replace(ele, "") 
    
    message_array = user_message.split(" ")
    if ("hello" in message_array) or ("hey" in message_array) or ("hi" in message_array):
        return "Hello Sar!"
    if "good morning" in user_message:
        return "Good Morning Sar!"
    if "good night" in user_message:
        return "Good Night Sar!"
    if "bye" in message_array:
        return "See you soon Sar!"
    
    return ""
