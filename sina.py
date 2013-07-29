#coding=utf-8
import lxml.html as HTML
import sys, urllib2
import gzip, re
from gzip import GzipFile
from StringIO import StringIO


reload(sys)
sys.setdefaultencoding('utf-8')


regx_sina_page = "http://\w+\.sina\.com\.cn.*[s]*htm[l]*"

def crawler():
    print "crawler"
    url = "http://www.sina.com.cn"
    fd = urllib2.urlopen(url)

    gf = GzipFile(fileobj=StringIO(fd.read()), mode="r")
    try:
        html = gf.read()
    except:
        print "except"
        html = gf.extrabuf
    #print html[:300]


    doc = HTML.fromstring(html)
    items = doc.xpath("//div[@class='mod06-cont']/ul/li/a")
    
    print len(items)
    #print items[0].text_content()

    for item in items:
        href = item.get('href')
        if item.text != None and re.match(regx_sina_page, href):
            print "==>", item.text, href


def ifeng():
    url = "http://www.sina.com.cn"
    fd = urllib2.urlopen(url)

    gf = GzipFile(fileobj=StringIO(fd.read()), mode="r")
    try:
        html = gf.read()
    except:
        print "except"
        html = gf.extrabuf
    #print html[:300]


    doc = HTML.fromstring(html)
    items = doc.xpath("//div[@class='mod06-cont']/ul/li/a")
    
    print len(items)
    #print items[0].text_content()

    
    for item in items:
        print "==>", item.text, item.get('href')


if __name__ == "__main__":
    crawler()
