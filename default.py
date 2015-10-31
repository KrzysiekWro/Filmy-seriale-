# -*- coding: utf-8 -*-
__scriptname__ = "Alltube"
__author__ = "detoyy"
__url__ = ""
__scriptid__ = "plugin.video.alltube"
__credits__ = "Bunkford"
__version__ = "0.0.1"

import sys,os
import urllib,urllib2,re,urlresolver
from t0mm0.common.addon import Addon
from bs4 import BeautifulSoup
import requests


try: import xbmc,xbmcplugin,xbmcgui,xbmcaddon
except:
     xbmc_imported = False
else:
     xbmc_imported = True


# global constants
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


#get path to me
addon = xbmcaddon.Addon()
alltube=addon.getAddonInfo('path')

_PLT = Addon('plugin.video.alltube', sys.argv)


def xbmcpath(path,filename):
     translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
     return translatedpath

def _get_keyboard(default="", heading="", hidden=False):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard(default, heading, hidden)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
                return unicode(keyboard.getText(), "utf-8")
        return default

def SEARCHVIDEOS(url):
        searchUrl = 'http://alltube.tv/szukaj'
        vq = _get_keyboard(heading="Enter the query")
        # if blank or the user cancelled the keyboard, return
        if (not vq): return False, 0
        # we need to set the title to our query
        title = urllib.quote_plus(vq)
        INDEX3(searchUrl,title)

def CDA(url):
    r = requests.get(url)
    match = re.compile("url: 'http://(.+?)',").findall(r.text)
    if match:
      videourl = "http://"+match[0]
      print videourl + ' videourl'
      return videourl
    else :
         return ""
    match = re.compile("file: 'http://(.+?)',").findall(r.text)
    if match:
       videourl = "http://"+match[0]
       print videourl+ ' videourl'
       return videourl
    else :
         return ""
    match = re.compile('data-urlhost="http://(.+?)"').findall(r.text)
    if match:
        videourl = "http://www."+match[0]
        print videourl+ ' videourl'
        return videourl
    else :
         return ""

def addDir(name,url,mode,iconimage,letter,page):
         u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)  + "&letter=" +urllib.quote_plus(letter)+"&page=" + str(page)   
         ok = True
         liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage)                               
         liz.setInfo(type="Video", infoLabels={ "Title": name })
         ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
         return ok

     
def CATEGORIES():
        addDir('Filmy najnowsze','http://alltube.tv/filmy-online/strona[1]+',6,'','',1)
        addDir('Seriale najnowsze','http://alltube.tv/seriale-online/1',9,'','',1)
        addDir('Kids','http://alltube.tv/filmy-online/kategoria[5]+strona[1]',2,'','',1)
        addDir('Szukaj filmu/serialu','http://alltube.tv/szukaj',3,'','','')
        addDir('Filmy wg rodzaju','http://alltube.tv/filmy-online/',5,'','',1)
        addDir('Filmy wg wersji jezykowej','http://alltube.tv/filmy-online/',7,'','',1)
        addDir('Filmy wg roku produkcji','http://alltube.tv/filmy-online/',8,'','',1)
        addDir('Spis seriali','http://alltube.tv/seriale-online/',10,'','',1)

        

def INDEX2(url,page):
        nr_strony = str(page)
        page=page+1
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')
        divTag = soup.find_all("div", {"class":"col-xs-3 col-md-2"})
        for tag in divTag:
             print ''
             tytul = tag.find("h3")
             tytul = tytul.text
             link = tag.find('a')
             fullLink = link.get('href').strip()
             imglinks = tag.find_all('img')
             for imglink in imglinks:
                  imgfullLink = imglink.get('src').strip()
             addDir(tytul.encode('UTF-8')+' ',fullLink.encode('UTF-8'),4,imgfullLink,'','')
        print url + ' '+nr_strony #http://alltube.tv/filmy-online/kategoria[5]+strona[1] 1
        won = 'strona['+nr_strony+']' 
        print won + ' won to'  #strona[1]
        if  won in url:
             url = url.replace(won,'')
        else:
             print ' nie ma tego'
        #print nexturl + ' dodac ' + 'strona['+str(page)+']+'
        addDir('Next page -----> str.'+str(page),url+'strona['+str(page)+']+',2,'','',page)  

def INDEX3(url,query):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://alltube.tv',
        'Accept-Encoding':'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        print query + ' query'
        content = requests.post(url, "search="+query, headers=headers)
        #print content.text.encode('utf-8')
        #return content.text
        match = re.compile('<a href="(.+?)">(.+?)</a>').findall(content.text)
        for url,name in match:
             if "/serial/" in url:
                  print url + ' seriall'
                  addDir(name.encode('UTF-8')+'[COLOR yellow] - Serial[/COLOR]',url,12,'','',1)
             else:
                  addDir(name.encode('UTF-8'),url,4,'','',1)

def INDEX4(url,page):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')

        divTag = soup.find_all("ul", {"id":"filter-category"})
        #print divTag
        for ul in divTag:
                match=re.compile('<li data-id="(.+?)">(.+?)</li>').findall(str(ul))
                for kategoria_id,nazwa_kategorii in match:
                        #print kategoria_id+' '+nazwa_kategorii
                        addDir(nazwa_kategorii,url+'kategoria['+kategoria_id+']+strona['+str(page)+']',6,'','',str(page))

def INDEX5(url,page):
        nr_strony = str(page)
        page=page+1
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')
        tags = soup.find_all("div", {"class":"col-xs-12 col-md-6"})
        for tag in tags:
                  #print '============================================================\n'
                  #print tag
                  divTags1 = tag.find_all("div", {"class":"border-box clearfix"})
                  for tag in divTags1:
                      divTags2 = tag.find_all("div", {"class":"col-xs-4 col-md-4 col-lg-3 poster-parent"})
                      divTags3 = tag.find_all("div", {"class":"col-xs-8 col-md-8 col-lg-9"})    #tytul i opis
                      links = tag.find_all('a')
                      wersja = ""
                      for tag in divTags3:       
                           tytul = tag.find("h3")
                           tytul = tytul.text
                           print tytul.encode('UTF-8')
                      for tag in divTags2:
                          imglinks = tag.find_all('img')
                          for imglink in imglinks:
                             imgfullLink = imglink.get('src').strip()
                             print imgfullLink

                      for link in links:
                           fullLink = link.get('href').strip()
                           print fullLink
                           addDir(tytul.encode('UTF-8')+' '+wersja,fullLink.encode('UTF-8'),4,imgfullLink,'','')
        #http://alltube.tv/filmy-online/strona[1]+
        #http://alltube.tv/filmy-online/kategoria[1]+strona[1]+
        print url + ' '+nr_strony
        won = 'strona['+nr_strony+']'
        print won + ' won to'
        if  won in url:
             url = url.replace(won,'')
        else:
             print ' nie ma tego'
        #print nexturl + ' dodac ' + 'strona['+str(page)+']+'
        addDir('Next page -----> str.'+str(page),url+'strona['+str(page)+']+',6,'','',page)          


def INDEX6(url,page):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')

        divTag = soup.find_all("ul", {"id":"filter-version"})
        #print divTag
        for ul in divTag:
                match=re.compile('<li data-id="(.+?)">(.+?)</li>').findall(str(ul))
                for kategoria_id,nazwa_kategorii in match:
                        print kategoria_id+' '+nazwa_kategorii
                        url_kategoria_id = url+'wersja['+kategoria_id+']+strona[1]'
                        print "kategoriaa "+url_kategoria_id
                        addDir(nazwa_kategorii.encode('UTF-8'),url_kategoria_id.encode('UTF-8'),6,'','',str(page))

def INDEX7(url,page):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')

        divTag = soup.find_all("ul", {"id":"filter-year"})
        #print divTag
        for ul in divTag:
                match=re.compile('<li data-id="(.+?)">(.+?)</li>').findall(str(ul))
                for kategoria_id,nazwa_kategorii in match:
                        #print kategoria_id+' '+nazwa_kategorii
                        addDir(nazwa_kategorii,url+'rok['+kategoria_id+']+strona[1]',6,'','',str(page))

def INDEX8_SERIALE(url,page):
        nr_str = str(page)
        page= page+1
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')

        #print(soup.prettify())
        #print(soup.body)
        divTag = soup.find_all("div",{"class":"col-sm-9"})
        #print divTag
        for tag in divTag:
                 divTags2 = tag.find_all("div", {"class":"series"})
      
                 for tag in divTags2:
                     imglinks = tag.find_all('img')
                     for imglink in imglinks:
                        imgfullLink = imglink.get('src').strip()
                        #print imgfullLink
                     links = tag.find_all('a')
                     wersja = ""
                     for link in links:
                         fullLink = link.get('href').strip()
                     tytul = tag.find('h3')
                     tytul = tytul.text
                     addDir(tytul.encode('UTF-8')+' '+wersja,fullLink,12,imgfullLink,'',page)
        nexturl=url.replace('/'+nr_str,'')
        #http://alltube.tv/seriale-online/1
        addDir('Next page -----> str.'+str(page),nexturl+'/'+str(page),9,'','',page)  

def SERIALE_SPIS(url,page):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')
        divTag = soup.find_all("li", {"class":"letter"})
        for tag in divTag:
               letter = tag.text.encode('UTF-8')  
               addDir(letter,url,11,'',letter,str(page))

def INDEX11(url,letter,page):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile('<li data-letter="'+str(letter)+'"><a href="(.+?)">(.+?)</a></li>').findall(link)
        for adres,tytul in match:
               addDir(tytul,adres.encode('UTF-8'),12,'','',str(page))

def INDEX12(url,page):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, 'html.parser')
        divTag = soup.find_all("ul", {"class":"episode-list"})
        for tag in divTag:
             print ''
             divTags2 = tag.find_all("li", {"class":"episode"})
             for tag in divTags2:
                     links = tag.find_all('a')
                     for link in links:
                             fullLink = link.get('href').strip()
                             name = re.compile('odcinek-(.+?)-sezon-',re.I).findall(fullLink)
                             if '/' in name[0]:
                                     odcinek,reszta = name[0].split('/',1)
                             else:
                                     odcinek = name[0]
                             match =re.compile('-sezon-(.+?)/',re.I).findall(fullLink) 
                             addDir('[COLOR  yellow]Sezon '+match[0]+'[/COLOR] [COLOR white]odc. '+odcinek+'[/COLOR]',fullLink,4,'','',str(page))
             
        

                        
def VIDEOLINKS(url,name):
        name = name.replace('[COLOR green]Lektor','')
        name = name.replace('[COLOR orange]Napisy','')
        name = name.replace('[/COLOR]','')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        #print link
        response.close()
        match=re.compile('<td class="text-center"><a class="watch" data-urlhost="(.+?)" data-iframe="(.+?)" data-version="(.+?)" data-size="width: (.+?)px; height: (.+?)px;" href="#!">Oglądaj</a></td>').findall(link)
        for url,cos,lang,width,hight in match:
                 print url
                 match= re.compile('http:\/\/(.+?)\/').findall(url)
                 for host in match:
                     host = host.replace('embed.','')
                     host = host.replace('www.','')
                     if "openload" in host:
                          print "cosco " + host
                          media_url = url.replace("http://openload.co/video/","https://openload.co/f/")
                          media_url = urlresolver.resolve(media_url)
                          print media_url
                     elif "cda" in host:
                         media_url = CDA(url)
<<<<<<< HEAD
                         media_url = media_url+'|referer=http://static.cda.pl/flowplayer/flash/flowplayer.commercial-3.2.18.swf'
                     elif "streamin" in host:
                          media_url = url.replace("video/","")             
=======
                         media_url = media_url+ '|Cookie="PHPSESSID=1&Referer=http://static.cda.pl/player5.9/player.swf'
>>>>>>> origin/master
                     else:                  
                         media_url = urlresolver.resolve(url)
                 #print media_url
                 #print lang           

                 addLink(name+'[COLOR blue] '+lang+'[/COLOR]( '+host+' )',media_url,'http://alltube.tv/static/host/play.png')
               
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

def addLink(name,url,iconimage):
        ok=True
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', name)
        win.setProperty('1ch.playing.year', '2069')
        #win.setProperty('pltv.playing.imdb', )
        win.setProperty('1ch.playing.season', name[2:3])
        win.setProperty('1ch.playing.episode', name[5:6])
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        #print 'totu'+str(url)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
        return ok


    
params=get_params()
url=None
name=None
mode=None
season=None

try:
        letter=urllib.unquote_plus(params["letter"])
except:
        pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        pass

print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "Season: "+str(season)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print "hmmm "+url
        INDEX(url)

elif mode==2:
        #print ""+url
        INDEX2(url,page)
        
elif mode == 3:
        print mode
        SEARCHVIDEOS(url)
            
elif mode==4:
        #print ""+url
        VIDEOLINKS(url,name)

elif mode==5:
        #print ""+url
        INDEX4(url,page)

elif mode==6:
        #print ""+url
        INDEX5(url,page)
        
elif mode==7:
        #print ""+url
        INDEX6(url,page)

elif mode==8:
        #print ""+url
        INDEX7(url,page)

elif mode==9:
        #print ""+url
        INDEX8_SERIALE(url,page)

elif mode==10:
        #print ""+url
        SERIALE_SPIS(url,page)

elif mode==11:
        #print ""+url
        INDEX11(url,letter,page)

elif mode==12:
        #print ""+url
        INDEX12(url,page)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
