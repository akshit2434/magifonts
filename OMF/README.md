# Oh My Font Template
### v2021.05.23
- A powerful font module template for [Magisk](https://github.com/topjohnwu/Magisk). Powered by [OMF](https://gitlab.com/nongthaihoang/oh_my_font).
- The template includes many useful variables and functions. It is designed intended mostly for font module makers and developers.
- The template alone does nothing. You have to write your own code to make it works.
- You can clone the template or just get the [`customize.sh`](https://gitlab.com/nongthaihoang/omf-template/-/blob/master/customize.sh).

## Variables
- ORIGINAL Paths:
    - `ORIPRDFONT`	: /product/fonts
    - `ORIPRDETC`	: /product/etc
    - `ORIPRDXML`	: /product/etc/fonts_customization.xml
    - `ORISYSFONT`	: /system/fonts
    - `ORISYSETC`	: /system/etc
    - `ORISYSXML`	: /system/etc/fonts.xml
___
- MODULE Paths:
    - `PRDFONT`		: system/product/fonts
    - `PRDETC`		: system/product/etc
    - `PRDXML`		: system/product/etc/fonts_customization.xml
    - `SYSFONT`		: system/fonts
    - `SYSETC`		: system/etc
    - `SYSXML`		: system/etc/fonts.xml
    - `MODPROP`		: module.prop
    - `FONTS`		: the `fonts` folder where all your fonts should be.
___
- FONT families:
  - `SA`    : sans-serif
  - `SC`    : sans-serif-condensed
  - `MO`    : monospace
  - `SE`    : serif
  - `SO`    : serif-monospace

## Functions
- **`ver`** (version)
    - Append text to the version string which shows in Magisk app.  
    - Usage: `ver <text>`
- **`xml`**
    - Shortcut for the `sed` command to edit fontxml `$XML` (default is `$SYSXML`).  
    - Usage: `xml <sed expresions>`
- **`cpf`** (cp font)
    - copy (don't overwrite) font from `$FONTS` to `$CPF` (default is `$SYSFONT`).
    - Usage: `cpf <font1> [font2] [font3] ...`
    - E.g. `cpf firstfont.ttf secondfont.ttf thirdfont.otf`
- **`fallback`**
    - Make a font family fallback.  
    - Usage: `fallback [font family]`  
        If no argument was provided, the font family is sans-serif by default.  
    - E.g.  
        `fallback`  
        `fallback serif`  
        It recommends to call the `$FB` variable which is a shortcut for the function. `$FB` will be empty if the fontxml is already pre-patched (i.e. Oxygen 11).
- **`prep`** (prepare)
    - Copy the original fontxml to module path and check if it is patched. This is usually the first function you want to call.  
- **`font`**
    - The most powerfull function to manipulate `<font>` tag inside fontxml.  
    - Usage: `font <font family> <font name> <font style> [axis1 value1] [axis2 value2] ...`
    - `font family`: sans-serif, serif, monospace, etc  
    - `font name`: Regular.ttf, Medium.ttf, MyFontName.ttf  
    - `font style`: from weight 100 to 900 (Thin to Black):
      - Uprights: `t, el, l, r, m, sb, b, eb, bl`  
      - Italics: `ti, eli, li, ri, mi, sbi, bi, ebi, bli`  
    - `axis`: wdth, wght, slnt, opsz, etc.
    - `value`: value of each `axis`
    - E.g.  
        `font sans-serif MyFont-Regular.ttf r`  
        `font sans-serif MyFont-Bold.ttf b`  
        `font sans-serif AnyFont-VF.ttf bl wght 900 width 100`  
- **`mksty`** (make style)
    - Edit fontxml to add more font styles for a family. Only usefull if you font has more weights than default.  
    - Usage: `mksty [font family] <max weight> [min weight]`  
        without arguments, `font family` is sans-serif and `max weigt` is 9 by default.
    - E.g.  
        `mksty`  
        will make 9 weights for sans-serif - both uprights and italics (18 styles). Use this if your font has full weights.  
        `mksty sans-serif-condensed 9`  
        does the same thing but for sans-serif-condensed family
- **`finish`**
    - Remove all unnecessary files except `system` folder and `module.prop` file, correct permissions. Run it as the last function.  
- **`config`**
    - Copy the default config file to `/sdcard/OhMyFont/config.cfg`. You can chage the default path inside the function itself.
- **`valof`** (value of)
    - Read value of a variable in the config file.  
    - Usage: `valof <variable>`  
    - E.g. `BOLD=$(valof BOLD)`
- **`rom`**
    - Try to make the module work system-wide on many ROMs which already use custom font by default. This function is only for sans-serif font family. You may not want to call it if changing font families other than sans-serif. You can also edit the function to add more customations for a specific ROM if needed. Make sure to call the function after copying fonts into `$SYSFONT` and patching fontxml and before `finish`.  
- **`install_font`**
    - You need at least one `Regular.ttf` for static font or one variable font in `$FONTS` to use the function. It will install sans-serif and sans-serif-condensed font family for you by creating missing font styles from available ones, copying fonts to `$SYSFONT` and patching fontxml.  
- **`bold`**
    - A font configuration (for sans-serif) to replace Regular style with Medium one. It reads `BOLD` value from the config file. Run this after `rom`.  

## How to use
For people who don't know where to start:
### Static fonts
- Put your fonts into `fonts` folder. Rename them as below:
	```
	BlackItalic
	Black
	ExtraBoldItalic
	ExtraBold
	BoldItalic
	Bold
	SemiBoldItalic
	SemiBold
	MediumItalic
	Medium
	Italic
	Regular
	LightItalic
	Light
	ExtraLightItalic
	ExtraLight
	ThinItalic
	Thin
	Condensed-BlackItalic
	Condensed-Black
	Condensed-ExtraBoldItalic
	Condensed-ExtraBold
	Condensed-BoldItalic
	Condensed-Bold
	Condensed-SemiBoldItalic
	Condensed-SemiBold
	Condensed-MediumItalic
	Condensed-Medium
	Condensed-Italic
	Condensed-Regular
	Condensed-LightItalic
	Condensed-Light
	Condensed-ExtraLightItalic
	Condensed-ExtraLight
	Condensed-ThinItalic
	Condensed-Thin
	```
    There must be at least one font `Regular`, the rest are optional.  
    Default font extension is `.ttf`, but if you have `.otf` font, set `X=.otf` before runing `install_font`.
- Add the following line to the bottom of the `customize.sh` script:  
    ```
    prep; $FB; config; install_font; rom; bold; finish
    ```
### Variable font (VF)
- You usually need two fonts, one for upright and the other for italic.
    Open the config file, at the bottom, set `SS=<upright font name>` (e.g. `SS=MyFont-VF.ttf`) and `SSI=<italic font name>` (e.g. `SSI=MyFontItalic-VF.ttf`).  
    If there is only one upright font, leave the `SSI` empty. Copy both fonts to the `fonts` folder.
- In the config file, set each font style from Thin to Black, from Upright to Condensed with desired axis and its value. E.g.
    ```
    ...
    UR=wght 400
    UBL=wght 900
    ...
    ISB=wght 600 slnt 1
    IL=wght 300 slnt 1
    ...
    CM=wght 500 wdth 75
    CT=wght 100 wdth 75
    ...
    DEB=wght 800 wdth 75 slnt 1
    ...
    ```
    If you have only upright font, just set upright font styles, leave the rest empty. They will take the value from upright automatically.
- The final step is the same as for static fonts.
## Support
- [XDA](https://forum.xda-developers.com/t/module-oh-my-font-improve-android-typography.4215515)
