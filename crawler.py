#coding=utf-8
import lxml.html as HTML
import sys, urllib2,re
from gzip import GzipFile
from StringIO import StringIO
EMPTY = ""


# 从url中获取网页内容
def get_html_from_url(url):
    print "get_html_from_url ==> "
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        fd = opener.open(url, timeout = 50)
    except:
        print url,' can not open, please check'
        return EMPTY
    
    html = fd.read()
    print "url: ", url
    if fd.info().get('content-encoding') == 'gzip':
        print 'content-encodeing is gzip'
        gf = GzipFile(fileobj=StringIO(html), mode="r")
        try:
            html = gf.read()
        except:
            print "except"
            html = gf.extrabuf    
    fd.close()
    return html






# open url and read content
def open_url(url):
    fd = urllib2.urlopen(url, timeout = 10)
    return_code = fd.getcode()

    # check return code, 2XX is right
    if return_code < 200 or return_code >= 300:
        print url,' can not open, please check'
        print "return code is ", return_code


    print dict(fd.headers).get('content-encoding', '') 
    
    # return content of url    
    return str(fd.read())

    
# from head and js part of html
def get_body_from_html(html): 
    body_tag = "<body>"
    if (html != EMPTY and html.find(body_tag) != -1):
        return html[html.index(body_tag) : ]
    return EMPTY


def get_index_of_close_tag(content, tag, index):
    print "index: ", index
    open_tag = "<" + tag
    close_tag = "</" + tag + ">"
    tag_len = len(tag)
    open_tag_len = tag_len + 1
    close_tag_len = tag_len + 3
    content_len = len(content)
    
    # check whether index is position of tag in content
    if (content[index - 1 : index + open_tag_len - 1]) != open_tag:
        return -1
    
    tag_index = index + tag_len
    stack = 0
    found = False

    while True:
        temp_index = content.find(tag, tag_index, content_len)
        print "temp_index ", temp_index
        # not found tag
        if (temp_index == -1):
            break
        else:
            tag_ch = content[temp_index - 1 : temp_index]
            print "tag_ch", tag_ch
            # found open tag
            if ( tag_ch == '<'):
                stack += 1
                
            # found close tag
            elif ( tag_ch == '/'):
                if stack > 0:
                    stack -= 1
                else:
                    found = True
                    break
                
            tag_index = temp_index + tag_len

    if found:
        return content[index - 1 : temp_index + tag_len + 1]
    else:
        return "NOT FOUND"
    

# get top news from content
def get_top_from_163(html):
    if (html == EMPTY):
        return EMPTY

    news_tag = '<span class="tab-hd-con current"><a href="http://news.163.com/">'
    news_index = html.find(news_tag);
    if (news_index == -1):
        print "news_index", news_index
        return EMPTY

    div_tag = '<div class="tab-bd-con current">'
    div_index = html.find(div_tag, news_index)
    if (div_index == -1):
        print "div_index", div_index
        return EMPTY
    
    tag = 'div'
    content = get_index_of_close_tag(html, tag, div_index + 1)
    
    parse_herf(content)
    #print "div part: ", content
    #return content


def parse_herf(html):
    print html
    # html.decode('gbk').encode('utf8')
    soup = BeautifulSoup(html, fromEncoding='gb2312')
    print soup.originalEncoding
    list_herf = soup.findAll('a')

    fd = open("herf.txt", 'w+')
    
    for herf_item in list_herf:
        print herf_item.string, herf_item['href']
        #fd.write(str(herf_item.content()) + "\n")

    fd.close()




# main function
if __name__ == "__main__":

    urls = ['http://www.sina.com.cn', 'http://www.ifeng.com', 'http://www.sohu.com', 'http://www.163.com']
    
    #url = "http://www.sina.com.cn"

    for url in urls:
        html = get_html_from_url(url)
        if (html == EMPTY):
            exit
        print "html length: ", len(html)

    #xPath.parse(html)
    #body = get_body_from_html(html)
    #print "body length: ", len(body)

    #top_content = get_top_from_163(body)
    # print content
    

