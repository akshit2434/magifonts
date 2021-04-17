from telegram import *
from telegram.ext import *
#import telegram
import os
import shutil
import logging
import constants as keys
import responses as r
import random

magifonts_id = -1001393886080
font_ext = ("ttf", "otf")
todof = "file_17.ttf"
file_responses = ["This your OP font by your OP group", "You are the best!!", "You are OP", "Keep it up, i am waiting for more...","Here you go!", "Thanks for being one of us","Check this out!!", "Take this...","I hope you like it!", "Done!!","Compiled...","Finished!"]
FONT, BOLD, ITALICS = range(3)
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
    if update.message.text:
        text = str(update.message.text).lower()
        if r.sample_responses(text) not in (""):
            update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    print(f"Update {update} caused error {context.error}")
    
def module(update,context):
    if "-" in str(update.message.chat_id):
        update.message.reply_text("Try running this command in my pm...")
    else:
        print("module requested by @"+update.message.from_user.username)
        bot.send_message(update.message.chat_id,"Hey "+update.message.from_user.first_name+", i think you want to make a custom font.\nSend /cancel to cancel the process...")
        bot.send_message(update.message.chat_id,"Send /cancel to cancel any time\nSend a font file to continue!")
        return FONT

def font(update,context):
    if update.message.document.file_name.split(".")[-1].lower() in font_ext:
        #update.message.reply_text("font request, huh? how's this font btw? -  "+update.message.document.file_name)
        clearcache()
        os.chdir("todo")
        update.message.document.get_file().download(custom_path=update.message.document.file_name)
    
        
        global todof
        for dirs,file,name in walklevel(os.getcwd(),1):
            todof=name[-1]
        
        if todof.split(".")[-1].lower() in font_ext:
            os.chdir("../")
            #modulify()
            #os.chdir("../magiFont")
            #context.bot.send_document(update.message.chat_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
            #update.message.reply_text("Make sure to send a sample... \ncheck #submit-sample It takes no effort and helps us a ton!! \nThanks for being a part of the awesome community!!")
            #os.chdir("../")
            bot.send_message(update.message.chat_id, "Do you have the bold version?\nSend /skip to skip this step\nSend Bold font file or do /skip ...")
            return BOLD
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
            bot.send_message(update.message.chat_id, "Send a valid font file to continue...")
            return FONT
        
def bold(update,context):
    if update.message.document.file_name.split(".")[-1].lower() in font_ext:
        #update.message.reply_text("font request, huh? how's this font btw? -  "+update.message.document.file_name)
        #clearcache()
        os.chdir("todo")
        update.message.document.get_file().download(custom_path=todof+"-bold.ttf")
        
        if todof.split(".")[-1].lower() in font_ext:
            os.chdir("../")
            #modulify()
            #os.chdir("../magiFont")
            #context.bot.send_document(update.message.chat_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
            #update.message.reply_text("Make sure to send a sample... \ncheck #submit-sample It takes no effort and helps us a ton!! \nThanks for being a part of the awesome community!!")
            #os.chdir("../")
            bot.send_message(update.message.chat_id, "Do you have the italics version?\nSend /skip to skip this step\nSend Italics font file or do /skip ...")
            return ITALICS
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
            bot.send_message(update.message.chat_id, "Send a valid font file to continue...")
            return BOLD
        
def italics(update,context):
    if update.message.document.file_name.split(".")[-1].lower() in font_ext:
        #update.message.reply_text("font request, huh? how's this font btw? -  "+update.message.document.file_name)
        #clearcache()
        os.chdir("todo")
        update.message.document.get_file().download(custom_path=todof+"-italics.ttf")
        
        if todof.split(".")[-1].lower() in font_ext:
            os.chdir("../")
            #modulify()
            #os.chdir("../magiFont")
            #context.bot.send_document(update.message.chat_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
            #update.message.reply_text("Make sure to send a sample... \ncheck #submit-sample It takes no effort and helps us a ton!! \nThanks for being a part of the awesome community!!")
            #os.chdir("../")
            bot.send_message(update.message.chat_id, "Ok... Processing...")
            modulifybi(todof)
            print(os.getcwd())
            print("../magiFont/"+todof.split(".")[0]+".zip")
            bot.send_document(magifonts_id, open("../magiFont/"+todof.split(".")[0]+".zip","rb"),caption=random.choice(file_responses))
            os.chdir("../")
            return ConversationHandler.END
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
            bot.send_message(update.message.chat_id, "Send a valid font file to continue...")
            return ITALICS
    
def skip_bold(update,context):
    bot.send_message(update.message.chat_id, "OK, np. Do you have Italics font file?\nSend to continue or send /skip ...")
    return ITALICS

def skip_italics(update,context):
    bot.send_message(update.message.chat_id, "OK, np. Processing, give me a minute sar ...")
    modulifybi(todof)
    bot.send_document(magifonts_id, open("../magiFont/"+todof.split(".")[0]+".zip","rb"),caption=random.choice(file_responses))
    bot.send_message(magifonts_id, "Here @"+update.message.from_user.username)
    update.message.reply_text("Check Magifonts group (@magifonts_support). Your font has been posted")
    os.chdir("../")
    return ConversationHandler.END
    
def cancel(update, context):
    bot.send_message(update.message.chat_id, "Cancelled... :(")
    return ConversationHandler.END
    
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    initialize()
    ttf_handler = ConversationHandler(
        entry_points=[CommandHandler('module', module)],
        states={
            FONT: [MessageHandler(Filters.document, font)],
            BOLD: [MessageHandler(Filters.document, bold), CommandHandler('skip', skip_bold)],
            ITALICS: [MessageHandler(Filters.document, italics), CommandHandler('skip', skip_italics)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(ttf_handler)
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help",help_command))
    dispatcher.add_handler(CommandHandler("ccache",ccache_command))
    dispatcher.add_handler(CommandHandler("creator",maker_command))
    dispatcher.add_handler(CommandHandler("owner",owner_command))
    dispatcher.add_handler(CommandHandler("about",about_command))
    #dp.add_handler(CommandHandler("module",module_command))
    dispatcher.add_handler(CommandHandler("faketrigger",member_join))
    
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    
    dispatcher.add_handler(MessageHandler(Filters.document, ttfdownload))

    #dispatcher.add_handler(MessageHandler(Filters.document & (Filters.chat(1441717868) | Filters.chat(-1001393886080) | Filters.chat(-503134615)), ttfdownload))
    dispatcher.add_error_handler(error)
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, member_join)
    dispatcher.add_handler(add_group_handle)

    # Start the Bot
    updater.start_polling(drop_pending_updates=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
    
tfonts = ["MFFM.ttf"]

tfontsr = ["Black.ttf", "Medium.ttf","Regular.ttf","Light.ttf","Thin.ttf"]

tfontsb = ["Bold.ttf","BoldItalic.ttf"]

tfontsi = ["MediumItalic.ttf", "Italic.ttf","BlackItalic.ttf","LightItalic.ttf","ThinItalic.ttf"]
#todof= file...

#os.chdir("C:/Users/rsran/Downloads/akshit ka fonts")
def modulify():
    os.chdir("magiTemplate/Fonts")
    
    for i in range(0,len(tfonts)):
        shutil.copyfile(src="../../todo/"+todof , dst=tfonts[i])
    
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir("magiTemplate")
    shutil.make_archive("../magiFont/"+todof.split(".")[0], 'zip', os.getcwd())
    
def modulifybi(fname):
    os.chdir(orig_dir)
    fnameb = fname+"-bold.ttf"
    fnamei = fname+"-italics.ttf"
    todocontents = []
    
    for dirs,file,name in walklevel("todo"):
        todocontents = name
        
    if fnameb not in todocontents:
        fnameb = fname
    
    if fnamei not in todocontents:
        fnamei = fname
    
    os.chdir("magiTemplate/Fonts")
    for i in range(0,len(tfontsr)):
        shutil.copyfile(src="../../todo/"+fname , dst=tfontsr[i])
    
    for i in range(0,len(tfontsb)):
        shutil.copyfile(src="../../todo/"+fnameb , dst=tfontsb[i])
        
    for i in range(0,len(tfontsi)):
        shutil.copyfile(src="../../todo/"+fnamei , dst=tfontsi[i])
    
    #print(os.getcwd())
    os.chdir(orig_dirs)
    os.chdir("magiTemplate")
    shutil.make_archive("../magiFont/"+fname.split(".")[0], 'zip', os.getcwd())
    

def ttfdownload(update, context):
    os.chdir(orig_dir)
    clearcache()
    print("ttf download requested by @"+update.message.from_user.username)
    #print(update.message.document.file_name.split(".")[-1].lower())
    if update.message.document.file_name.split(".")[-1].lower() in font_ext:
        bot.send_message(update.message.chat_id, "Check /module for creating fonts with custom bold and/or italic fonts!!")
        update.message.reply_text("font request, huh? how's this font btw? -  "+update.message.document.file_name)
        print(os.getcwd())
        os.chdir("todo")

        update.message.document.get_file().download(custom_path=update.message.document.file_name)
        global todof
        for dirs,file,name in walklevel(os.getcwd()):
            print("DIRECTORY LOCATION ABHI KI:")
            print(os.getcwd())
            todof=name[-1]
            print(name)
        
        if todof.split(".")[-1].lower() in font_ext:
            os.chdir("../")
            modulify()
            os.chdir("../magiFont")
            context.bot.send_document(magifonts_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
            bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
            if not str(update.message.chat_id) == str(magifonts_id):
                update.message.reply_text("Your file has been posted in @magifonts_support")
            update.message.reply_text("Checkout #submit-sample\nThanks for being a part of the awesome community!!")
            os.chdir("../")
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
    elif update.message.document.file_name.split(".")[-1].lower() == "zip":
        update.message.reply_text("Zip detected!")
        os.chdir("ziptodo")
        update.message.document.get_file().download(custom_path=update.message.document.file_name)
        print("file downloaded!")
        shutil.unpack_archive(update.message.document.file_name,update.message.document.file_name.split(".")[0])
        print("file unzipped")
        if os.path.exists(update.message.document.file_name.split(".")[0]+"/system/fonts"):
            if os.path.exists(update.message.document.file_name.split(".")[0]+"/module.prop"):
                update.message.reply_text("The provided zip is already a magisk module LOL!")
                os.chdir("../")
                print(os.getcwd())
            else:
                update.message.reply_text("Converting to a magisk module sar!!")
                os.chdir(update.message.document.file_name.split(".")[0])
                shutil.copyfile(src="../../magiTemplate/module.prop" , dst="module.prop")
                shutil.copyfile(src="../../magiTemplate/META-INF/com/google/android/update-binary" , dst="META-INF/com/google/android/update-binary")
                shutil.copyfile(src="../../magiTemplate/META-INF/com/google/android/updater-script" , dst="META-INF/com/google/android/updater-script")
                shutil.make_archive("../../magiFont/"+update.message.document.file_name.split(".")[0], 'zip', os.getcwd())
                os.chdir("../../magiFont")
                bot.send_document(magifonts_id, open(update.message.document.file_name.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
                bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
                if not str(update.message.chat_id) == str(magifonts_id):
                    update.message.reply_text("Your file has been posted in @magifonts_support")
                update.message.reply_text("Checkout #submit-sample\nThanks for being a part of the awesome community!!")
                os.chdir("../")
        else:
            ttfarray = []
            
            ttfarray = listfiles("../ziptodo/"+update.message.document.file_name.split(".")[0])
            ttfarray = list(filter(lambda x : x.split(".")[-1] in font_ext, ttfarray))
            print(ttfarray)
            ttfarray = list(filter(lambda x : (("regular" in x.lower()) or ("normal" in x.lower()) and not(("condensed" in x.lower()) or ("bold" in x.lower()) or ("italics" in x.lower()))), ttfarray))
            print(ttfarray)
            print("regular ttf file below")
            print(ttfarray)
            if len(ttfarray)>0:
                print(1)
            else:
                print(os.getcwd())
                ttfarray = listfiles("../ziptodo/"+update.message.document.file_name.split(".")[0])
                print("0_.1")
                ttfarray = list(filter(lambda x : x.split(".")[-1] in font_ext, ttfarray))
                print("0_.2")
                ttfarray = list(filter(lambda x : lambda x : not (("bold" in x) or ("italics" in x) or ("ital" in x)), ttfarray))
                print("0_.3")
                print("1_")
                if len(ttfarray) == 0:
                    ttfarray = listfiles("../ziptodo/"+update.message.document.file_name.split(".")[0])
                    ttfarray = list(filter(lambda x : x.split(".")[-1] in font_ext, ttfarray))
                    ttfarray = ttfarray[0]
            
            if len(ttfarray) > 0:
                todof = ttfarray[0]
                shutil.copy("../ziptodo/"+update.message.document.file_name.split(".")[0]+"/"+ttfarray[0], "../todo/"+ttfarray[0])
                print(1.1)
                ttfarray = listfiles("../ziptodo/"+update.message.document.file_name.split(".")[0])
                print(1.2)
                ttfarray = list(filter(lambda x : x.split(".")[-1] in font_ext, ttfarray))
                ttfarray = list(filter(lambda x : (("bold" in x) or ("-b." in x)) and not(("condensed" in x) or ("italics" in x) or ("light" in x)), ttfarray))
                print(1.3)
                if len(ttfarray)>0:
                    shutil.copy("../ziptodo/"+update.message.document.file_name.split(".")[0]+"/"+ttfarray[0],"../todo/"+ttfarray[0].split(".")[0]+"-bold.ttf")
                print(2)
                ttfarray = listfiles("../ziptodo/"+update.message.document.file_name.split(".")[0])
                ttfarray = list(filter(lambda x : x.split(".")[-1] in font_ext, ttfarray))
                ttfarray = list(filter(lambda x : (("-i." in x) or ("ital" in x)) and not (("condensed" in x) or ("bold" in x) or ("light" in x)), ttfarray))
                print(3)
                if len(ttfarray)>0:
                    shutil.copy("../ziptodo/"+update.message.document.file_name.split(".")[0]+"/"+ttfarray[0], "../todo/"+ttfarray[0].split(".")[0]+"-italics.ttf")

        
                os.chdir("../")
                print("modulifybi...")
                modulifybi(todof)
                os.chdir("../magiFont")
                bot.send_document(magifonts_id, open(todof.split(".")[0]+".zip",'rb'),caption=random.choice(file_responses))
                bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
                if not (update.message.chat_id == magifonts_id):
                    bot.send_message(update.message.chat_id,"The file has been posted to @magifonts_support")
                os.chdir("../")
            else:                
                os.chdir("../")
                update.message.reply_text("Sar, sorry but I can't make this to a module. Pls gib ttf ot otf file :(")
        #os.chdir("../magiTemplate/system/fonts")
        #for i in range(0,len(tfontsr)):
        #    shutil.copyfile(src="../../../todo/"+fname , dst=tfontsr[i])
        
        
    
def clearcache():
    os.chdir(orig_dir)
    path_to_folder = "todo"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            
    path_to_folder = "magiFont"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    
    path_to_folder = "ziptodo"
    list_dir = os.listdir(path_to_folder)
    for filename in list_dir:
        file_path = os.path.join(path_to_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def listfiles(direc):
    for dirs,file,name in walklevel(direc, 1):
        return name


    
def initialize():
    create_dir("todo")
    create_dir("magiFont")
    create_dir("ziptodo")
    clearcache()
    
def create_dir(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        return True
    

if __name__ == '__main__':
    orig_dir = os.getcwd()
    main()
