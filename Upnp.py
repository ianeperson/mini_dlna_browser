'''

mini_dlna_browser - a dlna/upnp browser with a basic GUI implemented in Python

Copyright (C) 2021  Ian Eperson - ian.eperson@dedf.co.uk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

Created on 25 Feb 2021

'''
from requests import post
from re import compile
from os import system

url = 'http://192.168.1.1:8200'                 
header = {'User-Agent' : 'gupnp-av-cp GUPnP/0.18.1 DLNADOC/1.50', 'Accept' : '','Content-Type' : 'text/xml; charset="utf-8"','Accept-Language' : 'en-us;q=1, en;q=0.5','Accept-Encoding' : 'gzip'}

containerheader = '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><ObjectID>_PARENTID_</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter>@childCount</Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria></u:Browse></s:Body></s:Envelope>'
itemheader = '<?xml version="1.0" encoding="UTF-8" ?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><s:Body><u:Search xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><ContainerID>0</ContainerID><SearchCriteria>(@id contains "_ITEMID_")</SearchCriteria><Filter>*</Filter><StartingIndex>0</StartingIndex><RequestedCount>100</RequestedCount><SortCriteria>+dc:title</SortCriteria></u:Search></s:Body></s:Envelope>'

class Upnp():
    
    def unescape(self, s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&amp;", "&") # this has to be last
        return s

    def Search(self, parent):
        # add the SOAP action
        header['SOAPAction'] = '"urn:schemas-upnp-org:service:ContentDirectory:1#Browse"'
        # inject the item number we want and execute the request
        r = post(url, data=containerheader.replace("_PARENTID_",parent), headers=header)
        p = compile(r'<(item|container)\sid="(.*?)"\s.*?title>(.*?)</dc') # parse for the things we are interested in
        return (p.findall(self.unescape(r.content.decode('utf-8')))) # return the type. id,name tuple
    
    def FindandPlay(self, item):
        # add the SOAP action
        header['SOAPAction'] = '"urn:schemas-upnp-org:service:ContentDirectory:1#Search"'
        # inject the item number we want and execute the request
        r = post(url, data=itemheader.replace("_ITEMID_", item), headers=header)
        p = compile(r'<item id="(.*?)".*?<res.*?>(.*?)</res>') # parse for the things we are interested in
        for e in p.findall(self.unescape(r.content.decode('utf-8'))):
            if (e[0].startswith(item)): # we want the item or all of the direct children
                system('mplayer -quiet -vo x11 ' + e[1])
