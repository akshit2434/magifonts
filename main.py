from telegram import *
from telegram.ext import *
import fnmatch
import os
import shutil
import logging
import constants as keys
import responses as r
import random
import urllib.request as urllib
from fontpreview import *
from pyunpack import Archive
from py7zr import unpack_7zarchive
from fontTools import ttLib
import requests
import re
import zipfile
from time import *

member_count_alert = 1000
magifonts_id = keys.gid
font_ext = ("ttf", "otf")
zip_ext= ("zip","7z","rar")
todof = "file_17.ttf"
file_responses = ["This your OP font by your OP group", "You are the best!!", "You are OP", "Keep it up, i am waiting for more...","Here you go!", "Thanks for being one of us","Check this out!!", "Take this...","I hope you like it!", "Done!!","Compiled...","Finished!"]
FONT, BOLD, ITALICS = range(3)
PREVIEW = 1
bot = Bot(keys.API_KEY)

def getFilename_fromURL(url):
    cd = requests.get(url, allow_redirects=True).headers.get('content-disposition')

    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def member_join(update, context):
    
    for member in update.message.new_chat_members:
        member_count = int(bot.get_chat_members_count(update.message.chat_id))
        if member_count%member_count_alert == 0:
            message = update.message.reply_text(f"{member.full_name} is the "+str(member_count)+"th to join the group!!\nWhoo!! "+str(member_count)+" members!")
            try:
                bot.pin_chat_message(update.message.chat_id, message.message_id)
            except:
                update.message.reply_text("I can't even pin a message.. dang!")

def preview_command(update,context):
    clearcache()
    if update.message.reply_to_message:
        msg = bot.send_message(update.message.chat_id, "Gimme a minute")
        #keyboard = [
        #[
        #    InlineKeyboardButton("OMF (Recommended)", callback_data='OMF'),
        #    InlineKeyboardButton("MFFM", callback_data='MFFM'),
        #]
        #]
        
        #reply_markup = InlineKeyboardMarkup(keyboard)
        #context.user_data["file_request"] = update.message.reply_to_message
        #context.user_data["preview_message"] = update.message
        
        preview(update,context,update.message.reply_to_message)
        bot.deleteMessage(update.message.chat_id, msg.message_id)
        #bot.send_message(update.message.chat_id, "Ignore any missing glyphs or broken characters.\nThose will be replaced by Roboto font when flashing the module...")
    else:
        update.message.reply_text("Reply to a valid font file...")

def preview(update,context,doc):
    os.chdir(orig_dir)
    if doc.document.file_name.split(".")[-1].lower() in font_ext:
        os.chdir("preview")
        doc.document.get_file().download(custom_path=remove_ext(doc.document.file_name)+".ttf")
        pic = previewfont(None, remove_ext(doc.document.file_name)+".ttf")
        os.chdir(orig_dir)
        os.chdir("preview")
        bot.send_photo(update.message.chat_id, open("preview.png", "rb"))
    elif doc.document.file_name.split(".")[-1].lower() in zip_ext:
        os.chdir("preview")
        doc.document.get_file().download(custom_path="preview_zip."+doc.document.file_name.split(".")[-1].lower())
        print("gonna extract")
        create_dir("preview_zip")
        extract("preview_zip."+doc.document.file_name.split(".")[-1].lower(),"preview_zip/")
        ffiles = []
        ffiles = list(find("*.otf", "preview_zip"))
        regular_font = ""
        if len(ffiles)<1:
            ffiles = list(find("*.ttf", "preview_zip"))
        regular_font = find_font(ffiles,"Regular", remove_ext(doc.document.file_name))
        bold_font = find_font(ffiles,"Bold")
        light_font = find_font(ffiles,"Light")
        italic_font = find_font(ffiles,"Italic")
        print(regular_font)
        if regular_font:
            #regular_font = ffiles[i]
            os.chdir(orig_dir)
            pic = previewfont(None, regular_font, bold_font, light_font, italic_font)
            os.chdir(orig_dir)
            os.chdir("preview")
            bot.send_photo(update.message.chat_id, open("preview.png", "rb"))
            os.chdir(orig_dir)
                #break
        
    else:
        update.message.reply_text("Send valid font file/zip wen?")
    

def start_command(update, context):
    update.message.reply_text("I'm alive bRUH!...")
    
def help_command(update,context):
    update.message.reply_text("Search for it on Google, duh. Tag @TheSc1enceGuy for some very important questions...")
    
def ccache_command(update,context):
    clearcache()
    update.message.reply_text("Done")  
    
def about_command(update,context):
    #update.message.reply_text("Memebers count: "+str(bot.get_chat_members_count(update.message.chat_id)))
    update.message.reply_text("This bot will convert any sent font (.ttf or .otf) or web downloaded zip file to a magisk flashable zip... enjoy!")

def maker_command(update,context):
    update.message.reply_text("@TheSc1enceGuy(akshit singh) has made this bot...")

def owner_command(update,context):
    update.message.reply_text("@TheSc1enceGuy(akshit singh) is my father... and he is the owner too lel ;)")
    
def handle_message(update,context):
    if hasattr(update.message, "text"):
        text = str(update.message.text).lower()
        if r.sample_responses(text) not in (""):
            update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    print(f"Update {update} caused error {context.error}")
    error = str(context.error).lower()
    try:
        chat_id = update.message.chat_id
    except:
        chat_id = magifonts_id
    if error == "timed out":
        bot.send_message(chat_id,"Request Timed Out. Pls try again...")
        return
    elif error == "broken file":
        bot.send_message(chat_id,"File is broken LoL xD.\nSorry, I feel sad for you...")
        return
    elif error == str("Message can't be deleted").lower():
        print("I cant delete a message either lol")
    else:
        bot.send_message(chat_id,"An Error Occured...")
       

#OMF update function
def updateomf(update, context):
    if update.message.from_user.id == 1441717868 :
        try:
            print("updating OMF")
            os.chdir(orig_dir)
            
            shutil.rmtree("OMF_old")
            
            if os.path.isdir('OMF_reverted'):
                shutil.rmtree("OMF_reverted")
            
            os.rename("OMF", "OMF_old")
            
            urllib.urlretrieve("https://gitlab.com/nongthaihoang/omftemplate/-/archive/master/omftemplate-master.zip", "OMF.zip")
            
            # os.mkdir("OMF")
            extract("OMF.zip", os.getcwd())
            os.rename("omftemplate-master", "OMF")
            print(os.listdir())
            
            update.message.reply_text("Updated OMF successfully")
            
        except:
            update.message.reply_text("An error occured, which might have caused some messups. so better check that out asap...")
        os.chdir(orig_dir)
        initialize()
        fix_update()
    else:
        update.message.reply_text("Only my owner can execute this cmd")
    
    

#OMF revert function
def revertomf(update, context):
    if update.message.from_user.id == 1441717868 :
        print("reverting OMF")
        os.chdir(orig_dir)
        if os.isdir('OMD_reverted') or os.isdir('OMF_old'):
            try:
                
                if os.path.isdir('OMF_reverted'):
                    os.rename('OMF', 'OMF_old')
                    
                    os.rename('OMF_reverted', "OMF")
                    
                else:
                    os.chdir(orig_dir)
                    os.rename("OMF", "OMF_reverted")
                    
                    os.rename("OMF_old", "OMF")
                    
                    update.message.reply_text("Revert successful!")
            except:
                update.message.reply_text("An error occured, that too during Reverting,,. so better check that out asap!")
            os.chdir(orig_dir)
        else:
            update.message.reply_text("Nothing to revert sir!")
        initialize()
    else:
        update.message.reply_text("Only my owner can execute this cmd")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    initialize()
    
    dispatcher.add_handler(CommandHandler("preview",preview_command))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help",help_command))
    dispatcher.add_handler(CommandHandler("ccache",ccache_command))
    dispatcher.add_handler(CommandHandler("creator",maker_command))
    dispatcher.add_handler(CommandHandler("owner",owner_command))
    dispatcher.add_handler(CommandHandler("about",about_command))
    dispatcher.add_handler(CommandHandler("module",module_command))
    dispatcher.add_handler(CommandHandler("ffiles",ffiles_command))
    dispatcher.add_handler(CommandHandler("delete",delete_command))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern="^OMF||MFFM||advanced_module||cancel_module$"))
    dispatcher.add_handler(CommandHandler("faketrigger",member_join))
    dispatcher.add_handler(CommandHandler("extractfont",extract_font))

    #OMF update and backup
    dispatcher.add_handler(CommandHandler("updateomf",updateomf))
    dispatcher.add_handler(CommandHandler("revertomf",revertomf))
    
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    
    dispatcher.add_error_handler(error)
    add_group_handle = MessageHandler(Filters.status_update.new_chat_members, member_join)
    dispatcher.add_handler(add_group_handle)
    
    adv_handler = ConversationHandler(
        entry_points=[CommandHandler("advanced",advanced_main)],
        states={
            TEMPLATE: [CallbackQueryHandler(template, pattern='^template$')],
            METRICS: [CallbackQueryHandler(metrics, pattern='^metrics$')],
            ASCENT: [CallbackQueryHandler(ascent, pattern='^ascent_advanced$')],
            DESCENT: [CallbackQueryHandler(descent, pattern='^descent_advanced$')],
            LINEGAP: [CallbackQueryHandler(linegap, pattern='^linegap_advanced$')],
            EM: [CallbackQueryHandler(em, pattern='^em_advanced$')],
            ASCENT_R: [MessageHandler(Filters.text, ascent_received)],
            DESCENT_R: [MessageHandler(Filters.text, descent_received)],
            LINEGAP_R: [MessageHandler(Filters.text, linegap_received)],
            EM_R: [MessageHandler(Filters.text, em_received)],
        },
        fallbacks=[CallbackQueryHandler(button, pattern='^cancel_advanced$')],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    #dispatcher.add_handler(adv_handler)
    
    # Start the Bot
    updater.start_polling(drop_pending_updates=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def extract(file, location):
    create_dir(location)
    if file.split(".")[-1] == "7z":
        shutil.unpack_archive(file, location)
    else:
        Archive(file).extractall(location)

def capscheck(x):
    lower_tfontsall = list(map(lambda x : x.split(".")[0].lower(), tfontsall.copy()))
    if x in lower_tfontsall:
        return list(map(lambda x : x.split(".")[0], tfontsall.copy()))[lower_tfontsall.index(x)]

def delete_command(update, context):
    if update.message.reply_to_message.document:
        if update.message.reply_to_message.document.file_name.split(".")[-1] in zip_ext:
            clearcache()
            doc = update.message.reply_to_message.document
            os.chdir(orig_dir)
            os.chdir("ziptodo")
            doc.get_file().download(custom_path=doc.file_name)
            create_dir("to_delete")
            extract(doc.file_name,"to_delete/")
            
            
            ffiles = find("*.ttf", "to_delete")
            find("*.otf","to_delete") if not ffiles else ffiles
            
            for attr in context.args:
                if attr in list(map(lambda x : name_from_dir(x), ffiles)):
                    os.remove(find(attr, "to_delete")[0])
                else:
                    to_del = capscheck(attr)
                    font = find_font(ffiles, to_del, remove_ext(doc.file_name))
                    if font:
                        os.remove(font)
                    else:
                        update.message.reply_text("Couldn't find that...")
                        return
                print("makin archive")     
                shutil.make_archive(remove_ext(doc.file_name)+"_mod","zip","to_delete/")
                bot.send_document(magifonts_id, open(remove_ext(doc.file_name)+"_mod.zip", "rb"))
                return
        else:
            update.message.reply_text("Are you sure that that is a zip file?\nYou might wana get your eyes tested...")
    else:
        update.message.reply_text("Reply to a zip...")

def module_command(update,context):
    if update.message.reply_to_message:
        if int(update.message.reply_to_message.document.file_size) <= 20000000:
            print(int(update.message.reply_to_message.document.file_size))
            keyboard = [
            [
                InlineKeyboardButton("OMF (Recommended)", callback_data='OMF'),
                InlineKeyboardButton("MFFM", callback_data='MFFM'),
            ],
            #[InlineKeyboardButton("Advanced", callback_data='advanced')],
            [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.user_data["file_request"] = update.message.reply_to_message
            context.user_data["module_message"] = update.message
            update.message.reply_text('What Type of Module?', reply_markup=reply_markup)
            
            msgarray = []
            if "/module " in update.message.text:
                msgarray = list(map(lambda x: x.replace('\"', ""), update.message.text.replace("/module ", "").split(" ")))
            filename=None
            #print("filename: ",msgarray)
            if len(msgarray) >= 1:
                filename = msgarray[0]
            #ttfdownload(update,update.message.reply_to_message,filename)
            #bot.delete_message(update.message.chat_id,msg.message_id)
        else:
            update.message.reply_text("File is too big sar...")
    else:
        update.message.reply_text("Reply to a font file/zip bro.")
        
TEMPLATE, METRICS, ASCENT, DESCENT, LINEGAP, EM, ASCENT_R, DESCENT_R, LINEGAP_R, EM_R = range(10)
    
def ascent_received(update, context):
    print("ascent_r")
    bot.delete_message(update.message.chat_id, update.message.message_id)
    context.user_data["advanced"]["metrics_msg"].edit_message_text("Ascent has been saved too: ", update.message.text)
    return METRICS

def descent_received(update, context):
    print("descent_r")
    bot.delete_message(update.message.chat_id, update.message.message_id)
    context.user_data["advanced"]["metrics_msg"].edit_message_text("Descent has been saved too: ", update.message.text)
    return METRICS

def linegap_received(update, context):
    print("linegap_r")
    bot.delete_message(update.message.chat_id, update.message.message_id)
    context.user_data["advanced"]["metrics_msg"].edit_message_text("LineGap has been saved too: ", update.message.text)
    return METRICS

def em_received(update, context):
    print("em_r")
    bot.delete_message(update.message.chat_id, update.message.message_id)
    context.user_data["advanced"]["metrics_msg"].edit_message_text("UPM has been saved too: ", update.message.text)
    return METRICS


def button(update, context):
    query = update.callback_query
    
    
    def module():
        query = update.callback_query
        query.answer()
    
        if query.data in ("OMF","MFFM"):
            query.edit_message_text(text=f"Processing: {query.data}")
            print(context.user_data.get("file_request", "File Request Not found..."))
            file = context.user_data.get("file_request", "File Request Not found...")
        
        usermsg = context.user_data["module_message"]
        msgarray = []
        if "/module " in usermsg.text:
            msgarray = list(map(lambda x: x.replace('\"', ""), usermsg.text.replace("/module ", "").split(" ")))
        filename=None
        
        #print("filename: ",msgarray)
        if len(msgarray) >= 1:
            filename = msgarray[0]
        
        if query.data == "OMF":
            ttfdownload("OMF", usermsg,file, filename, keys.omf_dir, keys.omffonts_dir, keys.omf_r, keys.omf_b, keys.omf_i, keys.omf_all, keys.omf_single)
        
        if query.data == "MFFM":
            ttfdownload("MFFM", usermsg,file, filename, keys.mffm_dir, keys.mffmfonts_dir, keys.mffm_r, keys.mffm_b, keys.mffm_i, keys.mffm_all, keys.mffm_single)
        
        bot.deleteMessage(query.message.chat_id, query.message.message_id)
        bot.deleteMessage(usermsg.chat_id, usermsg.message_id)
            
            
        
        def compile_advanced():
            print("")
        if query.data == "template":
            template()
        if query.data == "advanced":
            main()
        if query.data == "metrics":
            metrics()
        if query.data == "MFFM_advanced":
            context.user_data["advanced"]["template"] = "MFFM"
            metrics()
        if query.data == "OMF_advanced":
            context.user_data["advanced"]["template"] = "OMF"
            metrics()
        if query.data == "ascent_advanced":
            ascent()
        if query.data == "descent_advanced":
            descent()
        if query.data == "linegap_advanced":
            linegap()
        if query.data == "em_advanced":
            em()
        
        if "advanced" in context.user_data:
            print(context.user_data["advanced"])
        #if query.data == "metrics":
        #    metrics()
    
    def cancel():
        query.answer()
        query.edit_message_text(text="Request Cancelled...")
        return
    
    def proceed():
        if query.data == "OMF" or query.data == "MFFM":
            module()
        if query.data == "advanced_module":
            advanced()
        if query.data == "cancel_module":
            cancel()
        if query.data in ("template", "metrics","advanced","MFFM_advanced","OMF_advanced","ascent_advanced","descent_advanced","linegap_advanced","em_advanced"):
            query.answer()
            advanced()
        return
    
    userMessage = None
    if update.callback_query.message.reply_to_message:
        if update.callback_query.message.reply_to_message.from_user.username == update.effective_user.username:
            userMessage = update.callback_query.message.reply_to_message
            proceed()
        else:
            return
    else:
        proceed()
    
    return
    

    
    
    

tfonts = ["Regular.ttf"]

tfontsr = ["Regular.ttf","Light.ttf","Thin.ttf"]

tfontsb = [ "Medium.ttf","Black.ttf","Bold.ttf"]

tfontsi = ["BlackItalic.ttf","BoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ThinItalic.ttf"]#todof= file...

tfontsall = ["Regular.ttf","Light.ttf","Thin.ttf","Medium.ttf","Black.ttf","Bold.ttf","BlackItalic.ttf","BoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ThinItalic.ttf"]

#os.chdir("C:/Users/rsran/Downloads/akshit ka fonts")

def advanced(update,context):
    print("advanced: ",query.data)
    keyboard = [
    [InlineKeyboardButton("Advanced", callback_data='advanced')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["file_request"] = update.message.reply_to_message
    context.user_data["module_message"] = update.message
    update.message.reply_text('What Type of Module?', reply_markup=reply_markup)

query = None
def advanced_main(update,context):
    query = update.callback_query
    print("advanced_main")
    context.user_data["advanced"] = {}
    keyboard = [
    [
        InlineKeyboardButton("Template", callback_data='template'),
        InlineKeyboardButton("Metrics", callback_data='metrics'),
    ],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose Template: ', reply_markup=reply_markup)
def template(update,context):
    query = update.callback_query
    print("template")
    keyboard = [
    [
        InlineKeyboardButton("OMF", callback_data='OMF_advanced'),
        InlineKeyboardButton("MFFM", callback_data='MFFM_advanced'),
    ],
    [InlineKeyboardButton("Back", callback_data='advanced')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Choose Template: ', reply_markup=reply_markup)
    return METRICS
def metrics(update,context):
    query = update.callback_query
    keyboard = [
    [
        InlineKeyboardButton("Ascent", callback_data='ascent_advanced'),
        InlineKeyboardButton("Descent", callback_data='descent_advanced'),
        InlineKeyboardButton("LineGap", callback_data='linegap_advanced'),
        InlineKeyboardButton("unitsPerEm", callback_data='em_advanced')
    ],
    [InlineKeyboardButton("Back", callback_data='advanced')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Choose Template: ', reply_markup=reply_markup)
    print("metrics")
    #compile_advanced()
    return



def ascent(update,context):
    query = update.callback_query
    keyboard = [
    [InlineKeyboardButton("Back", callback_data='metrics')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    print(context.user_data)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Options: ', reply_markup=reply_markup)
    context.user_data["advanced"]["metrics_msg"] = bot.send_message(query.message.chat_id, "Reply to this message by sending ascent in numbers.\nex. 1900"+(("\n@"+userMessage.from_user.username) if userMessage else ""), reply_markup=ForceReply(selective = True if userMessage else False))
    return ASCENT_R

def descent(update,context):
    query = update.callback_query
    keyboard = [
    [InlineKeyboardButton("Back", callback_data='metrics')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Options: ', reply_markup=reply_markup)
    context.user_data["advanced"]["metrics_msg"] = bot.send_message(query.message.chat_id,"Reply to this message by sending descent in numbers.\nex. -500"+(("\n@"+userMessage.from_user.username) if userMessage else ""), reply_markup=ForceReply(selective = True if userMessage else False))
    return DESCENT_R

def linegap(update,context):
    query = update.callback_query
    keyboard = [
    [InlineKeyboardButton("Back", callback_data='metrics')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Options: ', reply_markup=reply_markup)
    context.user_data["advanced"]["metrics_msg"] = bot.send_message(query.message.chat_id,"Reply to this message by sending linegap in numbers.\nex. 0"+(("\n@"+userMessage.from_user.username) if userMessage else ""), reply_markup=ForceReply(selective = True if userMessage else False))
    return LINEGAP_R

def em(update,context):
    query = update.callback_query
    keyboard = [
    [InlineKeyboardButton("Back", callback_data='metrics')],
    [InlineKeyboardButton("Cancel", callback_data='cancel_module')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Options: ', reply_markup=reply_markup)
    context.user_data["advanced"]["metrics_msg"] = bot.send_message(query.message.chat_id,"Reply to this message by sending unitsPerEm in numbers.\nex. 2048"+(("\n@"+userMessage.from_user.username) if userMessage else ""), reply_markup=ForceReply(selective = True if userMessage else False))
    return EM_R



def modulify(template_type, templatedir, fontdir, zipname = None, fonts = ["Regular.ttf"]):
    print("modulify me hu")
    if not zipname:
        zipname=remove_ext(todof)
    zipname = zipname.replace("[Magifonts]","")+"[Magifonts]"
    os.chdir(orig_dir)
    os.chdir(fontdir)
    processfonts([["", "../../todo/"+todof]])
    for i in range(0,len(fonts)):
        shutil.copyfile(src="../../todo/"+todof , dst=fonts[i])
    print("copied files")
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir(templatedir)
    edit_module_prop(remove_ext(todof), templatedir, template_type)
    os.chdir(orig_dir)
    shutil.make_archive("magiFont/"+zipname, 'zip', templatedir)
    print("archive ready")
    return zipname
    
def modulifybi(fname,zipname=False):
    print(["moodulify bi reached",fname])
    if not zipname:
        zipname=fname.split(".")[0]
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
    os.chdir(keys.fonts_dir)
    for i in range(0,len(tfontsr)):
        shutil.copyfile(src="../../todo/"+fname , dst=tfontsr[i])
    
    for i in range(0,len(tfontsb)):
        shutil.copyfile(src="../../todo/"+fnameb , dst=tfontsb[i])
        
    for i in range(0,len(tfontsi)):
        shutil.copyfile(src="../../todo/"+fnamei , dst=tfontsi[i])
    print(4)
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir(keys.template_dir)
    edit_module_prop(remove_ext(fname))
    os.chdir(orig_dir)
    #print(zipname)
    shutil.make_archive("magiFont/"+zipname, 'zip', keys.template_dir)
    return zipname
    #print(5)
    
def edit_module_prop(fname, templatedir, template_type = "OMF"):
    os.chdir(orig_dir)
    os.chdir(templatedir)
    os.rename('module.prop','module.txt')
    if template_type == "OMF":
        prop_list = ["id=Magifonts_omf_font_module\n","name="+fname+"\n","Moduleversion=v2021.05.23\n""versionCode=2021052301\n","author=nongthaihoang @GitLab; MFFM; @TheSc1enceGuy\n","description=OMF Advanced font installer for Android. Module prepared by @magifont_bot. Join @MFFMDisc / @Magifonts_Support for more.\n"]
    else:
        prop_list = ["id=Magifonts_mffm_font_module\n","name="+fname+"\n","Moduleversion=v2021.05.23\n""versionCode=2021052301\n","author=MFFM; @TheSc1enceGuy\n","description=MFFM Advanced font installer for Android. Module prepared by @magifont_bot. Join @MFFMDisc / @Magifonts_Support for more.\n"]
    my_file = open("module.txt", "w")
    my_file.write("".join(prop_list))
    my_file.close()
    os.rename('module.txt','module.prop')
    os.chdir(orig_dir)

def remove_ext(filewext):
    file = filewext.split(".").copy()
    file.pop(-1)
    strfile = ""
    for i in file:
       strfile+=str(i)
    return strfile


def extract_font(update,context):
    if update.message.reply_to_message.document:
        if update.message.reply_to_message.document.file_name.split(".")[-1] in zip_ext:
            clearcache()
            doc = update.message.reply_to_message
            os.chdir(orig_dir)
            os.chdir("ffiles")
            doc.document.get_file().download(custom_path="ffiles."+doc.document.file_name.split(".")[-1].lower())
            extract("ffiles."+doc.document.file_name.split(".")[-1].lower(), "fonts")
            ffiles = find("*.ttf", "fonts")
            if not ffiles:
                ffiles = find("*.otf", "fonts")
            if not ffiles:
                update.message.reply_text("It has no Fonts in .ttf ot .otf format! xD")
            else:
                ffiles_str=""
                #ffiles = list(map(lambda x : name_from_dir(x), ffiles))
                for i in ffiles:
                    if ffiles:
                        bot.send_document(update.message.chat_id, open(i,"rb"), caption=shortName(ttLib.TTFont(i))[0])
                        #ffiles_str += "\n"+i
                    else:
                        ffiles = i
                #update.message.reply_text(ffiles_str)
        else:
            update.message.reply_text("Reply to a .zip wen?")
    else:
        update.message.reply_text("Reply to a .zip file sar...")



def ffiles_command(update,context):
    if update.message.reply_to_message.document:
        if update.message.reply_to_message.document.file_name.split(".")[-1] in zip_ext:
            clearcache()
            doc = update.message.reply_to_message
            os.chdir(orig_dir)
            os.chdir("ffiles")
            doc.document.get_file().download(custom_path="ffiles."+doc.document.file_name.split(".")[-1].lower())
            extract("ffiles."+doc.document.file_name.split(".")[-1].lower(), "fonts")
            ffiles = find("*.ttf", "fonts")
            print(ffiles)
            print(os.getcwd())
            if not ffiles:
                ffiles = find("*.otf", "fonts")
            if not ffiles:
                update.message.reply_text("It has no Fonts in .ttf ot .otf format! xD")
            else:
                ffiles_str=""
                ffiles = list(map(lambda x : name_from_dir(x), ffiles))
                for i in ffiles:
                    if ffiles:
                        ffiles_str += "\n"+i
                    else:
                        ffiles = i
                update.message.reply_text(ffiles_str)
        else:
            update.message.reply_text("Reply to a .zip wen?")
    else:
        update.message.reply_text("Reply to a .zip file sar...")
def ttfdownload(template_type, docmsg, doc, zipname, templatedir, fontdir, fontsr = tfontsr, fontsb = tfontsb, fontsi = tfontsi, fontsall = tfontsall, single_file = tfonts):

    if not zipname:
        zipname = remove_ext(doc.document.file_name).replace("[Magifonts]","")
    print(doc)

    os.chdir(orig_dir)
    clearcache()
    try:
        print("ttf download requested by @"+docmsg.from_user.username)
    except:
        print("ttf download requested")
        
    
    if doc.document.file_name.split(".")[-1].lower() in font_ext:
        print(os.getcwd())
        os.chdir("todo")

        doc.document.get_file().download(custom_path=doc.document.file_name)
        global todof
        for dirs,file,name in walklevel(os.getcwd()):
            print("DIRECTORY LOCATION ABHI KI:")
            print(os.getcwd())
            todof=name[-1]
            print(name)
        
        if todof.split(".")[-1].lower() in font_ext:
            os.chdir("../")
            to_send = modulify(template_type, templatedir, fontdir, zipname, single_file)
            os.chdir(orig_dir)
            os.chdir("magiFont")
            print("sending...")
            flashable_in = "Magisk / TWRP (Read Instructions)" if (template_type=="OMF") else "Magisk"
            bot.send_document(magifonts_id, open(to_send+".zip",'rb'),caption=random.choice(file_responses)+"\nFont Name: "+zipname+"\nTemplate used: "+template_type+"\nFlashable in: "+flashable_in+"\nTime: "+strftime("%a, %d %b %Y", gmtime()))
            try:
                bot.send_message(magifonts_id,"Here you go! - @"+docmsg.from_user.username)
            except:
                bot.send_message(magifonts_id,"Here you go!")
            if not str(doc.chat_id) == str(magifonts_id):
                doc.reply_text("Your file has been posted in @magifonts_support")
                # doc.reply_text("Checkout #submit-sample\nThanks for being a part of the awesome community!!")
            os.chdir("../")
        else:
            doc.reply_text("invalid file type!")
            os.chdir("../")
    elif doc.document.file_name.split(".")[-1].lower() in zip_ext:
        os.chdir("ziptodo")
        doc.document.get_file().download(custom_path=doc.document.file_name)
        print("file downloaded!")
        extract(doc.document.file_name, remove_ext(doc.document.file_name))
        print("file unzipped: ",remove_ext(doc.document.file_name))
        ffiles = find("*.ttf",remove_ext(doc.document.file_name))
        print(0)
        origflist = deforigflist( keys.omf_all if template_type.lower() == "omf" else keys.mffm_all)
        flist = origflist.copy()
        if not ffiles:
            print("otf")
            ffiles = find("*.otf",remove_ext(doc.document.file_name))
        
        if not ffiles:
            doc.reply_text("This zip has no .ttf or .otf file... :(")
            return
        
        #print("files: ",ffiles[0])
        
        if len(ffiles) == 1:
            shutil.copyfile(ffiles[0], os.path.join("../",fontdir,"Regular.ttf"))
            flist[flist.index(["Regular",False])][1] = ffiles[0]
        else:
            
            for j in range(len(fontsall)):
                #print("filename..")
                x = find_font(ffiles, remove_ext(fontsall[j]),remove_ext(doc.document.file_name), "filename")
                if x:           
                    if [remove_ext(name_from_dir(fontsall[j])),False] in flist:
                        flist[flist.index([remove_ext(name_from_dir(fontsall[j])),False])][1] = x
            #print("\n\n gonna fallback \n\n")
            for j in range(len(fontsall)):
               
                    if [remove_ext(name_from_dir(fontsall[j])),False] in flist:
                        #print("fallback")
                        x = find_font(ffiles, remove_ext(fontsall[j]),remove_ext(doc.document.file_name), "fontname")
                        if x:
                            #print("fallback: ",x, " for ", remove_ext(fontsall[j]))
                            #print("applied")
                            flist[flist.index([remove_ext(name_from_dir(fontsall[j])),False])][1] = x
            
            
            if not template_type.lower() == "omf":
                for i in range(len(ffiles)):
                #for j in range(len(fontsall)):
                    deffonts = definefonts(flist)
                    if not remove_ext(fontsall[j]) in deffonts:
                        
                        nearest = nearest_weight2(flist,remove_ext(fontsall[j]), deffonts)
                        if nearest:
                            x = find_font(ffiles, nearest,remove_ext(doc.document.file_name))
                            if x:
                                flist[flist.index([remove_ext(fontsall[j]),False])][1] = x
                            else:
                                x = find_font(ffiles, "Regular",remove_ext(doc.document.file_name))
                                if x:
                                    flist[flist.index([remove_ext(fontsall[j]),False])][1] = x
                        
            
            paste_to_template(flist,"ziptodo",fontdir)
        
        edit_module_prop(zipname,templatedir)
        
        os.chdir("ziptodo")
        processfonts(flist)
        os.chdir(orig_dir)

        print("magiFont/"+remove_ext(doc.document.file_name)+".zip")
        shutil.make_archive("magiFont/"+zipname+"[Magifonts]", "zip",templatedir)
        if os.stat("magiFont/"+zipname+"[Magifonts]"+".zip").st_size <= 20000000:
            bot.send_document(magifonts_id, open("magiFont/"+zipname+"[Magifonts]"+".zip",'rb'),caption=random.choice(file_responses)+"\nFont Name: "+zipname+"\nTemplate used: "+template_type+"\nFlashable in: "+"Magisk"+"\nTime: "+strftime("%a, %d %b %Y", gmtime()))
            try:
                bot.send_message(magifonts_id,"Here you go! - @"+docmsg.from_user.username)
            except:
                bot.send_message(magifonts_id,"Here you go!")

            if not (docmsg.chat_id == magifonts_id):
                bot.send_message(docmsg.chat_id,"The file has been posted to @magifonts_support")
        else:
            bot.send_message(docmsg.chat_id,"The file is too big to send.\nTelegram has a limit of max 20mb for bots to send files...")
        os.chdir("../")
    else:                
        os.chdir("../")
        doc.reply_text("Sar, sorry but I can't make this to a module. Pls gib font(ttf or otf) file/zip :(")
    
        #os.chdir("../magiTemplate/system/fonts")
        #for i in range(0,len(tfontsr)):
        #    shutil.copyfile(src="../../../todo/"+fname , dst=tfontsr[i])
origflist = []
def get_key(dictioary, attr):
    for keys,values in dictionary.items():
        if attr == keys:
            return values
    return False

def processfonts(fontslist, em = None, ascent = None, descent = None, linegap = None):
    em = em if em else None
    ascent = ascent if ascent else 1900
    descent = descent if descent else -500
    linegap = linegap if linegap else 0
    fonts = []
    defined = []
    for i in fontslist:
        if i[1] and i[1] not in defined:
            defined.append(i[1])
    print("Processing fonts...\n", defined,"\n\n")
    
    
    
    
    
    fonts = fontslist#[find_font(defined, "Regular"), find_font(defined, "Italic")]
    for i in range(len(defined)):
        em = em if em else None
        ascent = ascent if ascent else 1900
        descent = descent if descent else -500
        linegap = linegap if linegap else 0
        if defined[i]:
            tt = ttLib.TTFont(defined[i])
            #if tt["head"].unitsPerEm >= 2040:
            #    tt["hhea"].ascent = 1800
            #else:
            #    tt["hhea"].ascent = 900
            if not em:
                ascent = int((ascent*tt["head"].unitsPerEm)/2048)
                descent = int((descent*tt["head"].unitsPerEm)/2048)
            tt["hhea"].ascent = ascent
            tt["OS/2"].sTypoAscender = ascent
            tt["hhea"].descent = descent
            tt["OS/2"].sTypoDescender = descent
                
            tt["head"].unitsPerEm = em if em else tt["head"].unitsPerEm
            if em:
                tt["hhea"].ascent = ascent
                tt["OS/2"].sTypoAscender = ascent
            else:
                if int(tt["head"].unitsPerEm) == 2048:
                    tt["hhea"].ascent = 1900
                    tt["OS/2"].sTypoAscender = 1900
                if int(tt["head"].unitsPerEm) == 1000:
                    tt["hhea"].ascent = 900
                    tt["OS/2"].sTypoAscender = 900
            
            tt["hhea"].lineGap = linegap
            tt["OS/2"].sTypoLineGap = linegap
            
            
            if em:
                tt["hhea"].descent = descent
                tt["OS/2"].sTypoDescender = descent
            else:
                if int(tt["head"].unitsPerEm) == 2048:
                    tt["hhea"].descent = -500
                    tt["OS/2"].sTypoDescender = -500
                if int(tt["head"].unitsPerEm) == 1000:
                    tt["hhea"].descent = -270
                    tt["OS/2"].sTypoDescender = -270
            #tt.saveXML("lesse")
            print("fixed: ", name_from_dir(defined[i]), tt["hhea"].ascent, tt["hhea"].descent, tt["hhea"].lineGap, tt["head"].unitsPerEm)
            tt.save(defined[i])
            
def paste_to_template(flist,src,dst):
    os.chdir(orig_dir)
    for i in range(len(flist)):
        if flist[i][1]:
            if os.path.exists(src+"/"+flist[i][1]):
                shutil.copyfile(src+"/"+flist[i][1], dst+"/"+flist[i][0]+".ttf")

def modulify2(flist,src,dst,definedfonts,filedst):
    os.chdir(orig_dir)

    if "Regular" in definedfonts:
        if len(definedfonts) == 1:
            shutil.copyfile(src+"/"+flist[2][1], dst+"/Regular.ttf")
        else:
            for i in range(len(flist)):
                if flist[i][1]:
                    shutil.copyfile(src+"/"+flist[i][1], dst+"/"+flist[i][0]+".ttf")
                
            for i in range(len(flist)):
                if not flist[i][1]:
                    shutil.copyfile(src+"/"+return_font(flist,"Regular"), dst+"/"+flist[i][0]+".ttf")
    edit_module_prop(remove_ext(filedst.split("/")[-1]))
    shutil.make_archive(remove_ext(filedst), 'zip', keys.template_dir)
    return filedst
    

def nearest_weight2(defined_fonts, font):
    deffonts = defined_fonts.copy()
    if not deffonts[0].split(".")[-1] in font_ext:
        deffonts = list(map(lambda x:x+".ttf", deffonts))
    #The flist should be a copy of origflist
    #The font var is the type of font we need to find the nearest_weight of. (ex. BlackItalic)
    allflist = [tfontsr.copy(), tfontsb.copy(), tfontsi.copy()]
    for i in range(len(allflist)):
        
        if font+".ttf" in allflist[i]:

            font_index = allflist[i].index(font+".ttf")
            forward_length = (len(allflist[i])-font_index)-1
            backward_length = (len(allflist[i])-forward_length)-1 
            
            for j in range(0,max(forward_length, backward_length)+1):
                if j <= forward_length:
                    if allflist[i][font_index+j] in deffonts:
                        return remove_ext(allflist[i][j])
                if j <= backward_length:
                    if allflist[i][font_index-j] in deffonts: 
                        return remove_ext(allflist[i][j])
                    
    return "Regular"    
    
def nearest_weight2(flist, x, deffonts):
    if x in deffonts:
        return return_font(flist, x)
    else:
        allf_list = [tfontsr.copy(),tfontsb.copy(),tfontsi.copy()]
        for array in allf_list:
            if x+".ttf" in array:
                l = (len(array)-array.index(x+".ttf"))-1
                i = (len(array)-l)-1
                for j in range(1,max(l,i)+1):
                    
                    if l>=j:
                        if  remove_ext(array[array.index(x+".ttf")+j]) in deffonts:
                            return remove_ext(array[array.index(x+".ttf")+j])
                            break
                    if i>=j:
                        if remove_ext(array[array.index(x+".ttf")-j]) in deffonts:
                            return remove_ext(array[array.index(x+".ttf")-j])
                            break
        
        #return return_font(flist, "Regular")
    if "Regular" in definedfonts:
        print("regular")
        return "Regular"
        
definedfonts=[]
def definefonts(flist):
    global definedfonts
    definedfonts=[]
    for i in flist:
        if i[1]:
            if not i[0] in definedfonts:
                definedfonts.append(i[0])
                
    return definedfonts

def return_font(array, value):
    if value=="first_element":
        for i in array:
            if not i[1] == False:
                return i[1]
    for i in array:
        if i[0] == value:
            return i[1]

def previewfont(font_name,fname = None,fname2 = None,fname3 = None,fname4 = None):
    fname2 = fname2 if fname2 else fname
    fname3 = fname3 if fname3 else fname
    fname4 = fname4 if fname4 else fname
    
    if not fname:
        raise Exception("fname not provided to previewfont()")
    print(name_from_dir(fname))
    bg_color = (0, 43, 54)
    fg_color = (0,160,153)
    fg_color2 = (159,255,163)
    os.chdir(orig_dir)
    os.chdir("preview")
    font_name = font_name if font_name else shortName(ttLib.TTFont(fname))[1] if shortName(ttLib.TTFont(fname))[1] else "font"
    
    print(0.1, " - ", font_name)
    #print(fdir)
    #print(os.path.join(os.getcwd(), fdir))
    header = fb = FontBanner(fname, 'landscape')
    body = fb2 = FontBanner(fname2, 'landscape')
    footer = fb3 = FontBanner(fname3, 'landscape')
    fb4 = FontBanner(fname4, 'landscape')
    fw = FontWall([fb,fb2,fb3,fb4],1,mode = "horizontal")
    fb.font_text = 'Checkout @Magifont_Support\nfor instant awesome fonts and previews!!'
    fb.bg_color = bg_color
    fb.fg_color = fg_color2
    
    fb.set_font_size(80)
    fb.set_text_position('center')
    # Modify properties of second banner
    fb2.font_text = 'Ignore any broken glyphs or characters as\nthey will be replaced by the default Roboto\nwhen flashing the magisk module...'
    fb2.bg_color = bg_color
    fb2.fg_color = fg_color
    fb2.set_font_size(70)
    fb2.set_text_position('center')
    # Modify properties of third banner
    fb3.font_text = 'Aa   Bb   Cc   Dd   Ee   Ff   Gg\n\n1!   2@   3#   4$   5%   6^   7&'
    fb3.bg_color = bg_color
    fb3.fg_color = fg_color
    fb3.set_font_size(90) 
    fb3.set_text_position('center')                 # the font is resized automatically because it exceeds the size of the banner
    # Modify properties of last banner
    fb4.font_text = 'By the way, th1s is just a sample for fonts.\nHow is this '+font_name+' btw? Do you like it?'
    fb4.bg_color = bg_color
    fb4.fg_color = fg_color
    fb4.set_font_size(70)
    fb4.set_text_position('center')
    fw.draw(1)
    fpage = FontPage()
    #fpage.set_header(header)
    #fpage.set_body(body)
    #fpage.set_footer(footer)
    #fpage.draw()
    
    print(0.2)
    os.chdir(orig_dir)
    os.chdir("preview")
    #fpage.save('preview.png')
    fw.save('preview.png')
    return "preview.png"
    
def deforigflist(all_fonts):
    arr = []
    for i in all_fonts:
        arr.append([remove_ext(i), False])
    return arr

def clearcache():
    origflist = deforigflist(keys.omf_all)
    os.chdir(orig_dir)
    wipefiles("todo")
    wipefiles("magiFont")
    wipefiles("ziptodo")
    wipefiles(keys.fonts_dir)
    wipefiles(keys.mffmfonts_dir)
    wipefiles(keys.omffonts_dir)
    wipefiles("preview")
    wipefiles("ffiles")
            
            
def wipefiles(path_to_folder):
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
        return name.copy()
    
def fix_update():
    os.chdir(orig_dir)
    os.chdir("OMF") 
    print(os.getcwd(), os.listdir())

    omfsh_data = open("customize.sh", errors = "ignore")
    string_list = omfsh_data.readlines()
    omfsh_data.close()
    omfsh = open("customize.sh", "w", errors = "ignore")
    new_string_list = map(tempfunc,string_list)
    omfsh.writelines(new_string_list)
    os.chdir(orig_dir)

def tempfunc(x):
    if x[0] == "#":
        if not x[1] == "#":
            return x[1:]
    return x
    # return x[1:] if x[0] == "#" and not x[1] == "#" else x

def initialize():
    try:
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    except:
        print("7z already registered")
    #else:
        #shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    os.chdir(orig_dir)
    create_dir("todo")
    create_dir("magiFont")
    create_dir("ziptodo")
    create_dir("ffiles")
    create_dir("preview/preview_zip")
    create_dir(keys.fonts_dir)
    create_dir(keys.mffmfonts_dir)
    create_dir(keys.omffonts_dir)
    clearcache()
    
def create_dir(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        return True
    
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                
                #result = os.path.join(str(result),os.path.join(root,name))
                result.append(os.path.join(root.replace("//","/"), name.replace("//","/")).replace("//","/"))
                #print(result)
    return list(map(lambda x : str(x).replace("\\","/"),result))

def regularfinder(x,filename = "```///2l"):
    if(("regular" in x.lower() or "mffm" in x.lower())):
        return True
    if not ("italic" in x.lower() or "black" in x.lower()  or "sembd" in x.lower() or "bold" in x.lower() or "medium" in x.lower() or  "thin" in x.lower() or "light" in x.lower() or "condensed" in x.lower()) and  filename.lower() in x.lower().split(' ')[0].split('-')[0]:
        return True
    return False

def find_font(name, font, filename = "``/`/...~", method = "filename"):
    #filename="hulu`124827@@#"
    a = []
    allfonts = name.copy()
    #print(allfonts)
    if os.path.exists(list(name)[0]) and not method == "filename":
        
        allfonts = list(map(lambda x : shortName(ttLib.TTFont(x))[0], allfonts))
        #print("method filename", font)
    else:
        allfonts = list(map(lambda x : remove_ext(name_from_dir(x)),allfonts)).copy()
        #print("allfonts\n",allfonts if font=="Regular" else font,"\n")
    a = []
    origlistt = allfonts.copy()
    if len(allfonts)== 1:
        #print("special case", allfonts, name[origlistt.index(allfonts[0])])
        return name[origlistt.index(allfonts[0])]
    
    origlistt = allfonts.copy()
    #if "condensed" not in font.lower():
    #    allfonts = list(filter(lambda x : "condensed" not in x.lower(), allfonts))
    
    #Filters unnescesary fonts
    for i in range(0,len(keys.font_styles)):
        if keys.font_styles[i].lower() in font.lower():
            #print("removing",keys.font_styles[i].lower(), "for",font.lower())
            allfonts = list(filter(lambda x : keys.font_styles[i].lower() in x.lower() and keys.font_styles[i].lower() in font.lower(), allfonts))
        else:
            allfonts = list(filter(lambda x : keys.font_styles[i].lower() not in x.lower(), allfonts))
    
    if len(allfonts) == 1:
        a = allfonts.copy()
    #print("v2", allfonts, font)
    #print(allfonts)
    if True:
        if font == "Regular":
            a = list(filter(lambda x : regularfinder(x,filename), allfonts))
            print("regular time...")
            #if not len(a) > 0:
            #    return name[0]
        
            
        if font == "Black":
            a = list(filter(lambda x : (("blck" in x.lower()) or ("black" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
    
        if font == "Medium":
            print("medium",  allfonts)
            a = list(filter(lambda x : (("-med" in x.lower()) or ("medium" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
    
        if font == "Light":
            a = list(filter(lambda x : (("-l" in x.lower()) or ("light" in x.lower())) and not ("extra" in x.lower() or "bold" in x.lower() or "italic" in x.lower()),allfonts))
    
        if font == "ExtraLight":
            a = list(filter(lambda x : (("extralight" in x.lower()) or ("extra light" in x.lower()) or "exlight" in x.lower()) and not ("bold" in x.lower() or "italic" in x.lower() or "thin" in x.lower()),allfonts))
    
        if font == "Bold":
            a = list(filter(lambda x : (("bold" in x.lower()) or ("-b" in x.lower())) and not ("semi" in x.lower() or "black" in x.lower() or "light" in x.lower() or "thin" in x.lower() or "italic" in x.lower()),allfonts))
        
        if font == "SemiBold":
           # print("semiBold",  allfonts)
            a = list(filter(lambda x : (("semibold" in x.lower()) or ("semi bold" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "thin" in x.lower() or "italic" in x.lower()),allfonts))
            #print(a)
            
        if font == "BoldItalic":
            a = list(filter(lambda x : ("-bi" in x.lower()) or ("bold" in x.lower() and "italic" in x.lower()) or ("bolditalic" in x.lower()),allfonts))
    
        if font == "Italic":
            a = list(filter(lambda x : (("italic" in x.lower()) or ("-i" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "bold" in x.lower() or "thin" in x.lower() or "medium" in x.lower()),allfonts))
    
        if font == "MediumItalic":
            a = list(filter(lambda x : ("mediumitalic" in x.lower()) or ("italic" in x.lower() and "medium" in x.lower()),allfonts))
    
        if font == "LightItalic":
            a = list(filter(lambda x : ("italic" in x.lower() and "light" in x.lower()) or ("lightitalic" in x.lower()),allfonts))
    
        if font == "ExtraLightItalic":
            a = list(filter(lambda x : ((("extralight" in x.lower()) or ("extra light" in x.lower()) or "exlight" in x.lower()) and "italic" in x.lower()) and not ("bold" in x.lower() or "thin" in x.lower()),allfonts))
    
    
        if font == "BlackItalic":
            a = list(filter(lambda x : ("black" in x.lower() and "italic" in x.lower()) or ("blackitalic" in x.lower()),allfonts))
    
        if font == "SemiBoldItalic":
            a = list(filter(lambda x : ((("semibold" in x.lower()) or ("semi bold" in x.lower())) and "italic" in x.lower()) and not ("black" in x.lower() or "light" in x.lower() or "thin" in x.lower()),allfonts))
        
        if font == "Thin":
            a = list(filter(lambda x : ((("thin" in x.lower()))) and not ("black" in x.lower() or "light" in x.lower() or "bold" in x.lower() or "italic" in x.lower()),allfonts))
        
        if font == "ThinItalic":
            a = list(filter(lambda x : ((("thin" in x.lower()) and "italic" in x.lower()) or ("thini" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "bold" in x.lower()),allfonts))
        
        if font == "ExtraBold":
            a = list(filter(lambda x : ((("bold" in x.lower()) and "extra" in x.lower()) or ("exbold" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "italic" in x.lower()),allfonts))
        
        if font == "ExtraBoldItalic":
            a = list(filter(lambda x : ((("bold" in x.lower()) and "extra" in x.lower()) and ("italic" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "thin" in x.lower()),allfonts))
    
    if len(a) > 0:
        print(a,name[origlistt.index(a[0])], origlistt.index(a[0]))
        return name[origlistt.index(a[0])]

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
def shortName( font ):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:   
            name_str = record.string.decode('latin-1')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family: 
            family = name_str
        if name and family: break
    return (name,family)


def name_from_dir(x):
    return x.split("/")[-1]

if __name__ == '__main__':
    orig_dir = os.getcwd()
    main()
