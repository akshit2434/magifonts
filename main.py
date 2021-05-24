from telegram import *
from telegram.ext import *
import fnmatch
import os
import shutil
import logging
import constants as keys
import responses as r
import random
from fontpreview import *
from pyunpack import Archive
from py7zr import unpack_7zarchive
from fontTools import ttLib

magifonts_id = keys.gid
font_ext = ("ttf", "otf")
zip_ext= ("zip","7z","rar")
todof = "file_17.ttf"
file_responses = ["This your OP font by your OP group", "You are the best!!", "You are OP", "Keep it up, i am waiting for more...","Here you go!", "Thanks for being one of us","Check this out!!", "Take this...","I hope you like it!", "Done!!","Compiled...","Finished!"]
FONT, BOLD, ITALICS = range(3)
PREVIEW = 1
bot = Bot(keys.API_KEY)

def member_join(update, context):
    
    for member in update.message.new_chat_members:
        member_count = int(bot.get_chat_members_count(update.message.chat_id))
        if member_count%100 == 0:
            message = update.message.reply_text(f"{member.full_name} is the "+str(member_count)+"th to join the group!!\nWhoo!! "+str(member_count)+" members!")
            if not bot.pin_chat_message(update.message.chat_id, message.message_id):
                update.message.reply_text("I can't even pin a message.. dang!")

def preview_command(update,context):
    clearcache()
    if update.message.reply_to_message:
        msg = bot.send_message(update.message.chat_id, "Gimme a minute")
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
        pic = previewfont(doc.document.file_name.split(".")[0], remove_ext(doc.document.file_name)+".ttf")
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
            #print(ffiles)
            #for i in range(0,len(ffiles)):
        regular_font = find_font(ffiles,"Regular", remove_ext(doc.document.file_name))
        bold_font = find_font(ffiles,"Bold")
        light_font = find_font(ffiles,"Light")
        italic_font = find_font(ffiles,"Italic")
        print(regular_font)
        if regular_font:
            #regular_font = ffiles[i]
            os.chdir(orig_dir)
            pic = previewfont(doc.document.file_name.split(".")[0], regular_font, bold_font, light_font, italic_font)
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
    update.message.reply_text("Search for it on Google, duh. Tag my master @TheSc1enceGuy for some very important questions...")
    
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
    if update.message.text:
        text = str(update.message.text).lower()
        if r.sample_responses(text) not in (""):
            update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    print(f"Update {update} caused error {context.error}")
    error = str(context.error).lower()
    #print(error, error == "broken file")
    if error == "timed out":
        update.message.reply_text("Request Timed Out. Pls try again...")
    if error == "broken file":
        update.message.reply_text("File is broken LoL xD.\nSorry, I feel sad for you...")
def module(update,context):
    if "-" in str(update.message.chat_id):
        update.message.reply_text("Try running this command in my pm...")
    else:
        print("module requested by @"+update.message.from_user.username)
        bot.send_message(update.message.chat_id,"This is the procedure to create multiweight fonts. Send the regular font to continue...\nSend /cancel anytime to skip")
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
            bot.send_message(update.message.chat_id, "Do you have the bold version, send to continue?\nSend /skip to skip this step...")
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
            bot.send_message(update.message.chat_id, "Do you have the italics version, send to continue?\nSend /skip to skip this step ...")
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

            temp_msg = bot.send_message(update.message.chat_id, "Ok... Processing...")
        
            modulifybi(todof,)
            os.chdir(orig_dir)
            print("magiFont/"+todof.split(".")[0]+".zip")
            bot.send_document(magifonts_id, open("magiFont/"+remove_ext(todof)+".zip","rb"),caption=random.choice(file_responses))
            bot.send_message(update.message.chat_id,"Check Magifonts group (@magifonts_support). Your font has been posted")
            context.bot.send_message(magifonts_id, "Here @"+update.message.from_user.username)
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
    temp_msg = bot.send_message(update.message.chat_id, "OK sar, Processing, give me a minute...")
    modulifybi(todof)
    os.chdir(orig_dir)
    bot.send_document(magifonts_id, open("magiFont/"+remove_ext(todof)+".zip","rb"),caption=random.choice(file_responses))
    context.bot.send_message(magifonts_id, "Here @"+update.message.from_user.username)
    bot.send_message(update.message.chat_id,"Check Magifonts group (@magifonts_support). Your font has been posted")
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
        entry_points=[CommandHandler('mwmodule', module)],
        states={
            FONT: [MessageHandler(Filters.document, font)],
            BOLD: [MessageHandler(Filters.document, bold), CommandHandler('skip', skip_bold)],
            ITALICS: [MessageHandler(Filters.document, italics), CommandHandler('skip', skip_italics)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    #preview_handler = ConversationHandler(
    #    entry_points = [CommandHandler("preview",preview_command)],
    #    states = {
    #        PREVIEW: [MessageHandler(Filters.document, preview)]    
    #    },
    #    fallbacks=[CommandHandler("cancel",cancel_preview)]
    #)

    
    dispatcher.add_handler(ttf_handler)
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
    #dispatcher.add_handler(CommandHandler("rename",rename_command))
    dispatcher.add_handler(CommandHandler("faketrigger",member_join))
    
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    
    #dispatcher.add_handler(MessageHandler(Filters.document, ttfdownload))

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
                    print(attr)
                else:
                    to_del = capscheck(attr)
                    font = find_font(ffiles, to_del, remove_ext(doc.file_name))
                    print("font: ",font, "   to_del: ",to_del)
                    if font:
                        os.remove(font)
                        print(font)
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
        msg = update.message.reply_text("Processing...")
        #print("filename: ",context.args)
        msgarray = []
        if "/module " in update.message.text:
            msgarray = list(map(lambda x: x.replace('"', ""), update.message.text.replace("/module ", "").split(" ")))
        filename=None
        #print("filename: ",msgarray)
        if len(msgarray) >= 1:
            filename = msgarray[0]
        ttfdownload(update,context,update.message.reply_to_message,filename)
        bot.delete_message(update.message.chat_id,msg.message_id)
    else:
        update.message.reply_text("Reply to a font file/zip bro.")
tfonts = ["MFFM.ttf"]

tfontsr = ["Regular.ttf","Light.ttf","Thin.ttf"]

tfontsb = [ "Medium.ttf","Black.ttf","Bold.ttf"]

tfontsi = ["BlackItalic.ttf","BoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ThinItalic.ttf"]#todof= file...

tfontsall = ["Regular.ttf","Light.ttf","Thin.ttf","Medium.ttf","Black.ttf","Bold.ttf","BlackItalic.ttf","BoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ThinItalic.ttf"]

#os.chdir("C:/Users/rsran/Downloads/akshit ka fonts")
def modulify(zipname):
    print("modulify me hu")
    if not zipname:
        zipname=remove_ext(todof)
    os.chdir(orig_dir)
    os.chdir(keys.font_dir)
    
    for i in range(0,len(tfonts)):
        shutil.copyfile(src="../../todo/"+todof , dst=tfonts[i])
    print("copied files")
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir(keys.template_dir)
    edit_module_prop(remove_ext(todof))
    os.chdir(orig_dir)
    shutil.make_archive("magiFont/"+zipname, 'zip', keys.template_dir)
    print("archive ready")
    
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
    #print(5)
    
def edit_module_prop(fname):
    os.chdir(orig_dir)
    os.chdir(keys.template_dir)
    os.rename('module.prop','module.txt')
    prop_list = ["id=id=omf_font_module\n","name="+fname+"\n","Moduleversion=v2021.05.23\n""versionCode=2021052301\n","author=nongthaihoang @GitLab; MFFM; @TheSc1enceGuy\n","description=OMF Advanced font installer for Android. Module prepared by @magifont_bot. Join @MFFMDisc / @Magifonts_Support for more.\n"]
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
def ttfdownload(update, context,doc, zipname):
    #flist = origlist.copy()
    if not zipname:
        zipname = remove_ext(doc.document.file_name)
    print(doc)
    if not doc:
        doc = update.message
    os.chdir(orig_dir)
    clearcache()
    print("ttf download requested by @"+update.message.from_user.username)
    
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
            modulify(remove_ext(doc.document.file_name))
            os.chdir(orig_dir)
            os.chdir("magiFont")
            print("sending...")
            bot.send_document(magifonts_id, open(remove_ext(todof)+".zip",'rb'),caption=random.choice(file_responses))
            bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
            if not str(update.message.chat_id) == str(magifonts_id):
                update.message.reply_text("Your file has been posted in @magifonts_support")
                update.message.reply_text("Checkout #submit-sample\nThanks for being a part of the awesome community!!")
            os.chdir("../")
        else:
            update.message.reply_text("invalid file type!")
            os.chdir("../")
    elif doc.document.file_name.split(".")[-1].lower() in zip_ext:
        os.chdir("ziptodo")
        doc.document.get_file().download(custom_path=doc.document.file_name)
        print("file downloaded!")
        extract(doc.document.file_name, remove_ext(doc.document.file_name))
        print("file unzipped: ",remove_ext(doc.document.file_name))
        ffiles = find("*.ttf",remove_ext(doc.document.file_name))
        print(0)
        origflist = [["Regular",False],["Light",False],["Thin",False],["Bold",False],["Black",False],["Medium",False],["BoldItalic",False],["MediumItalic",False],["Italic",False],["BlackItalic",False],["LightItalic",False],["ThinItalic",False]]
        flist = origflist.copy()
        if not ffiles:
            print("otf")
            ffiles = find("*.otf",remove_ext(doc.document.file_name))
        
        if not ffiles:
            update.message.reply_text("This zip has no .ttf or .otf file... :(")
            return
        
        print("files: ",ffiles[0])
        if len(ffiles) == 1:
            shutil.copyfile(ffiles[0], os.path.join("..\\",keys.fonts_dir,"MFFM.ttf"))
        else:
            for i in range(len(ffiles)):
                for j in range(len(tfontsall)):
                    x = find_font(ffiles, remove_ext(tfontsall[j]),remove_ext(doc.document.file_name))
                    if x:
                        #print(x,flist)
                        if [remove_ext(tfontsall[j]),False] in flist:
                            flist[flist.index([remove_ext(tfontsall[j]),False])][1] = x
            print(1)
            for i in range(len(ffiles)):
                for j in range(len(tfontsall)):
                    deffonts = definefonts(flist)
                    if not remove_ext(tfontsall[j]) in deffonts:
                        
                        nearest = nearest_weight2(flist,remove_ext(tfontsall[j]), deffonts)
                        if nearest:
                            x = find_font(ffiles, nearest,remove_ext(doc.document.file_name))
                            if x:
                                flist[flist.index([remove_ext(tfontsall[j]),False])][1] = x
                            else:
                                x = find_font(ffiles, "Regular",remove_ext(doc.document.file_name))
                                if x:
                                    flist[flist.index([remove_ext(tfontsall[j]),False])][1] = x
                        
            print(2)
            paste_to_template(flist,"ziptodo",keys.fonts_dir)
        edit_module_prop(zipname)
        print(3)
        os.chdir(orig_dir)
        print("magiFont/"+remove_ext(doc.document.file_name)+".zip")
        shutil.make_archive("magiFont/"+zipname+"[Magifonts]", "zip",keys.template_dir)
        bot.send_document(magifonts_id, open("magiFont/"+zipname+"[Magifonts]"+".zip",'rb'),caption=random.choice(file_responses))
        bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
        if not (update.message.chat_id == magifonts_id):
            bot.send_message(update.message.chat_id,"The file has been posted to @magifonts_support")
        os.chdir("../")
    else:                
        os.chdir("../")
        update.message.reply_text("Sar, sorry but I can't make this to a module. Pls gib font(ttf or otf) file/zip :(")
    
        #os.chdir("../magiTemplate/system/fonts")
        #for i in range(0,len(tfontsr)):
        #    shutil.copyfile(src="../../../todo/"+fname , dst=tfontsr[i])
origflist = [["Regular",False],["Light",False],["Thin",False],["Bold",False],["Black",False],["Medium",False],["BoldItalic",False],["MediumItalic",False],["Italic",False],["BlackItalic",False],["LightItalic",False],["ThinItalic",False]]

def paste_to_template(flist,src,dst):
    os.chdir(orig_dir)
    print(src+"/"+flist[0][1])
    for i in range(len(flist)):
        if flist[i][1]:
            if os.path.exists(src+"/"+flist[i][1]):
                shutil.copyfile(src+"/"+flist[i][1], dst+"/"+flist[i][0]+".ttf")

def modulify2(flist,src,dst,definedfonts,filedst):
    os.chdir(orig_dir)

    if "Regular" in definedfonts:
        if len(definedfonts) == 1:
            shutil.copyfile(src+"/"+flist[2][1], dst+"/MFFM.ttf")
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
                            #print("x: ",x," / ",remove_ext(array[array.index(x+".ttf")+j]))
                            return remove_ext(array[array.index(x+".ttf")+j])
                            break
                    if i>=j:
                        if remove_ext(array[array.index(x+".ttf")-j]) in deffonts:
                            print("x: ",x," / ",remove_ext(array[array.index(x+".ttf")-j]))
                            return remove_ext(array[array.index(x+".ttf")-j])
                            break
        
        #return return_font(flist, "Regular")
    print("sed loif: ",x," / ",definedfonts)
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
    print([fname,fname2,fname3,fname4])
    print(name_from_dir(fname))
    bg_color = (0, 43, 54)
    fg_color = (0,160,153)
    fg_color2 = (159,255,163)
    os.chdir(orig_dir)
    os.chdir("preview")
    print(0.1)
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
    
def clearcache():
    origflist = [["Regular",False],["Light",False],["Thin",False],["Bold",False],["Black",False],["Medium",False],["BoldItalic",False],["MediumItalic",False],["Italic",False],["BlackItalic",False],["LightItalic",False],["ThinItalic",False]]
    os.chdir(orig_dir)
    wipefiles("todo")
    wipefiles("magiFont")
    wipefiles("ziptodo")
    wipefiles(keys.fonts_dir)
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
    
def initialize():
    try:
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    except:
        print("7z already registered")
    #else:
        #shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    create_dir("todo")
    create_dir("magiFont")
    create_dir("ziptodo")
    create_dir("ffiles")
    create_dir("preview/preview_zip")
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
                #print("\n\nfind...")
                
                #result = os.path.join(str(result),os.path.join(root,name))
                result.append(os.path.join(root.replace("//","/"), name.replace("//","/")).replace("//","/"))
                #print(result)
    return list(map(lambda x : str(x).replace("\\","/"),result))

def regularfinder(x,filename):
    if(("regular" in x.lower() or "mffm" in x.lower())):
        return True
    if not ("italic" in x.lower() or "black" in x.lower() or "bold" in x.lower() or "medium" in x.lower() or  "thin" in x.lower() or "light" in x.lower() or "condensed" in x.lower()):
        return True
    return False

def find_font(name, font, filename = ""):
    #print("finding ",font," in ",name)
    #filename="hulu`124827@@#"
    #print("\nallfonts")
    allfonts = []
    if os.path.exists(list(name)[0]):
        #print("files detected ")
        for i in range(0,len(name)):
            #print("in fur luup")
            #print(name[i]," mm ")#, shortName(name[i]))
            allfonts.append(shortName(ttLib.TTFont(name[i])))
    else:
        allfonts = list(name).copy()
    a = []
    
    #print(allfonts)
    if len(allfonts)== 1:
            return name[0]
    if font == "Regular":
        a = list(filter(lambda x : regularfinder(x,filename), allfonts))
        #print("Regular: ",a," , allfonts: ", allfonts)
        if not len(a) > 0:
            return name[0]
        
        
    if font == "Black":
        a = list(filter(lambda x : (("blck" in x.lower()) or ("black" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))

    if font == "Medium":
        a = list(filter(lambda x : (("-med" in x.lower()) or ("medium" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))

    if font == "Light":
        a = list(filter(lambda x : (("-l" in x.lower()) or ("light" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))

    if font == "Thin":
        a = list(filter(lambda x : (("thin" in x.lower()) or ("-th" in x.lower())) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))

    if font == "Bold":
        a = list(filter(lambda x : (("bold" in x.lower()) or ("-b" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "thin" in x.lower() or "italic" in x.lower()),allfonts))

    if font == "BoldItalic":
        a = list(filter(lambda x : ("-bi" in x.lower()) or ("bold" in x.lower() and "italic" in x.lower()) or ("bolditalic" in x.lower()),allfonts))

    if font == "Italic":
        a = list(filter(lambda x : (("italic" in x.lower()) or ("-i" in x.lower())) and not ("black" in x.lower() or "light" in x.lower() or "bold" in x.lower() or "thin" in x.lower() or "medium" in x.lower()),allfonts))

    if font == "MediumItalic":
        a = list(filter(lambda x : ("mediumitalic" in x.lower()) or ("italic" in x.lower() and "medium" in x.lower()),allfonts))

    if font == "LightItalic":
        a = list(filter(lambda x : ("italic" in x.lower() and "light" in x.lower()) or ("lightitalic" in x.lower()),allfonts))

    if font == "BlackItalic":
        a = list(filter(lambda x : ("black" in x.lower() and "italic" in x.lower()) or ("blackitalic" in x.lower()),allfonts))

    if font == "ThinItalic":
        a = list(filter(lambda x : ("thin" in x.lower() and "italic" in x.lower()) , allfonts))
    
    if len(a) > 0:
        return name[allfonts.index(a[0])]
        

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
    return name


def name_from_dir(x):
    return x.split("/")[-1]

if __name__ == '__main__':
    orig_dir = os.getcwd()
    main()
