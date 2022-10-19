import requests
import sys
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil import parser
import os
import sqlite3

def convertDate(dts):
    year, month, day = str(parser.parse(dts))[:10].split("-")
    #print(year, month, day)
    dto = datetime.strftime(datetime(int(year), int(month), int(day)), "%Y-%m-%d")
    return dto
    

def getWords(pageno):
    global allLetters, cdate, pans, allword
    proxies = {

    "http": "http://40.67.252.70:8080",

    "https": "https://40.67.252.70:8080",

    }
    URL = "https://www.sbsolver.com/s/"+ str(pageno)     
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    #sys.stdout = f
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    
    #August 1, 2022 
    pats = r"<title>(.*) (.*) (.*) | Spelling Bee Answers | Spelling Bee Solver</title>"
    dts = re.search(pats, r.text).groups()
    cdate = dts[0].split("|")[0]

    
    #matches = re.search(pats,str(soup)).groups()
    #print(matches[0])
    pans = []
    bs_data = BeautifulSoup(r.content,'lxml')
    
    p = bs_data.find_all('span', {'class':"bee-center"})
    #pats = r'<span class=\"bee-center\">(.*)</span>'
    #p = re.findall(pats, r.text)
    
    words = []
    for link in soup.find_all('a'):
        curr = link.get('href')
        if re.match(r"https://www.sbsolver.com/h/",curr):
            word = curr.split("/")[-1]
            words.append(word)
            
        if re.match(r"https://www.sbsolver.com/z/", curr):            
            allLetters = curr.split("/")
            if len(allLetters) == 6:
                allLetters =  allLetters[-2]
            else:
                allLetters =  allLetters[-1] 
    return words 
# end of function get_words


def get_panagram(wrd, letters):
    pan = []
    for w in wrd:
        wc = [a for a in w] 
        if set(wc) == set(letters):
            pan.append(w)
    return pan 



def update_db(dt, c, o, aw, p)       :
    dbname = os.path.join(os.path.dirname(sys.argv[0]), "spell_be.sqlite3")
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
    except Exception as err:
        print(Exception, err)
            
    
    # update game details
    all_word = "_".join(aw)
    panas    = "_".join(p)
    
    sql = '''insert or ignore into game_data (game_date, center, other, panagram, all_words) values(?,?, ?, ?, ?)'''
    params = (dt, c, o, panas, all_word)
    
    try:
        cursor.execute(sql, params)
        conn.commit()
    except Exception as err:
        print("\nFailed to insert row into table game_data:\n" + str(sql))
        print(Exception, err)
    for a in aw:
        sql = "INSERT OR IGNORE INTO words (word) VALUES ('"+ a +"')"

        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as err:
            print("\nFailed to insert row into table game:\n" + str(sql))
            print(Exception, err)
    conn.close()        
# end update db
    
    
    

# begin main section
cdate = ""       
allLetters = ""
allword = []
words = []
pans = []
#f = open('output11.txt','a')
for i in range(1617, 1618):
    curr = getWords(i)
    #words.append(curr)
    '''
    for c in curr:
        f.write(c+"\n")
    '''    
    center = allLetters[0].lower()
    others = allLetters[1:]
    allword = curr
    pans   = get_panagram(allword, center + others) bloof 
    cdo = convertDate(cdate)
    update_db(cdo, center, others, allword, pans)
    print(i)    
# f.close()
# end main section 

#checking for push command after changeing a file.


Checkex.difference(y)
