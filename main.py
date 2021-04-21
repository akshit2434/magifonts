from telegram import *
from telegram.ext import *
#import telegram
import os
import shutil
import logging
import constants as keys
import responses as r
import random
from fontpreview import *

magifonts_id = -1001393886080
font_ext = ("ttf", "otf")
todof = "file_17.ttf"
file_responses = ["This your OP font by your OP group", "You are the best!!", "You are OP", "Keep it up, i am waiting for more...","Here you go!", "Thanks for being one of us","Check this out!!", "Take this...","I hope you like it!", "Done!!","Compiled...","Finished!"]
FONT, BOLD, ITALICS = range(3)
PREVIEW = 1
bot = Bot(keys.API_KEY)

def member_join(update, context):
    
    for member in update.message.new_chat_members:
        member_count = int(bot.get_chat_members_count(update.message.chat_id))
        if member_count%10 == 0:
            message = update.message.reply_text(f"{member.full_name} is the "+str(member_count)+"th to join the group!!\nWhoo!! "+str(member_count)+" members!")
            if not bot.pin_chat_message(update.message.chat_id, message.message_id):
                update.message.reply_text("I can't even pin a message.. dang!")

def preview_command(update,context):
    clearcache()
    bot.send_message(update.message.chat_id, "Send the font file you would like the preview for...\nSend /cancel to cancel")
    return PREVIEW

def preview(update,context):
    os.chdir(orig_dir)
    if update.message.document.file_name.split(".")[-1].lower():
        bot.send_message(update.message.chat_id, "1 min sar...")
        os.chdir("preview")
        update.message.document.get_file().download(custom_path=update.message.document.file_name)
        pic = previewfont("preview/"+update.message.document.file_name, update.message.document.file_name.split(".")[0])
        os.chdir(orig_dir)
        os.chdir("preview")
        bot.send_photo(update.message.chat_id, open("preview.png", "rb"))
        return ConversationHandler.END
    else:
        bot.send_message(update.message.chat_id, "Send a valid font file to continue")
        return PREVIEW

def cancel_preview(update,context):
    update.message.reply_text("OK. Preview cancelled...")
    return ConversationHandler.END
    

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
            #print(os.getcwd())
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
    bot.send_document(magifonts_id, open(".magiFont/"+remove_ext(todof)+".zip","rb"),caption=random.choice(file_responses))
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
    
    preview_handler = ConversationHandler(
        entry_points = [CommandHandler("preview",preview_command)],
        states = {
            PREVIEW: [MessageHandler(Filters.document, preview)]    
        },
        fallbacks=[CommandHandler("cancel",cancel_preview)]
        
    )

    
    dispatcher.add_handler(ttf_handler)
    dispatcher.add_handler(preview_handler)
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

tfontsr = ["Regular.ttf","Light.ttf","Thin.ttf"]

tfontsb = [ "Medium.ttf","Black.ttf","Bold.ttf"]

tfontsi = ["BlackItalic.ttf","BoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ThinItalic.ttf"]#todof= file...

#os.chdir("C:/Users/rsran/Downloads/akshit ka fonts")
def modulify(zipname):
    print("modulify me hu")
    if not zipname:
        zipname=todof.split(".")[0]
    os.chdir(orig_dir)
    os.chdir("magiTemplate/Fonts")
    
    for i in range(0,len(tfonts)):
        shutil.copyfile(src="../../todo/"+todof , dst=tfonts[i])
    print("copied files")
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir("magiTemplate")
    edit_module_prop(todof.split(".")[0])
    os.chdir(orig_dir)
    shutil.make_archive("magiFont/"+zipname, 'zip', "magiTemplate")
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
    os.chdir("magiTemplate/Fonts")
    for i in range(0,len(tfontsr)):
        shutil.copyfile(src="../../todo/"+fname , dst=tfontsr[i])
    
    for i in range(0,len(tfontsb)):
        shutil.copyfile(src="../../todo/"+fnameb , dst=tfontsb[i])
        
    for i in range(0,len(tfontsi)):
        shutil.copyfile(src="../../todo/"+fnamei , dst=tfontsi[i])
    print(4)
    #print(os.getcwd())
    os.chdir(orig_dir)
    os.chdir("magiTemplate")
    edit_module_prop(remove_ext(fname))
    os.chdir(orig_dir)
    #print(zipname)
    shutil.make_archive("magiFont/"+zipname, 'zip', "magiTemplate/")
    #print(5)
    
def edit_module_prop(fname):
    os.chdir(orig_dir)
    os.chdir("magiTemplate")
    os.rename('module.prop','module.txt')
    prop_list = ["id=MFFM_FontInstaller\n","name="+fname+"\n","version=v1.0\n""versionCode=10\n","author=@TheSc1enceGuy and MFFM\n","description=Magifonts - Install custom fonts with ease.\n"]
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

def ttfdownload(update, context):
    os.chdir(orig_dir)
    clearcache()
    print("ttf download requested by @"+update.message.from_user.username)
    
    if update.message.document.file_name.split(".")[-1].lower() in font_ext:
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
            modulify(remove_ext(update.message.document.file_name))
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
    elif update.message.document.file_name.split(".")[-1].lower() == "zip":
        update.message.reply_text("Zip detected!")
        os.chdir("ziptodo")
        update.message.document.get_file().download(custom_path=update.message.document.file_name)
        print("file downloaded!")
        shutil.unpack_archive(update.message.document.file_name,remove_ext(update.message.document.file_name))
        print("file unzipped")
        if os.path.exists(remove_ext(update.message.document.file_name)+"/system/fonts"):
            if os.path.exists(remove_ext(update.message.document.file_name)+"/module.prop"):
                #update.message.reply_text("The provided zip is already a magisk module LOL!")
                os.chdir("../")
                #print(os.getcwd())
            else:
                update.message.reply_text("Converting to a magisk module sar!!")
                os.chdir(remove_ext(update.message.document.file_name))
                shutil.copyfile(src="../../magiTemplate/module.prop" , dst="module.prop")
                shutil.copyfile(src="../../magiTemplate/META-INF/com/google/android/update-binary" , dst="META-INF/com/google/android/update-binary")
                shutil.copyfile(src="../../magiTemplate/META-INF/com/google/android/updater-script" , dst="META-INF/com/google/android/updater-script")
                shutil.make_archive("../../magiFont/"+remove_ext(update.message.document.file_name), 'zip', os.getcwd())
                os.chdir("../../magiFont")
                bot.send_document(magifonts_id, open(remove_ext(update.message.document.file_name)+".zip",'rb'),caption=random.choice(file_responses))
                bot.send_message(magifonts_id,"Here you go! - @"+update.message.from_user.username)
                if not str(update.message.chat_id) == str(magifonts_id):
                    update.message.reply_text("Your file has been posted in @magifonts_support")
                    update.message.reply_text("Checkout #submit-sample\nThanks for being a part of the awesome community!!")
                os.chdir("../")
        else:
            
            #ttfarray=[]
            os.chdir(orig_dir)
            #print(remove_ext(update.message.document.file_name))
            if not (len(list(filter(lambda x : x.split(".")[-1].lower() in font_ext, listfiles("ziptodo/"+remove_ext(update.message.document.file_name)).copy())))) >= 1:
            #if False:
                bot.send_message(update.message.chat_id, "This zip cannot be made to a font module, pls ensure that all fonts are located in the zip and not in a sub direectory...")
            else:
                fontlist = origflist.copy()
                os.chdir(orig_dir)
                definefonts(fontlist)
                if True:#fontlist[0][1]:                   
                    
                    for i in range(0,len(fontlist)):
                        fontlist[i][1] = find_font(fontlist[i][0],"ziptodo/"+remove_ext(update.message.document.file_name),fontlist,definedfonts,update.message.document.file_name)
                        definefonts(fontlist)
                    for i in range(0,len(fontlist)):
                        fontlist[i][1] = find_font(fontlist[i][0],"ziptodo/"+remove_ext(update.message.document.file_name),fontlist,definedfonts,update.message.document.file_name)
                        definefonts(fontlist)
            
                    print(["Fontlist: ",fontlist])
                    os.chdir(orig_dir)
                    os.chdir("magiFont")
                    zipname = update.message.document.file_name
                    #print("modulifybi...")
                    filedst = modulify2(fontlist,"ziptodo/"+remove_ext(zipname),"magiTemplate/Fonts",definedfonts,"magiFont/[MAGIFONTS]"+zipname)
                    #print (filedst)
                    bot.send_document(magifonts_id, open(filedst,'rb'),caption=random.choice(file_responses))
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
origflist = [["Regular",False],["Light",False],["Thin",False],["Bold",False],["Black",False],["Medium",False],["BoldItalic",False],["MediumItalic",False],["Italic",False],["BlackItalic",False],["LightItalic",False],["ThinItalic",False]]
    
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
    shutil.make_archive(remove_ext(filedst), 'zip', "magiTemplate/")
    return filedst
    
def find_font(font, direc,flist,deffonts,filename=False):
    files = listfiles(direc).copy()

    allfonts = list(filter(lambda x : x.split(".")[-1].lower() in font_ext, files))
    if font == "Regular":
        a = list(filter(lambda x : (x.lower() in filename.lower()) or ("regular" in x.lower()), allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))
    if font == "Black":
        a = list(filter(lambda x : ("blck" in x.lower()) or ("black" in x.lower()) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            approx = nearest_weight(flist,font,deffonts)
            print(["Medium",approx,return_font(flist, approx)])
            return return_font(flist, approx)
    
    if font == "Medium":
        a = list(filter(lambda x : ("-med" in x.lower()) or ("medium" in x.lower()) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            approx = nearest_weight(flist,font,deffonts)
            print(["Medium",approx,return_font(flist, approx)])
            return return_font(flist, approx)
            
    if font == "Light":
        a = list(filter(lambda x : ("-l" in x.lower()) or ("light" in x.lower()) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "Thin":
        a = list(filter(lambda x : ("thin" in x.lower()) or ("-th" in x.lower()) and not ("bold" in x.lower() or "italic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "Bold":
        a = list(filter(lambda x : ("bold" in x.lower()) or ("-b" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "BoldItalic":
        a = list(filter(lambda x : ("-bi" in x.lower()) or ("bold" in x.lower() and "italic" in x.lower()) or ("bolditalic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "Italic":
        a = list(filter(lambda x : ("italic" in x.lower()) or ("-i" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "MediumItalic":
        a = list(filter(lambda x : ("mediumitalic" in x.lower()) or ("italic" in x.lower() and "medium" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "LightItalic":
        a = list(filter(lambda x : ("italic" in x.lower() and "light" in x.lower()) or ("lightitalic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "BlackItalic":
        a = list(filter(lambda x : ("black" in x.lower() and "italic" in x.lower()) or ("blackitalic" in x.lower()),allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))

    if font == "ThinItalic":
        a = list(filter(lambda x : ("thin" in x.lower() and "italic" in x.lower()) , allfonts))
        if len(a) > 0:
            return a[0]
        else:
            return return_font(flist, nearest_weight(flist,font,deffonts))
    
         
    
    
def nearest_weight(flist, x, deffonts):
    if x in deffonts:
        return return_font(flist, x)
    else:
        allf_list = [tfontsr.copy(),tfontsb.copy(),tfontsi.copy()]
        for array in allf_list:
            print("array: "+x)
            print(array)
            if x+".ttf" in array:
                print("\n")
                l = (len(array)-array.index(x+".ttf"))-1
                i = (len(array)-l)-1
                for j in range(1,max(l,i)+1):
                    print([l,i,j])
                    
                    if l>=j:
                        print([x,"milega?: ",remove_ext(array[array.index(x+".ttf")+j])])
                        if  remove_ext(array[array.index(x+".ttf")+j]) in deffonts:
                            print("millla j")
                            return remove_ext(array[array.index(x+".ttf")+j])
                            break
                    if i>=j:
                        print([x,"milega???: ",remove_ext(array[array.index(x+".ttf")-j]), deffonts])
                        if remove_ext(array[array.index(x+".ttf")-j]) in deffonts:
                            print("mila.. i")
                            return remove_ext(array[array.index(x+".ttf")-j])
                            break
        
        #return return_font(flist, "Regular")
        if "Regular" in definedfonts:
            print("\nkuch nhi mila\n\n")
            return False
        return "first_element"
definedfonts=[]
def definefonts(flist):
    global definedfonts
    definedfonts=[]
    for i in flist:
        if not i[1]==False:
            if not i[0] in definedfonts:
                definedfonts.append(i[0])

def return_font(array, value):
    if value=="first_element":
        for i in array:
            if not i[1] == False:
                return i[1]
    for i in array:
        if i[0] == value:
            return i[1]

def previewfont(fdir,fname):
    bg_color = (29,53,87)
    fg_color = (241,250,238)
    os.chdir(orig_dir)
    
    fb = FontBanner(fdir, 'landscape')
    fb2 = FontBanner(fdir, 'landscape')
    fb3 = FontBanner(fdir, 'landscape')
    fb4 = FontBanner(fdir, 'landscape')
    fw = FontWall([fb,fb2,fb3,fb4])
    fb.font_text = 'Checkout @Magifont_Support for instant\nawesome fonts and previews!!'
    fb.bg_color = bg_color
    fb.fg_color = fg_color
    fb.set_font_size(100)
    fb.set_text_position('center')
    # Modify properties of second banner
    fb2.font_text = 'This preview is made by @Magifont_bot\nDeveloped by@TheSc1enceGuy (Akshit Singh)...\nCheck it out!'
    fb2.bg_color = bg_color
    fb2.fg_color = fg_color
    fb2.set_font_size(100)
    fb2.set_text_position('center')
    # Modify properties of third banner
    fb3.font_text = 'This group uses MFFM font templates!!\nbtw the digits of pi are\n3.1415926535 8979323846 2643383... '
    fb3.bg_color = bg_color
    fb3.fg_color = fg_color
    fb3.set_font_size(100) 
    fb3.set_text_position('center')                 # the font is resized automatically because it exceeds the size of the banner
    # Modify properties of last banner
    fb4.font_text = 'By the way, th1s is just a sample for fonts.\nHow is this '+fname+'? Do you like it?'
    fb4.bg_color = bg_color
    fb4.fg_color = fg_color
    fb4.set_font_size(100)
    fb4.set_text_position('center')
    fw.draw(2)             
    os.chdir("preview")
    fw.save('preview.png')
    return "preview.png"
    
def clearcache():
    os.chdir(orig_dir)
    wipefiles("todo")
    wipefiles("magiFont")
    wipefiles("ziptodo")
    wipefiles("magiTemplate/Fonts")
    wipefiles("preview")
            
            
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
    create_dir("todo")
    create_dir("magiFont")
    create_dir("ziptodo")
    create_dir("preview")
    clearcache()
    
def create_dir(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        return True
    

if __name__ == '__main__':
    orig_dir = os.getcwd()
    main()
