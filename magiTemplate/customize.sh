##MFFM Custom Font Installer Magisk Script##
##Don't alter codes after this##
##If you use it for your own module don't change the credits, unless you are a theif##

OD="$(magisk --path)/.magisk/mirror/system"
FONTS_XML="$(magisk --path)/.magisk/mirror/system/etc/fonts.xml"
FONTS_OOS_XML="$(magisk --path)/.magisk/mirror/system/etc/fonts_base.xml"
FXML=$MODPATH/system/etc/fonts.xml
SF=$MODPATH/system/fonts/
FD=$MODPATH/Fonts
PDF=$MODPATH/system/product/fonts

ui_print "  "
ui_print "************************************"
ui_print "*|- ||Custom Font Installer||      *"
ui_print "*|- ||By 'MFFM'||                  *"
ui_print "************************************"
ui_print "  "

if [ -f $FONTS_XML ]; then
    mkdir -p $MODPATH/system/fonts && mkdir -p $MODPATH/system/etc/ 
    cp -af $FONTS_XML $MODPATH/system/etc/fonts.xml
else
    abort "fonts.xml not found! Canceling installation."
fi

##Patch based on @nongthaihoang's work##
sed -i '/"sans-serif">/,/family>/H;1,/family>/{/family>/G}'	$FXML
sed -i ':a;N;$!ba; s/name=\"sans-serif\"//2' $FXML
sed -i '/\"sans-serif\">/,/family>/{s/Roboto-/MFFM-/}' $FXML

if [ -f $OD/fonts/Roboto-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic
	for i do cp $FD/$i.ttf $SF/MFFM-$i.ttf; done	
	cp $FD/Mono.ttf $SF/DroidSansMono.ttf;
	cp $FD/Bold.ttf $SF/AndroidClock.ttf;
fi

if [ -f $OD/fonts/RobotoCondensed-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic
	for i do cp $FD/$i.ttf $SF/RobotoCondensed-$i.ttf; done
fi

if [ -f $OD/fonts/RobotoCondensed-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic
	for i do cp $FD/Condensed-$i.ttf $SF/RobotoCondensed-$i.ttf; done
fi

if [ -f $OD/fonts/Roboto-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic
	for i do cp $FD/MFFM.ttf $SF/MFFM-$i.ttf; done
	cp $FD/MFFM.ttf $SF/AndroidClock.ttf;
	set Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic
	for i do cp $FD/MFFM.ttf $SF/RobotoCondensed-$i.ttf; done
fi

if [ -f $OD/fonts/NotoSerif-Regular.ttf ]; then
    set Bold BoldItalic Regular Italic
	for i do cp $FD/$i.ttf $SF/NotoSerif-$i.ttf; done
	set Bold BoldItalic Regular Italic
	for i do cp $FD/MFFM.ttf $SF/NotoSerif-$i.ttf; done	
fi

if [ -f $OD/fonts/SourceSansPro-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/$i.ttf $SF/SourceSansPro-$i.ttf;
	cp $FD/Medium.ttf $SF/SourceSansPro-Semibold.ttf;
	cp $FD/MediumItalic.ttf $SF/SourceSansPro-SemiboldItalic.ttf; done
	set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/MFFM.ttf $SF/SourceSansPro-$i.ttf;
	cp $FD/MFFM.ttf $SF/SourceSansPro-Semibold.ttf;
	cp $FD/MFFM.ttf $SF/SourceSansPro-SemiboldItalic.ttf; done	
fi

if [ -f $OD/product/fonts/GoogleSans-Regular.ttf ]; then
    mkdir -p $MODPATH/system/product/fonts   
    set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/$i.ttf $MODPATH/system/product/fonts/GoogleSans-$i.ttf; done
	set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/MFFM.ttf $MODPATH/system/product/fonts/GoogleSans-$i.ttf; done	
fi

if [ -f $OD/fonts/GoogleSans-Regular.ttf ]; then
    set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/$i.ttf $SF/GoogleSans-$i.ttf; done
	set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/MFFM.ttf $SF/GoogleSans-$i.ttf; done	
fi

if [ -f $OD/product/fonts/Arvo-Regular.ttf ]; then
    mkdir -p $MODPATH/system/product/fonts   
    set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/$i.ttf $MODPATH/system/product/fonts/Arvo-$i.ttf; done
	set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/MFFM.ttf $MODPATH/system/product/fonts/Arvo-$i.ttf; done	
fi

if [ -f $OD/product/fonts/Lato-Regular.ttf ]; then
    mkdir -p $MODPATH/system/product/fonts   
    set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/$i.ttf $MODPATH/system/product/fonts/Lato-$i.ttf; done
	set Bold BoldItalic Medium MediumItalic Regular Italic
	for i do cp $FD/MFFM.ttf $MODPATH/system/product/fonts/Lato-$i.ttf; done	
fi

##Patch based on @nongthaihoang's work##
if [ -f $OD/fonts/MiLanProVF.ttf ]; then
    sed -i '/"mipro"/,/family>/{/400/s/MiLanProVF/MFFM-Regular/;/stylevalue="340"/d}' $FXML
	sed -i '/"mipro"/,/family>/{/700/s/MiLanProVF/MFFM-Bold/;/stylevalue="400"/d}' $FXML
	sed -i '/"mipro-thin"/,/family>/{/400/s/MiLanProVF/MFFM-Thin/;/700/s/MiLanProVF/MFFM-Light/;/stylevalue/d}' $FXML
	sed -i '/"mipro-extralight"/,/family>/{/400/s/MiLanProVF/MFFM-Thin/;/700/s/MiLanProVF/MFFM-Light/;/stylevalue/d}' $FXML
	sed -i '/"mipro-light"/,/family>/{/400/s/MiLanProVF/MFFM-Light/;/700/s/MiLanProVF/MFFM-Regular/;/stylevalue/d}' $FXML
	sed -i '/"mipro-normal"/,/family>/{/400/s/MiLanProVF/MFFM-Light/;/700/s/MiLanProVF/MFFM-Regular/;/stylevalue/d}' $FXML
	sed -i '/"mipro-regular"/,/family>/{/400/s/MiLanProVF/MFFM-Regular/;/stylevalue="340"/d}' $FXML
	sed -i '/"mipro-regular"/,/family>/{/700/s/MiLanProVF/MFFM-Medium/;/stylevalue="400"/d}' $FXML
	sed -i '/"mipro-medium"/,/family>/{/400/s/MiLanProVF/MFFM-Medium/;/700/s/MiLanProVF/MFFM-Bold/;/stylevalue/d}' $FXML
	sed -i '/"mipro-demibold"/,/family>/{/400/s/MiLanProVF/MFFM-Medium/;/700/s/MiLanProVF/MFFM-Bold/;/stylevalue/d}' $FXML
	sed -i '/"mipro-semibold"/,/family>/{/400/s/MiLanProVF/MFFM-Medium/;/700/s/MiLanProVF/MFFM-Bold/;/stylevalue/d}' $FXML
	sed -i '/"mipro-bold"/,/family>/{/400/s/MiLanProVF/MFFM-Bold/;/700/s/MiLanProVF/MFFM-Black/;/stylevalue/d}' $FXML
	sed -i '/"mipro-heavy"/,/family>/{/400/s/MiLanProVF/MFFM-Black/;/stylevalue/d}' $FXML
	cp $FD/Regular.ttf $SF/MiLanProVF.ttf
	cp $FD/Regular.ttf $SF/MitypeClock.otf
	cp $FD/Regular.ttf $SF/MiClock.otf
	cp $FD/Regular.ttf $SF/MiClockThin.otf
	cp $FD/Regular.ttf $SF/MitypeClockMono.otf
	cp $FD/Regular.ttf $SF/MitypeMonoVF.ttf
	cp $FD/Bold.ttf $SF/Miui-Bold.ttf
	cp $FD/Bold.ttf $SF/MiuiEx-Bold.ttf
	cp $FD/Regular.ttf $SF/MiuiEx-Regular.ttf
	cp $FD/Light.ttf $SF/MiuiEx-Light.ttf
	cp $FD/Light.ttf $SF/Miui-Light.ttf
	cp $FD/Regular.ttf $SF/Miui-Regular.ttf
	cp $FD/Thin.ttf $SF/Miui-Thin.ttf	
	cp $FD/MFFM.ttf $SF/MiLanProVF.ttf
	cp $FD/MFFM.ttf $SF/MitypeClock.otf
	cp $FD/MFFM.ttf $SF/MiClock.otf
	cp $FD/MFFM.ttf $SF/MiClockThin.otf
	cp $FD/MFFM.ttf $SF/MitypeClockMono.otf
	cp $FD/MFFM.ttf $SF/MitypeMonoVF.ttf
	cp $FD/MFFM.ttf $SF/Miui-Bold.ttf
	cp $FD/MFFM.ttf $SF/MiuiEx-Bold.ttf
	cp $FD/MFFM.ttf $SF/MiuiEx-Regular.ttf
	cp $FD/MFFM.ttf $SF/MiuiEx-Light.ttf
	cp $FD/MFFM.ttf $SF/Miui-Light.ttf
	cp $FD/MFFM.ttf $SF/Miui-Regular.ttf
	cp $FD/MFFM.ttf $SF/Miui-Thin.ttf	
fi	

##Patch based on @nongthaihoang's work##
if [ -f $OD/fonts/SlateForOnePlus-Regular.ttf ]; then
	set Black Bold Medium Regular Light Thin
	for i do cp $FD/$i.ttf $SF/SlateForOnePlus-$i.ttf; done
	cp $FD/Regular.ttf $SF/SlateForOnePlus-Book.ttf	
	set Black Bold Medium Regular Light Thin
	for i do cp $FD/MFFM.ttf $SF/SlateForOnePlus-$i.ttf; done
	cp $FD/MFFM.ttf $SF/SlateForOnePlus-Book.ttf	
	elif [ -f $OD/fonts/OpFont-Regular.ttf ]; then
	cp -af $FONTS_OOS_XML $MODPATH/system/etc/fonts_base.xml
	sed -i '/"sans-serif">/,/family>/H;1,/family>/{/family>/G}'	$MODPATH/system/etc/fonts_base.xml
    sed -i ':a;N;$!ba; s/name=\"sans-serif\"//2' $MODPATH/system/etc/fonts_base.xml
    sed -i '/\"sans-serif\">/,/family>/{s/Roboto-/MFFM-/}' $MODPATH/system/etc/fonts_base.xml	
	cp $MODPATH/system/etc/fonts_base.xml $FXML	
	set Black BlackItalic Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic Thin ThinItalic
	for i do cp $FD/$i.ttf $SF/OpFont-$i.ttf; done
	set Black BlackItalic Bold BoldItalic Medium MediumItalic Regular Italic Light LightItalic Thin ThinItalic
	for i do cp $FD/MFFM.ttf $SF/OpFont-$i.ttf; done
fi

set_perm_recursive $MODPATH 0 0 0755 0644
sleep 0.5
ui_print "   "
ui_print "|- Cleaning your sins away..."
rm -rf $FD

ui_print "|- Installation Completed! Reboot to see changes!"
ui_print "|- Installation script is based on Nông Thái Hoàng's codes."
ui_print "|- Join on telegram https://t.me/MFFMDisc for support"
ui_print " "
ui_print "********************************"
ui_print "* ___  __________________  ___ *"
ui_print "* |  \/  ||  ___|  ___|  \/  | *"
ui_print "* | .  . || |_  | |_  | .  . | *"
ui_print "* | |\/| ||  _| |  _| | |\/| | *"
ui_print "* | |  | || |   | |   | |  | | *"
ui_print "* \_|  |_/\_|   \_|   \_|  |_/ *"
ui_print "********************************"