from telegram import *
from telegram.ext import *
import os
import shutil
import logging
import constants as keys
import responses as r  
    
todof = "file_17.ttf"
def start_command(update, context):
    update.message.reply_text("type something to begin!")
    
def help_command(update,context):
    update.message.reply_text("Search for it on Google, duh")
    
def handle_message(update,context):
    text = str(update.message.text).lower()
    update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    update.message.reply_text(f"Update {update} caused error {context.error}")
    
def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help",help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_handler(MessageHandler(Filters.document, ttfdownload))
    dp.add_error_handler(error)
    
    updater.start_polling()
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
    shutil.make_archive("../magiFont/"+todof, 'zip', os.getcwd())
    

def ttfdownload(update, context):
    update.message.reply_text("file detected...")
    clearcache()
    #print(context.bot.get_file(update.message.document))
    os.chdir("todo")
    context.bot.get_file(update.message.document).download()
    update.message.reply_text("downloaded!!")
    global todof
    for dirs,file,name in os.walk(os.getcwd()):
        #print(dirs)
        print(file)
        print(name)
        todof=name[len(name)-1]
    print(todof)
    os.chdir("../")
    #todof=
    #print(os.getcwd())
    update.message.reply_text("allwell before modulify")
    modulify()
    update.message.reply_text("allwell after modulify "+os.getcwd())
    os.chdir("../magiFont")
    update.message.reply_text("allwell before sendfile")
    context.bot.send_document(update.message.chat_id, open(todof+".zip",'rb'))
    os.chdir("../")
    
def clearcache():
    #print(os.getcwd())
    path_to_folder = "todo"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            print("deleting file:", file_path)
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            print("deleting folder:", file_path)
            shutil.rmtree(file_path)
            
    path_to_folder = "magiFont"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            print("deleting file:", file_path)
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            print("deleting folder:", file_path)
            shutil.rmtree(file_path)
    
    
main()
