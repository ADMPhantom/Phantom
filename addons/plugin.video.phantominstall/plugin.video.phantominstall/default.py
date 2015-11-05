import xbmc , xbmcaddon , xbmcgui , xbmcplugin , os
import shutil
import urllib2 , urllib
import re
import extract
import downloader
import time
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
o0OO00 = xbmcaddon . Addon ( id = 'plugin.video.phantominstall' )
if 78 - 78: i11i . oOooOoO0Oo0O
def iI1 ( url ) :
 i1I11i = urllib2 . Request ( url )
 i1I11i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 OoOoOO00 = urllib2 . urlopen ( i1I11i )
 I11i = OoOoOO00 . read ( )
 OoOoOO00 . close ( )
 return I11i
 if 64 - 64: OOooo000oo0 . i1 * ii1IiI1i % IIIiiIIii
 if 8 - 8: Oo / iII11iiIII111 % iiiIIii1I1Ii . O00oOoOoO0o0O
 if 43 - 43: Oo0 * OO - oooO0oo0oOOOO - ooO0oo0oO0 - i111I * OoooooooOO
def O0Oo0oO0o ( ) :
 iiI1iIiI = os . path . join ( xbmc . translatePath ( 'special://home' ) , 'userdata' , 'sources.xml' )
 if not os . path . exists ( iiI1iIiI ) :
  OOo = open ( iiI1iIiI , mode = 'w' )
  OOo . write ( '<sources><files><source><name>.Phantom Installer</name><path pathversion="1">http://subversion.assembla.com/svn/xbmc</path></source></files></sources>' )
  OOo . close ( )
  return
  if 1 - 1: i11i - Oo % i11iIiiIii + oooO0oo0oOOOO . ooO0oo0oO0
 OOo = open ( iiI1iIiI , mode = 'r' )
 str = OOo . read ( )
 OOo . close ( )
 if 'http://subversion.assembla.com/svn/xbmc' in str :
  str = str . replace ( 'xbmctalk.com' , 'phantom.com' )
  OOo = open ( iiI1iIiI , mode = 'w' )
  OOo . write ( str )
  OOo . close ( )
  if 55 - 55: iIii1I11I1II1 - oOooOoO0Oo0O . Oo0 * oooO0oo0oOOOO * i1IIi / iIii1I11I1II1
 if not 'http://subversion.assembla.com/svn/xbmc' in str :
  if '</files>' in str :
   str = str . replace ( '</files>' , '<source><name>.Phantom Installer</name><path pathversion="1">http://subversion.assembla.com/svn/xbmc</path></source></files>' )
   OOo = open ( iiI1iIiI , mode = 'w' )
   OOo . write ( str )
   OOo . close ( )
  else :
   str = str . replace ( '</sources>' , '<files><source><name>.Phantom Installer</name><path pathversion="1">http://subversion.assembla.com/svn/xbmc</path></source></files></sources>' )
   OOo = open ( iiI1iIiI , mode = 'w' )
   OOo . write ( str )
   OOo . close ( )
   if 79 - 79: iII11iiIII111 + ooO0oo0oO0 . i111I * oooO0oo0oOOOO % O00oOoOoO0o0O . oOooOoO0Oo0O
   if 94 - 94: OO * Oo0 / oooO0oo0oOOOO . i1IIi * OO
   if 47 - 47: i1IIi % i11iIiiIii
def i1iII1I1i1i1 ( ) :
 O0Oo0oO0o ( )
 I11i = iI1 ( 'http://phantomxbmc.googlecode.com/svn/Xpert/tools/Phantom.txt' )
 i1iIIII = xbmc . getInfoLabel ( "System.ProfileName" )
 I1 = xbmc . translatePath ( os . path . join ( 'special://home' , '' ) )
 O0OoOoo00o = xbmcgui . Dialog ( )
 if O0OoOoo00o . yesno ( "Maguinho" , "WELCOME TO PHANTOM QUICK INSTALL SET UP DO YOU" , "WANT TO INSTALL ALL PLUGIN GOODIES QUICKLY" , "[COLOR green]    http://xbmcphantom.xp3.biz/ [/COLOR]" ) :
  iiI1iIiI = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  iiiI11 = xbmcgui . DialogProgress ( )
  iiiI11 . create ( "Phantom Wizard" , "Downloading " , '' , 'Please Wait' )
  OOooO = os . path . join ( iiI1iIiI , 'Phantom.zip' )
  OOoO00o = os . path . join ( iiI1iIiI , 'splash.zip' )
  try :
   os . remove ( OOooO )
  except :
   pass
  downloader . download ( 'https://phantom2.googlecode.com/svn/Phantom.zip' , OOooO , iiiI11 )
  II111iiii = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  iiiI11 . update ( 0 , "" , "Extracting Zip Please Wait" )
  print '======================================='
  print II111iiii
  print '======================================='
  extract . all ( OOooO , II111iiii , iiiI11 )
  iiiI11 . update ( 0 , "" , "Downloading" )
  downloader . download ( 'https://phantomxbmc.googlecode.com/svn/splash.zip' , OOoO00o , iiiI11 )
  iiiI11 . update ( 0 , "" , "Extracting Zip Please Wait" )
  extract . all ( OOoO00o , I1 , iiiI11 )
  xbmc . executebuiltin ( 'UpdateLocalAddons ' )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  II = re . compile ( 'plugin="(.+?)"' ) . findall ( I11i )
  for oOoOo00oOo in II :
   xbmc . executebuiltin ( "Skin.SetString(%s)" % oOoOo00oOo )
  time . sleep ( 2 )
  xbmc . executebuiltin ( 'ReloadSkin()' )
  xbmc . executebuiltin ( "LoadProfile(%s)" % i1iIIII )
  if 96 - 96: i1IIi . ii1IiI1i * iiiIIii1I1Ii % i111I
  if 60 - 60: iII11iiIII111 * IIIiiIIii % IIIiiIIii % O00oOoOoO0o0O * i11i + i1IIi
def iI1 ( url ) :
 i1I11i = urllib2 . Request ( url )
 i1I11i . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 OoOoOO00 = urllib2 . urlopen ( i1I11i )
 I11i = OoOoOO00 . read ( )
 OoOoOO00 . close ( )
 return I11i
 if 64 - 64: iII11iiIII111 - O0 / i11i / IIIiiIIii / iIii1I11I1II1
i1iII1I1i1i1 ( )
if 24 - 24: O0 % IIIiiIIii + i1IIi + ooO0oo0oO0 + Oo
if 70 - 70: OOooo000oo0 % OOooo000oo0 . oooO0oo0oOOOO % i1 * IIIiiIIii % iII11iiIII111
if 23 - 23: i11iIiiIii + oOooOoO0Oo0O
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 68 - 68: ii1IiI1i . iII11iiIII111 . i11iIiiIii
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
