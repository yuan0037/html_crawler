import sys
import urllib2

from urlparse import urlparse
from urlparse import urljoin
from HTMLParser import HTMLParser
from wpwcaDB import wpwcaDB

import re

#a class from HTMLParser to parse the HTML content
               
class MyHTMLParserForAHref(HTMLParser):
  

    def __init__(self, level, url, maxLevel):        
        HTMLParser.__init__(self)
        self.myLevel = level
        self.listOfURL=[]
        self.myURL=url
        self.myMaxLevel=maxLevel
        self.inBody=False
        self.occurrenceOfWord=0
        
    @property
    def myURL(self):  
        return self._myURL

    @myURL.setter
    def myURL(self, value):
        self._myURL = value

    @myURL.deleter
    def myURL(self):
        del self._myURL
  
                   
    @property
    def myLevel(self):  
        return self._myLevel

    @myLevel.setter
    def myLevel(self, value):
        self._myLevel = value

    @myLevel.deleter
    def myLevel(self):
        del self._myLevel
        
    @property
    def myMaxLevel(self):  
        return self._myMaxLevel

    @myMaxLevel.setter
    def myMaxLevel(self, value):
        self._myMaxLevel = value

    @myMaxLevel.deleter
    def myMaxLevel(self):
        del self._myMaxLevel
            
    #detect if the link is to a certain type of file that should be excluded
    def shouldExcludeByFileExt(self, url):
        excludeFileExt = [".mp3", ".jpg", ".zip", ".rar", ".exe", ".gif", ".bmp", ".png", ".swf", ".xml", ".js", ".css", ".svg"]
        try: 
            filename = url.split('/')[-1].split('.')[0]
            #print filename
            file_ext = '.'+url.split('.')[-1]
            #print "file ext is :", file_ext
            if (not any(file_ext.lower() in excludeExtName for excludeExtName in excludeFileExt)) :
                return False
            else:
                print "excluded ", url
                return True
        except NameError:
            #print "could not split either by '/' or by '.'"
            return False
                            
# function to handle an opening tag in the doc
    def handle_starttag(self, tag, attrs):
        if (tag.lower() == "body"):
            self.inBody = True   

        if (self.myLevel<self.myMaxLevel):
            if tag == "a":
                #metacount += 1
               # Check the list of defined attributes.
                for name, value in attrs:
                    # If it is ahref
                    if name == "href":
                        linkFound="".join(value)
                        #exclude same page anchor link
                        #like <a href="#abc">go to abc</a>
                        if (not linkFound.startswith("#")):
                            #when the link is a relative link
                            #something like <a href="../../">some text</a>
                            #or <a href="/subdirectory/abasd.html">some text</a>
                            if ((linkFound.startswith("/")) or (linkFound.startswith("."))):
                                absoluteURL=urljoin(self.myURL, linkFound)
                                if (self.shouldExcludeByFileExt(absoluteURL)==False):
                                    if (not absoluteURL in self.listOfURL):
                                        #print "added", absoluteURL
                                        self.listOfURL.append(absoluteURL)
                            elif (linkFound.startswith("http")):
                                #when the link is an absolute link, http or https
                                if (self.shouldExcludeByFileExt(linkFound)==False):
                                    if (not linkFound in self.listOfURL):
                                        self.listOfURL.append(linkFound)  
                            else:
                                    print "ignored a link to :" , linkFound
                                    
    def handle_endtag(self, tag):
        if (tag.lower() == "body"):
            self.inBody = False
            #print "total count = ", self.occurrenceOfWord   
            
    #function to handle character and text data (tag contents)
    def handle_data(self, data):
        #global wordCount
          #print "Encountered some data:", data
        if (self.inBody==True):
            for w in re.findall(r"\w+", data):
                  if (w.lower()==sys.argv[2].lower()):
                      self.occurrenceOfWord += 1   