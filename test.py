import re, sys
from lxml import etree as TREE
from crawler import get_html_from_url
from lxml import html as HTML
from StringIO import StringIO
from parse import get_charset_of_html

# 解析配置文件
def parse_config(config_path = "config.xml"):
    print "parse_xml ==>  "
    
    html = get_html_from_url("http://finance.sina.com.cn/china/20130727/015816259014.shtml")

    #print html[:600]

    ss = StringIO('')

    charset = get_charset_of_html(html)
    doc = HTML.fromstring(html.decode(charset, 'ignore'))
    
    #doc = HTML.fromstring(html)
    result = doc.xpath('//div[@class="artInfo"]')
    #result = doc.xpath("//div[@id='artibody']/p")
    print "len ", len(result)
    for ret in result: 
        value = ret.text_content().strip()

    regx = '(\d{4}.\d{1,2}.\d{1,2}.*\d{1,2}:\d{1,2})'
    print "时间：", re.search(regx, value).groups(0)[0]

    print value
    regx = u':\d{2}([^\s]*)[\s]*'
    print "来源：", re.search(regx, value).groups(0)[0].strip()



def sohu_test(config_path = 'config.xml'):
    print "sohu_test ==>  "
    
    html = get_html_from_url("http://business.sohu.com/20130727/n382723680.shtml")

    ss = StringIO('')
    doc = HTML.fromstring(html)
    result = doc.xpath("//div[@class='time-source']")
    print "len ", len(result)
    
    for ret in result: 
        value = ret.text_content().strip()
        #value = re.sub('[\r\n]','',value)
    print value

    regx = '(\d{4}.\d{1,2}.\d{1,2}.*\d{1,2}:\d{1,2})'
    print "时间：", re.search(regx, value).groups(0)[0]
    
    regx = u'来源[:：](.*)(作者)*'
    print "时间：", re.search(regx, value).groups(0)[0].strip()


def ifeng_test(config_path = 'config.xml'):
    print "sohu_test ==>  "
    
    html = get_html_from_url("http://news.ifeng.com/society/1/detail_2013_07/27/27973995_0.shtml")
    print html[:800]

    charset = get_charset_of_html(html)
    print "ifeng charset: ", charset
    doc = HTML.fromstring(html.decode(charset, 'ignore'))
    
    ss = StringIO('')
    #doc = HTML.fromstring(html.decode('utf8', 'ignore'))
    #doc = HTML.fromstring(html)
    result = doc.xpath("//div[@id='artical_sth']/p")
    print "len ", len(result)
    
    for ret in result: 
        value = ret.text_content().strip()
        value = re.sub('[\r\n]','',value)
    print value

    regx = '(\d{4}.\d{1,2}.\d{1,2}.*\d{1,2}:\d{1,2})'
    print "时间：", re.search(regx, value).groups(0)[0]

    regx = u'来源[:：]*([^\s]*)[\s]*'
    print "来源：", re.search(regx, value).groups(0)[0].strip()


    xpath_cont = "//div[@id='main_content']/p"
    conts = doc.xpath(xpath_cont)
    if conts is not None:
        for cont in conts:
            value = cont.text_content().strip()
            print value

def net_test(config_path = 'config.xml'):
    print "net_test ==>  "
    
    html = get_html_from_url("http://news.163.com/13/0727/16/94Q724990001124J.html")

    charset = get_charset_of_html(html)
    print "ifeng charset: ", charset
    doc = HTML.fromstring(html.decode(charset, 'ignore'))
    
    ss = StringIO('')
    #doc = HTML.fromstring(html.decode('utf8', 'ignore'))
    #doc = HTML.fromstring(html)
    result = doc.xpath("//div[@class='left']")
    print "len ", len(result)
    
    for ret in result: 
        value = ret.text_content().strip()
        value = re.sub('[\r\n]','',value)
    print value

    regx = '(\d{4}.\d{1,2}.\d{1,2}.*\d{1,2}:\d{1,2})'
    print "时间：", re.search(regx, value).groups(0)[0]

    #regx = u'来源[:：\s]*([^\s]*)[有]*'
    #print "来源：", re.search(regx, value).groups(0)[0].strip()
#regx = u'\d|-|:|(有.*)'
    
    regx = u'来源[:：\s]*([^\s]+)有.*'
    
    print "来源：", re.search(regx, value).groups(0)[0].strip()
    
 
if __name__ == "__main__":
    #net_test()
    #parse_config()
    sohu_test()
    #ifeng_test()

    str1 = '中国'
    str2 = u'中国'

    print type(str1), str1[0:8]
    print type(str2), str2
    
    
