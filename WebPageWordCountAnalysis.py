import sys
import urllib
import urllib.request

from wpwcaDB import wpwcaDB
from wpwcaParser import MyHTMLParserForAHref

# basic design idea for the crawler:
# first: parse base url, get word count and sub level ahref links;
# then parse each sub level links, till reach the specified maxLevel; 
# save the url, level, and word occurrences to the sqlite db
# loop the db to display the result; 


#maxLevel indicates how many levels you want to crawl
maxLevel=1
currentLevel=0;

#generalListOfURL keeps a list of URLs that has been parsed
generalListOfURL=[]
db=None


                    
    
def parseURLForAHref(url, level):
    global maxLevel
    global generalListOfURL
    global db
    print ("now start to  parse url=", url, " level=", level)
    if (level<=maxLevel):
        try:
            webUrl=urllib.request.urlopen(url)
            if (webUrl.getcode() == 200):
                data = webUrl.read()
                #initiate a parser for ahref and feed it
                
                #if the url was not parsed before; 
                if (not url in generalListOfURL):
                    generalListOfURL.append(url)
                    parser = MyHTMLParserForAHref(level, url, maxLevel)
                    parser.feed(str(data))
                    parser.close()
                    
                    #save to database the url being parsed and the level as well as the word count;
                    db._insert_fulldata_for_url(parser.myURL, parser.myLevel, parser.occurrenceOfWord)
                    
                    #parser.listOfURL keeps a list of links found on the parser's current url.
                    for item in parser.listOfURL:
                        if (level+1<=maxLevel):
                            try: 
                                #if not exceeding the max level, start
                                #recursive parsing
                                parseURLForAHref(item, parser.myLevel+1)
                            except:
                                print ("Error happened when parsing ", item)
                                pass   
                else:
                    print ("do nothing because this url was parsed before already;")
            else:
                print ("Error code: ", str(webUrl.getcode()) , url)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            print ("exception happened for ", url)   
            pass     
            
    else:
        print ("exceeding max level, do nothing")   

def main():
    # instantiate the parser and feed it some HTML
    global generalListOfURL
    global db
    global maxLevel
    
    #reset the list that keeps the urls already parsed
    generalListOfURL=[]

    db=wpwcaDB()
    #every time, we open the db, drop the table, and recreate the table when the program is launched
    db.clear()
    db.createtable()
    
    
    #set the initial level to 0
    global currentLevel
    currentLevel=0
#     print 'Number of arguments:', len(sys.argv), 'arguments.'
#     print 'Argument List:', str(sys.argv)
   
    #get the url from the arguments
    url = sys.argv[1]
    
    #start the parsing from the base url
    parseURLForAHref(url, currentLevel)
    
    #sort the table by level 
   
    print ("Final Results---------------")
    for entry in db.get_data_for_all():
        #result string formatting
        if (entry["count"]!=None):
            if (entry["level"]==0):
                print ("Base Web Page Count for ",sys.argv[2].lower(), "=", entry["count"])
            elif (entry["level"]==1):
                print ("Child Page ",entry["url"]," count for ",sys.argv[2].lower()," =", entry["count"])
            else:
                groundStr="";
                for i in range(1, entry["level"]):
                    groundStr+="Grand"
                print (groundStr, "Child Page ",entry["url"], "count for ",sys.argv[2].lower(), "=", entry["count"])
                    
    print ("Task finished")        

if __name__ == "__main__":
    main();