from telegram import *
from telegram.ext import *
#import telegram
import os
import shutil
import logging
import constants as keys
import responses as r
import random
    
todof = "file_17.ttf"
file_responses = ["This your OP font by your OP group", "You are the best!!", "You are OP", "Keep it up, i am waiting for more...","Here you go!", "Thanks for being one of us","Check this out!!", "Take this...","I hope you like it!", "Done!!","Compiled...","Finished!"]

bot = Bot(keys.API_KEY)

def member_join(update, context):
    
    for member in update.message.new_chat_members:
        member_count = int(bot.get_chat_members_count(update.message.chat_id))
        if member_count%10 == 0:
            message = update.message.reply_text(f"{member.full_name} is the "+str(member_count)+"th to join the group!!\nWhoo!! "+str(member_count)+" members!")
            if not bot.pin_chat_message(update.message.chat_id, message.message_id):
                update.message.reply_text("I can't even pin a message.. dang!")

def start_command(update, context):
    update.message.reply_text("Send a font file to begin!! use /about for more info")
    
def help_command(update,context):
    update.message.reply_text("Search for it on Google, duh")
    
def ccache_command(update,context):
    clearcache()
    update.message.reply_text("Done")
    
def module_command(update,context):
    #clearcache()
    update.message.reply_text("Send a .otf/.ttf file...")
    
    
def about_command(update,context):
    #update.message.reply_text("Memebers count: "+str(bot.get_chat_members_count(update.message.chat_id)))
    update.message.reply_text("@TheSc1enceGuy(akshit singh) is the  developer of this bot... This bot will convert any sent font (.ttf or .otf) to a magisk flashable zip... enjoy!")

def maker_command(update,context):
    update.message.reply_text("@TheSc1enceGuy(akshit singh) has made this bot...")

def owner_command(update,context):
    update.message.reply_text("@TheSc1enceGuy(akshit singh) is my father... and he is the owner too lel ;)")
    
def handle_message(update,context):
    return True
    #text = str(update.message.text).lower()
    #if r.sample_responses(text) not in (""):
    #    update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    print(f"Update {update} caused error {context.error}")
    
def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("ccache",ccache_command))
    dp.add_handler(CommandHandler("creator",maker_command))
    dp.add_handler(CommandHandler("owner",owner_command))
    dp.add_handler(CommandHandler("about",about_command))
    dp.add_handler(CommandHandler("module",module_command))
    dp.add_handler(CommandHandler("faketrigger",member_join))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_handler(MessageHandler(Filters.document & (Filters.chat(1441717868) | Filters.chat(-1001393886080) | Filters.chat(-503134615)), ttfdownload))
    dp.add_error_handler(error)
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, member_join)
    dp.add_handler(add_group_handle)

    
    updater.start_polling(drop_pending_updates=True)
    updater.idle()
    
tfonts = ['MiLanProVF.ttf',
 'Roboto-Black.ttf',
 'Roboto-BlackItalic.ttf',
 'Roboto-Bold.ttf',
 'Roboto-BoldItalic.ttf',
 'Roboto-Italic.ttf',
 'Roboto-Light.ttf',
 'Roboto-LightItalic.ttf',
 'Roboto-Medium.ttf',
 'Roboto-MediumItalic.ttf',
 'Roboto-Regular.ttf',
 'Roboto-Thin.ttf',
 'Roboto-ThinItalic.ttf',
 'RobotoCondensed-Bold.ttf',
 'RobotoCondensed-BoldItalic.ttf',
 'RobotoCondensed-Italic.ttf',
 'RobotoCondensed-Light.ttf',
 'RobotoCondensed-LightItalic.ttf',
 'RobotoCondensed-Medium.ttf',
 'RobotoCondensed-MediumItalic.ttf',
 'RobotoCondensed-Regular.ttf',
 'RobotoNum-3R.ttf',
 'RRobotoNum-3L.ttf']
#todof= file...

#os.chdir("C:/Users/rsran/Downloads/akshit ka fonts")
def modulify():
    os.chdir("magiTemplate/system/fonts")
    
    for i in range(0,len(tfonts)):
        shutil.copyfile(src="../../../todo/"+todof , dst=tfonts[i])
    
    #print(os.getcwd())
    os.chdir("../../../magiTemplate")
    shutil.make_archive("../magiFont/"+todof.split(".")[0], 'zip', os.getcwd())
    

def ttfdownload(update, context):
    if update.message.document.file_name.split(".")[len(update.message.document.file_name.split("."))-1] in ("otf", "ttf"):
        bot.send_message(update.message.chat_id,"font request, huh? how's this font btw? -  "+update.message.document.file_name)
        clearcache()
        #update.message.reply_text("cleared ccache")
        #print(context.bot.get_file(update.message.document))
        os.chdir("todo")
        #print(context.bot.get_file(update.message.document).file_name)
        #context.bot.get_file(update.message.document).download()
        update.message.document.get_file().download(custom_path=update.message.document.file_name)
    
        
        global todof
        for dirs,file,name in os.walk(os.getcwd()):
            #print(dirs)
            #print(file) 
            #print(name)
            todof=name[len(name)-1]
        
        #print(todof.split("."))
        if todof.split(".")[len(todof.split("."))-1] in ("ttf", "otf"):
            #update.message.reply_text("downloaded!!")
            #print(todof)
            os.chdir("../")
            #todof=
            #print(os.getcwd())
            #update.message.reply_text("allwell before modulify")
            modulify()
            #update.message.reply_text("allwell after modulify "+os.getcwd())
            os.chdir("../magiFont")
            #update.message.reply_text("allwell before sendfile")
            context.bot.send_document(update.message.chat_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
            bot.send_message(update.message.chat_id,"Make sure to send a sample... \ncheck #submit-sample It takes no effort and helps us a ton!! \nThanks for being a part of the awesome community!!")
            os.chdir("../")
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
    
def clearcache():
    #print(os.getcwd())
    path_to_folder = "todo"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            #print("deleting file:", file_path)
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            #print("deleting folder:", file_path)
            shutil.rmtree(file_path)
            
    path_to_folder = "magiFont"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            #print("deleting file:", file_path)
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            #print("deleting folder:", file_path)
            shutil.rmtree(file_path)
    
    
main()
