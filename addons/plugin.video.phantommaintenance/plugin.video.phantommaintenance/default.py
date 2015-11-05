import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import subprocess
import urllib2,urllib
import re
import addon
import datetime
import time
import extract
#import checksuper
DEBUG_HUB = False

import navix
NAVIX_JD  = 150

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://phantomxbmc.googlecode.com/svn/not_touch/'
howto='http://xbmc-hub-repo.googlecode.com/svn/maintenance_do_not_touch/XBMC%20HUB%20GUIDES/txts/howto.txt'
ADDON=xbmcaddon.Addon(id='plugin.video.phantommaintenance')
versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])

javafolder = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'), 'java', 'bin'))
print '======================================='
print ADDON.getAddonInfo('path')
storage=ADDON.getSetting('storage')
boxbackupzip=ADDON.getSetting('boxbackupzip')+'.zip'
dropboxnumber=ADDON.getSetting('boxnumber')
boxuserdata='https://dl.dropbox.com/u/%s/%s'%(dropboxnumber,boxbackupzip)
linux_download=ADDON.getSetting('download_linux')
wallpaper_download=ADDON.getSetting('download_wallpaper')
hd_wallurl='http://www.hdwallpapers.in'
wallurl='http://wallpaperswide.com'

def DownloaderClass(url,dest, useReq = False):
    if DEBUG_HUB:
        print "**** DownloaderClass:%s" % url
    dp = xbmcgui.DialogProgress()
    dp.create("Phantom...Maintenance","Downloading & Copying File",'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()
    
def CATEGORIES():
        #addDir("How To Video's",howto,13,base+'images/VideoGuides.jpg',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir('Maintenance','url',9,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        addDir('Fixes','url',10,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','XBMC Fixes')
        addDir('Tweaks','url',11,base+'images/tweaks1.jpg',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        #addDir('Developer Tools','url',55,base+'images/developertools.jpg',base+'images/fanart/expert.jpg','Adding Special Stuff')
        addDir('HomeScreen Shortcuts','url',58,base+'images/home.jpg',base+'images/fanart/expert.jpg','Adding Special Stuff')
        #addDir('Fusion Installer','url',18,base+'images/fusion.jpg',base+'images/fanart/expert.jpg','Fusion Installer')
        #addDir('Upload Your LogFile','url',15,base+'images/logger.jpg',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        if DEBUG_HUB  or versionNumber < 12:
            addDir('Install Si02 For Eden',base + 'info/skin.txt',16,base+'images/si02.png',base+'images/fanart/expert.jpg','Adding Your Favourite Tweaks')
        if DEBUG_HUB  or xbmc.getCondVisibility('system.platform.android'):
            addDir('Anything Android','url',36,base+'images/android.jpg',base+'images/fanart/expert.jpg','')
        if DEBUG_HUB  or xbmc.getCondVisibility('system.platform.linux'):
            addDir('All Linux','url',38,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Anything Linux')
        #addDir('Need Help??','url',2000,base+'images/needhelp.jpg',base+'images/fanart/expert.jpg','Fusion Installer')
        if ADDON.getSetting('message')=='false' and not xbmc.getCondVisibility('system.platform.atv2') and not xbmc.getCondVisibility('system.platform.ios')and not xbmc.getCondVisibility('system.platform.osx') and not xbmc.getCondVisibility('system.platform.windows'): 
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Did You Know You Can Now Flash Your Android Box", "With Linux Also You Can Remove Checks And Resign","All Within The Plugin!!")
            ADDON.setSetting('message','true')
        setView('movies', 'MAIN')
        
def top_secret():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]THIS DIRECTORY !?![/B]','', "[B][COLOR red]IS FOR DEVELOPER AND EXPERIENCED USERS ONLY !!![/B][/COLOR]"):
        addDir('Install Developers Scripts','url',56,base+'images/developertools.jpg',base+'images/fanart/expert.jpg','Download The development url resolver if its broke thats your problem')
        addDir('Restore Original Scripts ','url',57,base+'images/developertools.jpg',base+'images/fanart/expert.jpg','Revert Back to your old url resolver')
        setView('movies', 'SUB')
                
        
def alllinux(url):
        addDir('TLBB Beta','url',33,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box TLBB Beta !!')
        addDir('Pivos NightLies Flash/Remove Checks','http://www.pivosforums.com/viewtopic.php?f=11&t=941',33,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Toys4Me Flash/Remove Checks','url',42,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Flash GeekSquad or J1nx','http://www.pivosforums.com/viewtopic.php?f=11&t=941',53,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('MyGica A11 Flash','url',52,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Enter Recovery/Upgrade','url',19,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Fed up with holding that stupid upgrade button down just use this make sure your upgrade image is on card and plugged in')
        if not ADDON.getSetting('storage')=='false':
            if os.path.exists(os.path.join(storage,'xbmc-data'))==False:
                addDir('[COLOR yellow]Move Userdata To Storage[/COLOR]','url',54,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        setView('movies', 'SUB')
        
        
def allandroid(url):
        addDir("Add GSH's PlayerCore.xml",base + 'playercorefactory.xml',37,base+'images/android.jpg',base+'images/fanart/expert.jpg','Change your playercorefactory hardware accelerated players to gsh xml')
        addDir('Pivos Flash/Remove Checks','http://www.pivosforums.com/viewtopic.php?f=11&t=941',33,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Toys4Me Flash/Remove Checks','url',42,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Flash GeekSquad or J1nx','http://www.pivosforums.com/viewtopic.php?f=11&t=941',53,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('MyGica A11 Flash','url',52,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Flash Your Box With Linux And Open Your World !!')
        addDir('Enter Recovery/Upgrade','url',19,base+'images/alllinux.jpg',base+'images/fanart/expert.jpg','Fed up with holding that stupid upgrade button down just use this make sure your upgrade image is on card and plugged in')
        setView('movies', 'SUB')

def maintenance(url):
        #addDir('Download All Repos',base + 'allrepos.zip',35,base+'repoinstalls/xbmchubrepo/icon.png',base+'repoinstalls/xbmchubrepo/fanart.jpg','Install All Popular Repos In One Click All Repos From Fusion')
        #addDir("Download All UK Plugins/Repos",base + 'uk.zip',35,base+'repoinstalls/xbmchubrepo/icon.png',base+'repoinstalls/xbmchubrepo/fanart.jpg','Install All Uk Plugins and Repos')
        addDir('Remove Addons','plugin.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted plugins')
        addDir('Remove Repos','repository.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted Repositories')
        addDir('Remove Skins','skin.',25,base+'images/recycle.png',base+'images/fanart/beginners.jpg','Safely Remove Unwanted Skins')
        addDir('Delete My Cache','url',3,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Safely delete all cache from plugins')
        #addDir('Delete Stale Thumbnails','url',111,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Delete stale thumbnails and textures')
        addDir('Delete Packages','url',2,base+'images/maintenance.jpg',base+'images/fanart/advanced.jpg','Delete all you old zipped packages very safe but you wont be able to roll back')
        addDir('Delete Crash Logs','url',1,base+'images/maintenance.jpg',base+'images/fanart/advanced.jpg','Delete all your old crash logs')
        if DEBUG_HUB  or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx') or xbmc.getCondVisibility('system.platform.android'):
            #addDir('Update Lib File','url',12,base+'images/maintenance.jpg',base+'images/fanart/expert.jpg','Update you lib file for rtmp live streams')
        setView('movies', 'SUB')
        
def fixesdir(url):
        addDir('1Channel Domain Fix',base+'fix/plugin.video.1channel-2.0.1.zip',59,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Use This to fix 1channel Domain issue')
        addDir('1Channel Subscription Fix',base+'fix/service.py',63,base+'images2/fixes.jpg',base+'images2/fanart/advanced.jpg','Use This to fix 1channel Subscriptions')
        addDir('Hulu Fix',base+'fix/script.module.cryptopy.zip',39,base+'images/hulu.png',base+'images/fanart/advanced.jpg','Fix For Hulu')
        #addDir('YouTube Fix',base+'',30,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Fix For YouTube')
        addDir('BBC iPlayer Fix',base+'',31,base+'fix/icon.png',base+'images/fanart/advanced.jpg','Go back to 2.0.17 but with the fix')
        if DEBUG_HUB  or versionNumber < 12:
            if 'listitem.addContextMenuItems(cm, replaceItems=True)' in oldlogfile() or 'listitem.addContextMenuItems(cm, replaceItems=True)' in logfile():
                addDir('1Channel Eden Fix',base+'fix/1channelfix.txt',4,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Use This If you Get This Error in your Log \n"listitem.addContextMenuItems(cm, replaceItems=True)"')
        addDir('1Channel Reboot Fix (Only Use If ATV2 Reboots)',base+'fix/1channelfix.txt',20,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Having problems with having to reboot xbmc to view next movie or tv show then this is your fix for that')
        addDir('1Channel Subtitles Fix',base+'fix/1channelfix.txt',27,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Use This To Fix Subtitles Not Working')
        try:
            if 'DatabaseError: database disk image is malformed' in oldlogfile() or 'DatabaseError: database disk image is malformed' in logfile():
                addDir('1Channel.db Issues Fix ','url',8,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your 1Channel.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \n plugin.video.1channel/default.py \n"DatabaseError: database disk image is malformed"\nThen use this fix')
                addDir('1Channel/Icefilms Meta_Cache Fix','url',7,base+'images/fixes.jpg',base+'images/fanart/advanced.jpg','Only Use this if you Know that it is your meta_cache video_cache.db is malformed \n\nIF YOU GET THIS MESSAGE IN YOUR LOG \nlib/metahandler/metahandlers.py \n"DatabaseError: database disk image is malformed"\n\n Then use this fix')
        except:
            pass
        #addDir('Extend Captcha Times','url',24,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','If you can never see the captchas for long enough please install this it will give you 5 seconds to read the captcha before the keyboard pops up')
        #addDir('Fix Slow Gui Issues','url',28,base+'images/maintenance.jpg',base+'images/fanart/beginners.jpg','Fix Slow GUI (Not Necessarily Going To Work For All!!)')
        setView('movies', 'SUB')
        
def tweaksdir(url):
        addDir("Wallpaper Downloads",howto,48,base+'images/wallpapers.jpg',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir('Confluence 7 Icons (Frodo Only)','url',40,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add 7 Icons To Your Home Menu For Video')
        addDir('Add Tuxens Advanced XML',base+'tweaks/tuxen.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        #addDir('Add HUB Advanced XML',base+'tweaks/mikeys.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Add 0 Cache Advanced XML',base+'tweaks/0cache.xml',5,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Check What XML You Are Using','url',29,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Check what advancedsettings.xml your are using')
        addDir('Delete Advanced XML','url',14,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Add advanced xml to sort your buffering if you have issues')
        addDir('Backup Advanced XML','Back Up',61,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Back up advanced xml')
        addDir('Restore Advanced XML','Restore',61,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','Restore advanced xml')
        if DEBUG_HUB  or xbmc.getCondVisibility('system.platform.ATV2'):
            addDir('Add Skip Forward/Back 10 Mins',base+'tweaks/joystick.AppleRemote.xml',6,base+'images/tweaks.jpg',base+'images/fanart/expert.jpg','ATV2 must have so you can push up or down to skip 10 minutes back or forward')
        if navix.installed():
            addDir('Add JDownloader Option to Navi-X', base, NAVIX_JD,base+'images/tweaks.jpg', base+'images/fanart/expert.jpg', 'Add JDownloader Option to Navi-X Download menu')            
        setView('movies', 'SUB')
        
def wallpaper_catergories():
        addDir("wallpaperswide.com",howto,44,base+'images/wallpaperwide.png',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        addDir("hdwallpapers.in",howto,49,'http://www.hdwallpapers.in/templates/custom/images/logo.png',base+'images/fanart/gettingstarted.jpg','Safely delete all cache from plugins')
        
        
############################################################        STANDARD CACHE          ###############################################################  
  
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
                             

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        PACKAGES          ###############################################################    
          
def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "Bloody Packages Wont Delete Can Some Developer", "Sort It!!    [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
        
############################################################        DELETING CRASH LOGS          ###############################################################    
        
def DeleteCrashLogs(url):  
    print '############################################################       DELETING CRASH LOGS             ###############################################################'
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Old Crash Logs", '', "Do you want to delete them?"):
        path=loglocation()
        import glob
        for infile in glob.glob(os.path.join(path, 'xbmc_crashlog*.*')):
             File=infile
             print infile
             os.remove(infile)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "Please Reboot XBMC To Take Effect !!", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
            
            
            
############################################################        1CHANNEL FIX         ###############################################################    
                
def OneChannel(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################       1CHANNEL EDEN FIX           ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel', ''))
        onechannel=os.path.join(path, 'default.py')
        os.remove(onechannel)
        print '========= REMOVING  '+str(onechannel)+'    =========================='
        link=OPEN_URL(url)
        a = open(onechannel,"w") 
        a.write(link)
        a.close()
        print '========= WRITING NEW  '+str(onechannel)+'=========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
    
############################################################        ADVANCE XML          ############################################################### 

def restoreadvancexml(url):
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    dialog = xbmcgui.Dialog()
    r='%s Your Original XML ?'% url
    if dialog.yesno("Back Up Original", '',r, ""):
        if 'Restore' in url:
            print '############################################################       Restore XML          ###############################################################'
            try:
                os.remove(advance)
                print '========= REMOVING    '+str(advance)+'    ====================================='
            except:
                pass
            os.rename(os.path.join(path, 'advancedsettings.xml.bak'),advance)
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        else:
            print '############################################################       Back Up XML          ###############################################################'

            os.rename(advance,os.path.join(path, 'advancedsettings.xml.bak'))
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
def advancexml(url,name):
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    dialog = xbmcgui.Dialog()
    bak=os.path.join(path, 'advancedsettings.xml.bak')
    if os.path.exists(bak)==False: 
        if dialog.yesno("Back Up Original", 'Have You Backed Up Your Original?','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
            print '############################################################       ADVANCE XML          ###############################################################'
            path = xbmc.translatePath(os.path.join('special://home/userdata',''))
            advance=os.path.join(path, 'advancedsettings.xml')
            try:
                os.remove(advance)
                print '========= REMOVING    '+str(advance)+'    ====================================='
            except:
                pass
            link=OPEN_URL(url)
            a = open(advance,"w") 
            a.write(link)
            a.close()
            print '========= WRITING NEW    '+str(advance)+'    =========================='
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    else: 
        print '############################################################       ADVANCE XML          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/userdata',''))
        advance=os.path.join(path, 'advancedsettings.xml')
        try:
            os.remove(advance)
            print '========= REMOVING    '+str(advance)+'    ====================================='
        except:
            pass
        link=OPEN_URL(url)
        a = open(advance,"w") 
        a.write(link)
        a.close()
        print '========= WRITING NEW    '+str(advance)+'    =========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
############################################################        CHECK ADVANCE XML          ###############################################################    
    
def checkadvancexml(url,name):
    print '############################################################       CHECK ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    try:
        a=open(advance).read()
        if 'mike' in a:
            name='MIKEYS'
        elif 'zero' in a:
            name='0'
        elif 'tuxen' in a:
            name='TUXENS'
    except:
        name="NO ADVANCED"
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev","[COLOR yellow]YOU HAVE[/COLOR] "+ name+"[COLOR yellow] SETTINGS SETUP[/COLOR]",'', "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
############################################################        DELETE ADVANCE XML          ###############################################################    
def deleteadvancexml(url):
    print '############################################################       DELETING ADVANCE XML          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    advance=os.path.join(path, 'advancedsettings.xml')
    os.remove(advance)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
############################################################        KEYMAPS          ###############################################################    
    
    
def joystick(url): 
    print '############################################################        KEYMAPS          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata/keymaps',''))
    joystick=os.path.join(path, 'joystick.AppleRemote.xml')
    try:
        os.remove(joystick)
        print '========= REMOVING    '+str(joystick)+'     =========================='
    except:
        pass
    link=OPEN_URL(url)
    a = open(joystick,"w") 
    a.write(link)
    a.close()
    print '========= WRITING NEW    '+str(joystick)+'     =========================='
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        CORRUPT META          ###############################################################    
    
def malformed(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################        CORRUPT META          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.module.metahandler/meta_cache',''))
        meta=os.path.join(path, 'video_cache.db')
        try:
            os.remove(meta)
            print '========= REMOVING  '+str(meta)+'     =========================='
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       CANT DELETE!!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        print '========= WRITING NEW   '+str(meta)+'     =========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "           REBOOT XBMC !!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
############################################################        1CHANNEL.DB CORRUPT         ###############################################################    
    
def onechanneldb(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     AS YOU CANNOT GO BACK !!![/B][/COLOR]"):
        print '############################################################        1CHANNEL.DB CORRUPT          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/userdata/Database',''))
        onechanneldb=os.path.join(path, 'onechannelcache.db')
        try:
            os.remove(onechanneldb)
            print '========= REMOVING   '+str(onechanneldb)+'     =========================='
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       CANT DELETE!!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        print '========= WRITING NEW   '+str(onechanneldb)+'     =========================='
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "           REBOOT XBMC !!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        LYB          ###############################################################    
    
def loglocation(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        log = os.path.join(log_path, 'xbmc.log')
    return log_path
    
def logfile(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
    
    log = os.path.join(log_path, 'xbmc.log')
    logfile=open(log, 'r').read()
    return logfile

    
def oldlogfile(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
    
    log = os.path.join(log_path, 'xbmc.old.log')
    logfile=open(log, 'r').read()
    return logfile

    
def lib(url): 
    print '############################################################        LYB          ###############################################################'
    log_path=loglocation()
    log = os.path.join(log_path, 'xbmc.log')
    logfile=open(log, 'r').read()
    if 'Windows' in logfile:
        match = re.compile('special://xbmc/ is mapped to: (.+?)\\XBMC').findall(logfile)
        path = xbmc.translatePath(os.path.join(match[0]+'XBMC\system\players\dvdplayer',''))
        lib=os.path.join(path, 'librtmp.dll')
        try:
            os.remove(lib)
        except:
            pass
        url = base+'lib/windows/librtmp.dll'
        DownloaderClass(url,lib)
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
    if 'Darwin OSX' in logfile:
        try:    
            match = re.compile('special://frameworks/ is mapped to: (.+?)Frameworks').findall(logfile)
            path = xbmc.translatePath(os.path.join(match[0]+'Frameworks',''))
            lib=os.path.join(path, 'librtmp.0.dylib')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/mac/librtmp.0.dylib'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
    if 'Darwin iOS' in logfile:
        try:    
            match = re.compile('special://frameworks/ is mapped to: (.+?)Frameworks').findall(logfile)
            path = xbmc.translatePath(os.path.join(match[0]+'Frameworks',''))
            lib=os.path.join(path, 'librtmp.0.dylib')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/atv/librtmp.0.dylib'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
            
    if 'Android,' in logfile:
        try:    
            path = xbmc.translatePath(os.path.join('/data/data/org.xbmc.xbmc/lib',''))
            lib=os.path.join(path, 'librtmp.so')
            try:
                os.remove(lib)
            except:
                pass
            url = base+'lib/android/librtmp.so'
            DownloaderClass(url,lib)
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "       CANT UPDATE YOUR LIB FILE SORRY!!!", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
            
    print '########################### LIB LOCATION ####################'
    print lib
    
def Shrink(db):
    from sqlite3 import dbapi2 as sqlite3
    try:
        db   = xbmc.translatePath(db)
        conn = sqlite3.connect(db, timeout = 10, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread = False)
        c    = conn.cursor()

        c.execute("DELETE FROM texture WHERE id > 0")       
        c.execute("VACUUM")       

        conn.commit()
        c.close()
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "Sorry There Was A Problem Please Manually ", "Delete Textures.db")
        
    
def GetFile(filepath):
     import glob
     path = filepath
     for infile in glob.glob(os.path.join(path, 'Textures*.*')):
         File=infile
         print infile
     return File
    
     
def howtos(url,fanart):
        link=OPEN_URL(url)
        match=re.compile('i="(.+?)" n="(.+?)" u="(.+?)" d="(.+?)"').findall(link)
        for icon, name, youtube , description in match:
                if icon=='none':
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % youtube
                else:
                    iconimage=str(icon)
                print iconimage
                fanart=str(fanart)
                url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube
                addDir(name,url,2001,iconimage,fanart,description)        
                setView('movies', 'SUB') 
                
def PLAY_STREAM(name,url,iconimage,description):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
                
                
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
     
def uploadlog(url): 
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "A New Window Will Now Open For You To In Put", "Your Email Address For The Logfile To Be Emailed To")
        ADDON.openSettings()
    addon.LogUploader()
    
############################################################        SKIN          ###############################################################    
    
def fastcoloreden(url,iconimage):    
        link=OPEN_URL(url)
        match=re.compile('skinurl="(.+?)" name"(.+?)" icon="(.+?)"').findall(link)
        for url,name,iconimage in match:
            addDir(name,url,17,iconimage,'','Download'+str(name))
            
def downloadanything(url,name):     
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, name)
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(4)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Phantom Dev", "Would You Like To Change Skin Now", "Window Will Change To Apperance Settings"):
        xbmc.executebuiltin("XBMC.ActivateWindow(appearancesettings)")
        
        
         ############################################################        HOME ICONS           ###############################################################    
         
def select_button(): 
    dialog=xbmcgui.Dialog()
    version_select=['Videos','Music','Programs','Pictures']
    select=['Videos','Music','Programs','Pictures']
    return version_select[xbmcgui.Dialog().select('Please Choose Your Build', select)]
         
         
def homeicons(url):
    gui_path = xbmc.translatePath(os.path.join('special://home', 'userdata'))
    gui = os.path.join(gui_path, 'guisettings.xml')
    guixml = open(gui, 'r').read()
    #guixml = guixml.split('skin.confluence.Home_Custom_Back_Settings_Folder')[1]
    button=select_button()
    r=name="skin.confluence.Home%sButton(.+?)"%button
    match=re.compile(r).findall(guixml)
    for number in match:
        addDir(button+' Button '+number,'url',62,'','','')
        
def homeicons2(name):
    if 'Video' in name:
        r="Skin.SetAddon(Home%s,xbmc.addon.video,xbmc.addon.executable)"%name.replace(' ','')
    elif 'Music' in name:
        r="Skin.SetAddon(Home%s,xbmc.addon.audio,xbmc.addon.executable)"%name.replace(' ','')
    elif 'Pictures' in name:
        r="Skin.SetAddon(Home%s,xbmc.addon.image,xbmc.addon.executable)"%name.replace(' ','')
    elif 'Programs' in name:
        r="Skin.SetAddon(Home%s,xbmc.addon.executable)"%name.replace(' ','')
        
    xbmc.executebuiltin(r)
    #xbmc.executebuiltin("XBMC.ActivateWindow(SkinSettings)")   
    
        
    
         ############################################################        FUSION INSTALLER           ###############################################################    
def FusionInstaller(url):
    print '############################################################        FUSION INSTALLER          ###############################################################'
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>FUSION</name><path pathversion="1">http://fusion.Maguinho</path></source></files></sources>')
        f.close()
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
        return
        
    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if 'http://fusion.Maguinho' in str:
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Phantom Dev", "Please Select Install From Zip Then ", "Select Fusion On The Right Hand Side"):
            xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
            xbmc.executebuiltin("XBMC.ActivateWindow(AddonBrowser)")
    if not'http://fusion.Maguinho' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>FUSION</name><path pathversion="1">http://fusion.Maguinho</path></source></files>')
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>FUSION</name><path pathversion="1">http://fusion.Maguinho</path></source></files></sources>')
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Reboot To Take Effect Then Come", "Back Here To Install Your Plugins")
            f = open(path, mode='w')
            f.write(str)
            f.close()
    
            
   
    
         ############################################################        1Channel REBOOT FIX           ###############################################################   
def onechannelreboot(url):
    print '############################################################        1Channel REBOOT FIX        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel',''))
    lib=os.path.join(path, 'playback.py')
    os.remove(lib)
    url = base+'fix/playback.py'
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
def onechanneldown(url):
    print '############################################################        1 Channel     ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel','resources'))
    settings=os.path.join(path, 'settings.xml')
    f   = open(settings, mode='r')
    str = f.read()
    f.close()
    replacewith=str.replace('<setting id="domain" type="labelenum" label="Domain" values="http://www.1channel.ch|http://www.letmewatchthis.ch" default="http://www.letmewatchthis.ch"/>','<setting id="domain" type="labelenum" label="Domain" values="http://www.1channel.ch|http://www.letmewatchthis.ch|http://www.primewire.ag" default="http://www.primewire.ag"/>')
    f = open(settings, mode='w')
    f.write(replacewith)
    f.close()
    channel=xbmcaddon.Addon(id='plugin.video.1channel')
    channel.setSetting('domain','http://www.primewire.ag')
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "All Done Thanks", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
def onechannelsub(url):
    print '############################################################        1Channel REBOOT FIX        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.1channel',''))
    lib=os.path.join(path, 'service.py')
    os.remove(lib)
    url = base+'fix/service.py'
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "All Done Thanks", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
         ############################################################        INSTALL XBMCHUB REPO           ###############################################################   
def xbmchubrepo(url):
    print '############################################################        INSTALL XBMCHUB REPO        ###############################################################'
    url = 'http://xbmc-hub-repo.googlecode.com/svn/addons/repository.xbmchub/repository.xbmchub-1.0.1.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'repository.xbmchub-1.0.1.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
    extract.all(lib,addonfolder,dp)

    ############################################################        Recovery        ###############################################################
def doRecovery(url = None):
    print '############################################################        Android Recovery        ###############################################################'
    dialog = xbmcgui.Dialog()
    if (url == None) or (dialog.yesno('Phantom Dev', "Are you sure you want to enter recovery mode?")):
       os.system('reboot recovery')
       
    ############################################################        Remove Mikey        ###############################################################
def removemikey(url):
    print '############################################################        Remove Mikey       ###############################################################'
    for root, dirs, files in os.walk(url):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.rmdir(url)
    
    
        ############################################################       Restore Userdata       ###############################################################'
def restore(url):
        print '############################################################       Restore Userdata       ###############################################################'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        zippath=os.path.join(path, boxbackupzip)
        DownloaderClass(url,zippath)
        userdata = xbmc.translatePath(os.path.join('special://profile/addon_data/',''))
        time.sleep(3)
        dp = xbmcgui.DialogProgress()
        dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
        extract.all(zippath,userdata,dp)
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "Thats It All Done", " [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        os.remove(zippath)
        if xbmc.getCondVisibility('system.platform.ATV2'):
            os.chmod(userdata, stat.S_IRWXO)        
        
         ############################################################        CAPTCHA FIX           ###############################################################   
def captcha(url):
    print '############################################################        CAPTCHA FIX       ###############################################################'
    url = base + 'fix/vidxden.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/script.module.urlresolver/lib/urlresolver/','plugins'))
    lib=os.path.join(path, 'vidxden.py')
    DownloaderClass(url,lib)
    url = base + 'fix/putlocker.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/script.module.urlresolver/lib/urlresolver/','plugins'))
    lib=os.path.join(path, 'putlocker.py')
    DownloaderClass(url,lib)
    
    
    ############################################################       REMOVE ADDON             ###############################################################'
def findaddon(url,name):  
    print '############################################################       REMOVE ADDON             ###############################################################'
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    import glob
    for file in glob.glob(os.path.join(pluginpath, url+'*')):
        name=str(file).replace(pluginpath,'').replace('plugin.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','')
        iconimage=(os.path.join(file,'icon.png'))
        fanart=(os.path.join(file,'fanart.jpg'))
        addDir(name,file,26,iconimage,fanart,'')
        setView('movies', 'SUB') 
         ############################################################        SUBTITLE FIX           ###############################################################   
def subtitle(url):
    print '############################################################        SUBTITLE FIX       ###############################################################'
    url = base + 'fix/default.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.1channel'))
    lib=os.path.join(path, 'default.py')
    DownloaderClass(url,lib)
    url = base + 'fix/playback.py'
    path = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.1channel'))
    lib=os.path.join(path, 'playback.py')
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "Thats It All Done", " [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
         ############################################################       SLOW GUI          ###############################################################    
def gui(url):
    print '############################################################        SLOW GUI         ###############################################################'
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'advancedsettings.xml')
    try:
        f   = open(path, mode='r')
        str = f.read()
        f.close()
        if '<algorithmdirtyregions>3</algorithmdirtyregions>' in str:
                str = str.replace('<algorithmdirtyregions>3</algorithmdirtyregions>','<algorithmdirtyregions>0</algorithmdirtyregions>')
                dialog = xbmcgui.Dialog()
                dialog.ok("Phantom Dev", 'You Had Dirty Regions Set To "3"', "All Fixed And Disabled")
                f = open(path, mode='w')
                f.write(str)
                f.close()
        else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Phantom Dev", 'You Have Not Got Dirty Regions "3"', "So Sorry You Just Have A Slow Box")
                f = open(path, mode='w')
                f.write(str)
                f.close()
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", 'You Have Not Got Any Advanced Settings Anyway', "So Sorry You Just Have A Slow Box")
        
            
def select_build(): 
    dialog=xbmcgui.Dialog()
    version_select=['Frodo','Eden']
    select=['Frodo','Eden']
    return version_select[xbmcgui.Dialog().select('Please Choose Your Build', select)]
   
         ############################################################        YouTube Fix           ###############################################################   
def youtubefix(name):
    print '############################################################        YouTube Fix       ###############################################################'
    version=select_build()
    url = base+'plugin.video.youtube-'+str(version)+'.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'plugin.video.youtube.zip')
    youtube = xbmc.translatePath(os.path.join('special://home/addons','plugin.video.youtube'))
    for root, dirs, files in os.walk(youtube):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.rmdir(youtube)
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "YouTube Is Now Fixed !!", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
def bbcfix(name):
    print '############################################################        BBC FIX       ###############################################################'
    url = base + 'fix/plugin.video.iplayer-2.0.18a.zip'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'plugin.video.iplayer-2.0.18a.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "All Done", "   [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
############################################################        URL RESOLVER        ###############################################################
def resolver(name):
    dialog = xbmcgui.Dialog()
    image_select=['EDEN','FRODO']
    select=['https://github.com/Eldorados/'+name+'/archive/master.zip','https://github.com/Eldorados/'+name+'/archive/frodo.zip']
    return select[xbmcgui.Dialog().select('Which Version ?', image_select)]
    
def restoredeveloper():
    dialog = xbmcgui.Dialog()
    image_select=['script.module.urlresolver','plugin.video.1channel','script.module.t0mm0.common','script.module.metahandler','Cancel']
    select=['script.module.urlresolver','plugin.video.1channel','script.module.t0mm0.common','script.module.metahandler','Cancel']
    return select[xbmcgui.Dialog().select('Which Choose?', image_select)]
    
    
    
def fixurlresolver(name):
    name=restoredeveloper() 
    if name=='Cancel':
        print 'cancelled'
    else:
        print '############################################################        FIX '+name+'          ###############################################################'
        path = xbmc.translatePath(os.path.join('special://profile/addon_data/'+name,name+'-backup.zip'))
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',name))
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
            extract.all(path,addonfolder,dp)
            os.remove(path)
            dialog = xbmcgui.Dialog()
            r="Original [COLOR yellow]%s[/COLOR] Restored"%name
            dialog.ok("Phantom Dev", r, '',"[COLOR yellow]Brought To You By Maguinho[/COLOR]")
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Nothing To Be Restored",'', "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
def zip_backup_folder(name):  
    to_backup = xbmc.translatePath(os.path.join('special://home/addons',name))
    backupfolder = xbmc.translatePath(os.path.join('special://profile/addon_data',name))
    backup_zip = xbmc.translatePath(os.path.join('special://profile/addon_data/'+name,name+'-backup.zip'))
    if os.path.exists(backup_zip):
        print '*************** BACKUP FOLDER EXISTS **************'
    else:
        print '*************** CREATING BACKUP FOLDER **************'
        import zipfile
        import sys
        if os.path.exists(backupfolder)==False:
            os.makedirs(backupfolder)
        zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(to_backup) + 1
        for base, dirs, files in os.walk(to_backup):
            for file in files:
                fn = os.path.join(base, file)
                zipobj.write(fn, fn[rootlen:])
                
                
    
def downloadurlresolver(name):
    name=restoredeveloper() 
    if name=='Cancel':
        print 'cancelled'
    else:
        print '############################################################        INSTALLING '+name+'          ###############################################################'
        zip_backup_folder(name)
        if '1channel' in name:
            url = 'https://github.com/bstrdsmkr/1Channel/archive/master.zip'
        else:
            url = resolver(name)
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, name+'-dev.zip')
        try:
            os.remove(lib)
        except:
            pass
        DownloaderClass(url,lib)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        import zipfile
     
        zipdata = zipfile.ZipFile(lib)
        zipinfos = zipdata.infolist()
     
        for zipinfo in zipinfos:
            zipinfo.filename =  zipinfo.filename.replace('-master','').replace('-frodo','').replace('1Channel',name)
            zipdata.extract(zipinfo,addonfolder)
        dialog = xbmcgui.Dialog()
        r="Developer [COLOR yellow]%s[/COLOR] Installed "%name
        dialog.ok("Phantom Dev", r,'', "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        LINUX        ###############################################################
        
def image_select():
    dialog = xbmcgui.Dialog()
    select=['M1','M3']
    image_select=['M1','M3']
    return select[xbmcgui.Dialog().select('Which Version ?', image_select)]
    
def image_nightlies_select_url():
    dialog = xbmcgui.Dialog()
    url=['https://www.dropbox.com/sh/qfsqqow67m8hawp/izMaTF_I4f/m1','https://www.dropbox.com/sh/qfsqqow67m8hawp/xWXi4ONQjX/m3']
    image_select=['M1','M3']
    return url[xbmcgui.Dialog().select('Which Version ?', image_select)]

def getimgdropbox(url):
    link=OPEN_URL(url)
    match=re.compile('MB</div><a href="(.+?)"').findall(link)
    return match[0]
    
def toys4me_select_url():
    dialog = xbmcgui.Dialog()
    url=['http://d-h.st/users/toys4me/?fld_id=11798#files','http://d-h.st/users/toys4me/?fld_id=10436#files']
    image_select=['M1','M3']
    return url[xbmcgui.Dialog().select('Which Version ?', image_select)]
    
def choose_storage():
    dialog = xbmcgui.Dialog()
    url=['/media/usb0','/media/sdcard']
    image_select=['USB','SDCARD']
    return url[xbmcgui.Dialog().select('USB OR STORAGE ?', image_select)]
    
    
def move_to_storage(name,url,iconimage):
    choose=choose_storage()
    os.makedirs(os.path.join(choose, 'xbmc-data')) 
    ADDON.setSetting('storage',choose)
     
    doreboot()    
    
def doreboot():
    print '############################################################        Reboot        ###############################################################'
    dialog = xbmcgui.Dialog()
    if dialog.yesno('Phantom Dev', "You Need To Reboot To Take Effect","You Want To Do It Now"):
       os.system('reboot')
            
    
def toys4me(name,url,iconimage):
    url=toys4me_select_url()
    print url
    link=OPEN_URL(url)
    match=re.compile('<a href="(.+?)">(.+?).img</a>').findall(link)
    yourversion='[B][COLOR yellow]Your Version Build Date: %s[/B][/COLOR]'%(myversion())
    addDir(yourversion,'url',34,iconimage,'',name)
    for url,name in match:
        regex=re.compile('(.+?)-(.+?)-(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)')
        match=regex.search(name)
        name='Date:%s%s/%s%s/%s%s%s%s - %s-%s'%(match.group(5),match.group(6),match.group(3),match.group(4),match.group(7),match.group(8),match.group(9),match.group(10),match.group(1).upper(),match.group(2).upper())
        url='http://d-h.st'+url
        addDir(name,url,43,iconimage,'','')  
        
def toys4medownload(name,url,iconimage):
    filename = 'toys4meimage.img'
    link     = OPEN_URL(url)
    match    = re.compile('action="(.+?)"').findall(link)
    path     = xbmc.translatePath(os.path.join(linux_download,''))
    img      = os.path.join(path, filename)

    if not DEBUG_HUB:
        try:
            os.remove(img)
        except:
            pass

    if not os.path.exists(img):
        try: 
            DownloaderClass(match[0],img)
        except:
            os.remove(img)
            return

    okFlash = False

    time.sleep(1)
    dialog = xbmcgui.Dialog()
    if 'M3' in name:
        if dialog.yesno("What Do You Want To Do ?", '','Do You Want To Remove Checks or Flash',"",'FLASH','R/CHECKS'):
            import checks
            okFlash = checks.remove(filename, DEBUG_HUB) 
        else:
            okFlash = True
            os.rename(img, os.path.join(path, 'update.img'))
    else:
        okFlash = True
        os.rename(img, os.path.join(path, 'update.img'))
    if okFlash:   
        if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
            ADDON.setSetting('storage','true')
            doRecovery()
        
    
def pivos_image(name,url,iconimage):
        yourversion='[B][COLOR yellow]Your Version Build Date: %s[/B][/COLOR]'%(myversion())
        addDir(yourversion,'url',34,iconimage,'',name)
        if 'url' in url :
            tlbb = xbmc.translatePath(os.path.join('special://home/addons','script.tlbb'))
            if os.path.exists(tlbb) == True:
	            url='https://www.dropbox.com/sh/l34dlmyc7t9qnu5/EAR-r7fLUR'
	            print '############################################################     TLBB NIGHTLIES      ###############################################################'
	            link=OPEN_URL(url)
	            match=re.compile('<div class="filename"><a href="(.+?)tlbb(.+?)zip" target="_top" class="filename-link" onclick="" rel="nofollow"><span id="emsnippet-.+?"></span></a></div></div><div class="filesize-col"><span class="size">(.+?)</span></div><div class="modified-col"><span><span class="modified-time">(.+?)</span>').findall(link)
	            for url,name,size,date in match:
	                url= url+'tlbb'+name+'zip'
	                name='tlbb'+name+'zip ['+date+' '+size+']' 
	                print url
	                url=getimgdropbox(url)
	                addDir(name,url,41,iconimage,'','To Install This '+name+' Please Go Ahead And Click on The One you Desire')
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Phantom Dev", '','SORRY YOU DO NOT HAVE A TLBB', "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
                return

        else:
        
            print '############################################################     LINUX IMAGE NIGHTLIES      ###############################################################'
            url=image_nightlies_select_url()
            print url
            link=OPEN_URL(url)
            if re.search('/m1',url,re.IGNORECASE):
                v='m1'
            else:
                v='m3'
            link=link.split(v+'/MD5SUM')[2]
            match=re.compile('<div class="filename"><a href="(.+?)update(.+?)img" target="_top" class="filename-link" onclick="" rel="nofollow"><span id="emsnippet-.+?"></span></a></div></div><div class="filesize-col"><span class="size">(.+?)</span></div><div class="modified-col"><span><span class="modified-time">(.+?)</span>').findall(link)
            for url,name,size,date in match:
                url= url+'update'+name+'img'
                name='update'+name+'img'+' ['+date+' '+size+']' 
                url=getimgdropbox(url)
                addDir(name,url,41,iconimage,'','To Install This '+v.upper()+' Please Go Ahead And Click on The One you Desire')
                
                
def geek_j1nx_image(name,url,iconimage):
        dialog = xbmcgui.Dialog()
        if dialog.yesno("What Is Your Box", '','',"",'M3','M1'):
            url=base + 'linuxflash/jynx_m1.img'
            print '======= Jynx M1 ======='
            install_linux_image('Jynx M1',url,iconimage)
        else:
            if dialog.yesno("Which Image?", '','',"",'GEEKSQUAD','JYNX'):
                url=base + 'linuxflash/jynx_m3.img'
                print '======= Jynx M3 ======='
                install_linux_image('Jynx M3',url,iconimage)
            else:
                url=base + 'linuxflash/Geeksquad8.m3.img'
                print '======= GEEKSQUAD M3 ======='
                install_linux_image('GEEKSQUAD M3',url,iconimage)
                    
                    
def mygica_flash(name,url,iconimage):
    url=base + 'linuxflash/mygica.img'
    install_linux_image('MYGICA',url,iconimage)
    
    
def install_linux_image(name,url,iconimage):
    dialog = xbmcgui.Dialog()
    if linux_download == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
        ADDON.openSettings()
    path = xbmc.translatePath(os.path.join(linux_download,''))
    img=os.path.join(path, 'update.img')
    try:
        os.remove(img)
    except:
        pass
    DownloaderClass(url,img)
    time.sleep(2)
    if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
        doRecovery(url)       
                    
                    
def install_linux_nightlies(name,url,iconimage,description):
    if '.img' in url:
        url = str(url)
        try:
            name = name.split(' [')[0]
        except:
            pass
        dialog = xbmcgui.Dialog()
        if linux_download == '':
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
            ADDON.openSettings()
        filename = 'nightlies.img'
        path     = xbmc.translatePath(os.path.join(linux_download,''))
        img      = os.path.join(path, filename)
    
        if not DEBUG_HUB:
            try:
                os.remove(img)
            except:
                pass
    
        if not os.path.exists(img):
            try: 
                DownloaderClass(url,img)
            except:
                os.remove(img)
                return
    
        okFlash = False
    
        time.sleep(1)
        dialog = xbmcgui.Dialog()
        if 'M3' in description:
            if dialog.yesno("What Do You Want To Do ?", '','Do You Want To Remove Checks or Flash',"",'FLASH','R/CHECKS'):
                import checks
                okFlash = checks.remove(filename, DEBUG_HUB) 
            else:
                okFlash = True
                os.rename(img, os.path.join(path, 'update.img'))
        else:
            okFlash = True
            os.rename(img, os.path.join(path, 'update.img'))
        if okFlash:   
            if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
                ADDON.setSetting('storage','true')
                doRecovery()
    else:
        print '####################### TLBB DOWNLOADING '+name+' ############################'
        url = str(url)
        try:
            name = name.split(' [')[0]
        except:
            pass
        dialog = xbmcgui.Dialog()
        if linux_download == '':
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
            ADDON.openSettings()
        filename = 'update.zip'
        path     = xbmc.translatePath(os.path.join(linux_download,''))
        img      = os.path.join(path, filename)
    
        if not DEBUG_HUB:
            try:
                os.remove(img)
            except:
                pass
    
        if not os.path.exists(img):
            try: 
                DownloaderClass(url,img)
            except:
                os.remove(img)
                return
    
    
        time.sleep(1)
        dialog = xbmcgui.Dialog()
        if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):
            ADDON.setSetting('storage','true')
            doRecovery()
                
                    
                
def install_linux_official_image(name,url,iconimage):
    name = str(name).replace('Date: ','Pivos_').replace('/','_')
    dialog = xbmcgui.Dialog()
    if linux_download == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMC TEAM", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set","Its In Hub Settings")
        ADDON.openSettings()
    filename = 'official.img'
    path     = xbmc.translatePath(os.path.join(linux_download,''))
    img      = os.path.join(path, filename)
        
    if not DEBUG_HUB:
        try:
            os.remove(img)
        except:
            pass

    if not os.path.exists(img):
        try: 
            if '.zip' in url:
                DownloaderClass(url,img)
                dp = xbmcgui.DialogProgress()
                dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
                extract.all(path,addonfolder,dp)

        except:
            os.remove(img)
            return

    okFlash = False

    time.sleep(1)
    dialog = xbmcgui.Dialog()
    if 'M3' in description:
        if dialog.yesno("What Do You Want To Do ?", '','Do You Want To Remove Checks or Flash',"",'FLASH','R/CHECKS'):
            import checks
            okFlash = checks.remove(filename, DEBUG_HUB) 
        else:
            okFlash = True
            os.rename(img, os.path.join(path, 'update.img'))
    else:
        okFlash = True
        os.rename(img, os.path.join(path, 'update.img'))
    if okFlash:   
        if dialog.yesno("[B][COLOR red]WARNING !!![/B][/COLOR]", '[B]ARE YOU SURE YOU KNOW WHAT THIS DOES !?![/B]','', "[B][COLOR red]     THIS WILL FLASH TO THIS LINUX IMAGE !!![/B][/COLOR]"):

            doRecovery()
            
           
def myversion():
   log_path = xbmc.translatePath('special://logpath')
   log = os.path.join(log_path, 'xbmc.log')
   logfile = open(log, 'r').read()
   match=re.compile('Starting XBMC \(.+? Git:(.+?)\)').findall(logfile)
   result=match[0]
   try:
       regex=re.compile('(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)(.+?)-.+?')
       match=regex.search(result)
       date='%s%s/%s%s/%s%s'%(match.group(7),match.group(8),match.group(5),match.group(6),match.group(3),match.group(4))
   except:
       date='Unknown'
   return date
   
  
############################################################        INSTALL ALL REPOS        ###############################################################
def allrepos(name,url):  
    print '############################################################        INSTALL ALL REPOS        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    import downloader
    link=OPEN_URL('http://fusion.Maguinho/video/repositories/')
    link=link.split('Parent Directory')[1]
    match=re.compile('href="((?!.+adult).+?)">').findall(link)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance","Downloading ",'', 'Please Wait')
    for name in match:
        url='http://fusion.Maguinho/video/repositories/'+name
        lib=os.path.join(path, name)
        name='[COLOR yellow]%s[/COLOR]'%name
        dp.update(0,"Downloading ",name, 'Please Wait')
        downloader.download(url, lib, dp)
        time.sleep(.5)
        dp.update(0, "Extracting ",name,"Please Wait")
        extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "Please Reboot To Take", "Effect   [COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
def removeanything(url):   
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove", '', "Do you want to Remove"):
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(url)
        xbmc.executebuiltin('Container.Refresh')         
    
    
############################################################        PLAYERCORE          ###############################################################    
    
    
def playercore(url): 
    print '############################################################        PLAYERCORE          ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/userdata',''))
    playercore=os.path.join(path, 'playercorefactory.xml')
    try:
        os.remove(playercore)
        print '========= REMOVING    '+str(playercore)+'     =========================='
    except:
        pass
    link=OPEN_URL(url)
    a = open(playercore,"w") 
    a.write(link)
    a.close()
    print '========= WRITING NEW    '+str(playercore)+'     =========================='
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "Please Enable Hardware Acceleration In Settings",'Please Reboot XBMC',"          [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        HULU FIX          ###############################################################    
def hulufix(url):  
    print '############################################################        HULU FIX        ###############################################################'
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib=os.path.join(path, 'script.module.cryptopy.zip')
    DownloaderClass(url,lib)
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
    time.sleep(2)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Phantom Dev", "Please Reboot To Take", "Effect   [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    
    
############################################################        ADD 7 ICONS          ###############################################################    
    
def add7icons(url): 
    dialog = xbmcgui.Dialog()
    print '############################################################        ADD 7 ICONS          ###############################################################'
    if dialog.yesno("Phantom Dev","" , "Add 7 Icons Or Restore To 5",'','Restore 5','Add 7'):
        url = base+'tweaks/confluence_7.zip'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'confluence_7.zip')
        DownloaderClass(url,lib)
        time.sleep(3)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        dp = xbmcgui.DialogProgress()
        dp.create("XBMCHUB...Maintenance", "Extracting Zip Please Wait")
        extract.all(lib,addonfolder,dp)
        ADDON.setSetting('add7','false')
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "Please Reboot To Take", "Effect   [COLOR yellow]Brought To You By Maguinho[/COLOR]")
    else:
        confluence = xbmc.translatePath(os.path.join('special://home/addons','skin.confluence'))
        if ADDON.getSetting('add7')=='false':
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Run Me Again After Reboot To Completely Clean", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
            ADDON.setSetting('add7','true')
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phantom Dev", "Great You Are Completely Clean Now", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
            ADDON.setSetting('add7','false')
        for root, dirs, files in os.walk(confluence):
            try:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            except:
                pass
        try:
            os.rmdir(confluence)
        except:
            pass
            
############################################################       WALLPAPER         ###############################################################    
def wallpaper(name,url,iconimage):
    link=OPEN_URL(wallurl)
    match=re.compile('<a href="(.+?)" title=".+?">(.+?)</a>  <small>(.+?)</small').findall(link)
    for url,name,amount in match:
            url=wallurl+url
            name= name+' '+amount
            addDir(name,url,45,iconimage,base+'images/fanart/gettingstarted.jpg','')
    

def wallpaper2(name,url,iconimage):
    link=OPEN_URL(url)
    match=re.compile('href="(.+?)" title=".+?"><p align="center">(.+?)</p>').findall(link)
    if not match:
            wallpaper3(name,url,iconimage)
    elif len(match)<2:
            addDir(name,url,46,iconimage,base+'images/fanart/gettingstarted.jpg','')
    else:
        for url,name in match:
            url=wallurl+url
            addDir(name,url,46,iconimage,base+'images/fanart/gettingstarted.jpg','')


def wallpaper3(name,url,iconimage):    
    link=OPEN_URL(url)
    match=re.compile('href="(.+?)" title=".+?">\n.+?img src="(.+?)" alt="(.+?) HD Wide').findall(link)
    for url,iconimage,name in match:
            url=wallurl+url
            addDir(name,url,47,iconimage,base+'images/fanart/gettingstarted.jpg','')
    if 'Next ' in link:
        try:
            link=link.split('Previous<')[1]
            link=link.split('>Next')[0]
            match=re.compile('href="(.+?)"').findall(link)
            pos=int(len(match))-1
            url=wallurl+str(match[pos])
            name= 'Next Page >>'
            addDir(name,url,46,base+'images/nextpage.jpg',base+'images/fanart/gettingstarted.jpg','')
        except:
            pass
    setView('movies', 'MAIN')

def wallpaper_download(name,url,iconimage):  
    link=OPEN_URL(url)
    if ADDON.getSetting('download_wallpaper')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "A New Window Will Now Open For You To In Put", "Download Path")
        ADDON.openSettings()
    size='1920x1080'
    r='<a target="_self" href="(.+?)" title=".+?">%s</a>'%(size)
    match=re.compile(r).findall(link)
    url= wallurl+match[0] 
    path = xbmc.translatePath(os.path.join(ADDON.getSetting('download_wallpaper'),''))
    img=os.path.join(path, name+'.jpg')
    try:
        DownloaderClass(url,img, True)    
    except Exception as e:
        try:
            os.remove(img)
        except:
            pass
        if str(e) == "Canceled":
            #you will end up here only if the user cancelled the download 
            pass
    
def hd_wallpaper(name,url,iconimage):
    link=OPEN_URL(hd_wallurl)
    match=re.compile('li style="padding-left:0px;"><a  href="(.+?)">(.+?)</a>').findall(link)
    for url,name in match:    
            url=hd_wallurl+url
            name= name
            addDir(name,url,50,iconimage,base+'images/fanart/gettingstarted.jpg','')
    

def hd_wallpaper2(name,url,iconimage):
    url=url.replace('pageSub','page')
    print'######################## '+url
    link=OPEN_URL(url)
    split=link.split('class="rss-image"')[1]
    match=re.compile('href="(.+?)"><p>(.+?)</p><em>.+?</em><img src="(.+?)"').findall(split)
    for url,name,iconimage in match:
        url=hd_wallurl+'/wallpapers/'+iconimage.replace('/thumbs/','').replace('-t1','-1920x1080')
        addDir(name,url,51,hd_wallurl+iconimage,base+'images/fanart/gettingstarted.jpg','')
    if 'Next ' in link:
        try:
            if '/pageSub/' in link:
                link=link.split('Previous<')[2]
            else:
                link=link.split('Previous<')[1]
            link=link.split('>Next')[0]
            match=re.compile('href="(.+?)"').findall(link)
            pos=int(len(match))-1
            url=hd_wallurl+str(match[pos])
            name= 'Next Page >>'
            addDir(name,url,50,base+'images/nextpage.jpg',base+'images/fanart/gettingstarted.jpg','')
        except:
            pass
    setView('movies', 'MAIN')

def hd_wallpaper_download(name,url,iconimage):   

    link=OPEN_URL(url)
    if ADDON.getSetting('download_wallpaper')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "A New Window Will Now Open For You To In Put", "Download Path")
        ADDON.openSettings()
    print '==================================    '+url
    path = xbmc.translatePath(os.path.join(ADDON.getSetting('download_wallpaper'),''))
    img=os.path.join(path, name+'.jpg')
    print '==================================    '+img
    try:    
        DownloaderClass(url,img)
    except:    
        DownloaderClass(url.replace('1920x1080','1280x720'),img)
    
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


class HUB( xbmcgui.WindowXMLDialog ): # The call MUST be below the xbmcplugin.endOfDirectory(int(sys.argv[1])) or the dialog box will be visible over the pop-up.
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()

             
def pop():# Added Close_time for window auto-close length.....
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    elif xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    
    popup.doModal()
    del popup
                
def checkdate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update


def check_popup():

    threshold  = 120

    now   = datetime.datetime.today()
    prev  = checkdate(ADDON.getSetting('pop_time'))
    delta = now - prev
    nDays = delta.days

    doUpdate = (nDays > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('pop_time', str(now).split('.')[0])
    pop()
     
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if (mode==13) or (mode==9) or (mode==10)or (mode==11)or (mode==36)or (mode==38)or (mode==6)or (mode==16)or (mode==25)or (mode==33)or (mode==34)or (mode==44)or (mode==45)or (mode==46)or (mode==42)or (mode==48)or (mode==49)or (mode==50)or (mode==55) or (mode==58) or (mode ==None):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def addLink(name,url,iconimage,description,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("Fanart_Image",fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 

def routine_insp():
    check_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
    settings_path = os.path.join(xbmc.translatePath('special://home/userdata'), 'addon_data')
    packages_path = os.path.join(xbmc.translatePath('special://home/addons'), 'packages')

    directories = os.listdir(check_path)
    for lol in directories:
        if lol == "plugin.video.hubmaintenance":
            try:
                urld = os.path.join(check_path, lol)
                shutil.rmtree(urld)
                urld = os.path.join(settings_path, lol)
                shutil.rmtree(urld)
            except: pass

routine_insp()
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        DeleteCrashLogs(url)
        
elif mode==2:
        DeletePackages(url)

elif mode==3:
        deletecachefiles(url)
        
elif mode==4:
        OneChannel(url)
        
elif mode==5:
        advancexml(url,name)
        
elif mode==6:
        joystick(url)
        
elif mode==7:
        print ""+url +iconimage
        malformed(url)
        
elif mode==8:
        onechanneldb(url)
        
elif mode==9:
        maintenance(url)
        
elif mode==10:
        fixesdir(url)
        
elif mode==11:
        tweaksdir(url)
        
elif mode==12:
        lib(url)
        
elif mode==13:
        howtos(url,fanart)
        
elif mode==14:
        deleteadvancexml(url)
        
elif mode==15:
        uploadlog(url)
        
elif mode==16:
        fastcoloreden(url,iconimage)
        
elif mode==17:
        downloadanything(url,name)
        
elif mode==18:
        FusionInstaller(url)
                
elif mode==19:
        doRecovery(url)
        
elif mode==20:
        onechannelreboot(url)
        
elif mode==21:
        xbmchubrepo(url)
        
elif mode==22:
        removemikey(url)
        
elif mode==23:
        restore(url)
elif mode==24:
        captcha(url)
elif mode==25:
        findaddon(url,name)
elif mode==26:
        removeanything(url)
elif mode==27:
        subtitle(url)
elif mode==28:
        gui(url)
elif mode==29:
        checkadvancexml(url,name)
elif mode==30:
        youtubefix(name)
elif mode==31:
        bbcfix(name)
elif mode==33:
        pivos_image(name,url,iconimage)
elif mode==34:
        install_linux_official_image(name,url,iconimage)
elif mode==35:
        allrepos(name,url)
elif mode==36:
        allandroid(url)
        
elif mode==37:
        playercore(url)
        
elif mode==38:
        alllinux(url)
        
elif mode==39:
        hulufix(url)
elif mode==40:
        add7icons(url)
elif mode==41:
        install_linux_nightlies(name,url,iconimage,description)
elif mode==42:
        toys4me(name,url,iconimage)
elif mode==43:
        toys4medownload(name,url,iconimage)
        
elif mode==44:
        wallpaper(name,url,iconimage)
        
elif mode==45:
        wallpaper2(name,url,iconimage)
elif mode==46:
        wallpaper3(name,url,iconimage)
elif mode==47:
        wallpaper_download(name,url,iconimage)
elif mode==48:
        wallpaper_catergories()
        
elif mode==49:
        hd_wallpaper(name,url,iconimage)
elif mode==50:
        hd_wallpaper2(name,url,iconimage)
elif mode==51:
        hd_wallpaper_download(name,url,iconimage)
        
elif mode==52:
        mygica_flash(name,url,iconimage)
        
elif mode==53:
        geek_j1nx_image(name,url,iconimage)
        
elif mode==54:
        move_to_storage(name,url,iconimage)
        
elif mode==55:
        top_secret()
        
elif mode==56:
        downloadurlresolver(name)
        
elif mode==57:
        fixurlresolver(name)
        
elif mode==58:
        homeicons(url)
        
elif mode==59:
        onechanneldown(url)
elif mode==61:
        restoreadvancexml(url)
        
elif mode==62:
        homeicons2(name)
        
elif mode==63:
        onechannelsub(url)
        
elif mode==2000:
        pop()
        
elif mode==2001:
        PLAY_STREAM(name,url,iconimage,description)

elif mode==111:
        import maintenance
        maintenance.doMaintenance(1)
        dialog = xbmcgui.Dialog()
        dialog.ok("Phantom Dev", "All Done Thank You", "[COLOR yellow]Brought To You By Maguinho[/COLOR]")
        
elif mode == NAVIX_JD:
        navix.addJDownloader(base)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
check_popup()

