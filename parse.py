#coding=utf8

import util
import re, sys, os
import StringIO, codecs
from lxml import etree
from lxml import html as HTML
from crawler import get_html_from_url


# 网易新闻的网页文件的正则表达式
regx_163_page = "http://\w+\.163\.com.*[s]*htm[l]*"

# 网易新闻top新闻的xpath路径
xpath_top_news = "//div[@id='layout-news']/div[2]/div/ul/li/a"

# 标题 【xpath路径、正则表达式】
xpath_title = "//h1[@id='h1title']"

# 发布时间 【xpath路径、正则表达式】
xpath_pub_time = "//div[@id='epContentLeft']/div/div/div"
regx_pub_time = "\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"

# 来源 【xpath路径、正则表达式】
xpath_source = "//div[@id='epContentLeft']/div/div/div/a"

# 内容 【xpath路径、正则表达式】
xpath_content = "//div[@id='endText']/p"

# 获取一个文件名，用于存储下载的数据
def get_file_name():
    today = util.get_today()
    if not os.path.exists(today):
        os.mkdir(today)
    filename = today + os.sep + util.get_now_str() + "_163_top.txt"
    print filename
    return filename



# 解析网易首页的top新闻，并且返回herf列表
def parse_top_news_herf_list(html):
    print "163.parse_top_news->"
    # 根据xpath解析top news的链接和标题
    tree = etree.HTML(html.decode('gbk', 'ignore'))
    top_items = tree.xpath(xpath_top_news)

    string = StringIO.StringIO()
    herf_list = []
    # 对匹配的链接逐个处理
    for top_item in top_items:
        if top_item.text != None:
            href = top_item.get('href')
            if href != None and re.match(regx_163_page, href):
                string.write(top_item.text + "\t" + href + "\n")
                herf_list.append(href)
    recode_top_news(string.getvalue())
    string.close()
    return herf_list


# 将新闻记录到文件中
def recode_top_news(string = ""):
    fd = codecs.open(get_file_name(), 'w+', 'utf-8')
    fd.write(string)
    fd.close()


# 解析herf列表中的所有文章
def get_and_parse_herf_list(herf_list):
    print "get_and_parse_herf_list->"
    for herf in herf_list:
        html = get_html_from_url(herf)
        tree = etree.HTML(html.decode('gbk', 'ignore'))
        try:
            # 获取主题
            title = tree.xpath(xpath_title)[0].text

            # 获取时间
            pub_time_raw = tree.xpath(xpath_pub_time)[0].text
            for match in re.finditer(regx_pub_time, pub_time_raw):
                pub_time = match.group()

            # 获取来源
            source = tree.xpath(xpath_source)[0].text

            #  主体内容
            content = StringIO.StringIO("")
            for section in tree.xpath(xpath_content):
                content.write(section.text)
        except:
            pass
        
        print "herf: ", herf
        print "title: ", title
        print "pub_time: ", pub_time
        print "source: ", source
        print "content: ", content.getvalue()



# 解析url中的top新闻herf列表
def parse_href_list_of_url(url, node):
    print "parse_herf_list_of_url ==> "

    # 记录解析出来的新闻链接列表
    href_list = []
    string = StringIO.StringIO('')

    if node == None:
        print "[Error]: index tag of config.xml error"
        return href_list
    
    # 获取网页内容
    html = get_html_from_url(url)
    try:
        xpath = node.find('xpath').text
        regx_page = node.find('regx_page').text
    except:
        print 'xpath regx_page config of ', url, ' error'
        return href_list

    print "xpath", xpath
    print "regx_page", regx_page

    # 根据xpath解析top news的链接和标题
    doc = HTML.fromstring(html)
    news_items = doc.xpath(xpath)
    print "len: ", len(news_items)

    # 逐个解析
    for news_item in news_items:
        title = news_item.text
        href = news_item.get('href')
        if title != None and re.match(regx_page, href):
            print title, href
            string.write(title + "\t" + href + "\n")
            href_list.append(href)

    # 将结果记录到文件中
    string.close()
    return href_list


# 从源码中获取网页编码格式
def get_charset_of_html(html):
    regx_charset = 'charset[^\w]{1,3}([-\w]+)[^\w]'
    search_info = re.search(regx_charset, html)
    if search_info is not None:
        return search_info.groups(0)[0]
    else:
        return 'gbk'



# 测试解析url中的top新闻herf列表
def test_parse_href_list_of_url(url, node):
    print "parse_herf_list_of_url ==> "

    
    # 记录解析出来的新闻链接列表
    href_list = []
    string = StringIO.StringIO('')

    # 判断配置文件中index相关标签节点是否存在
    if node == None:
        print "[Error]: index tag of config.xml error"
        return href_list
    
    # 获取网页内容
    html = get_html_from_url(url)
    try:
        xpath_list = node.findall('xpath')
        regx_page = node.find('regx_page').text
    except:
        print 'xpath regx_page config of ', url, ' error'
        return href_list

    # 获取网页编码格式，并进行解码 
    charset = get_charset_of_html(html)
    print "charset: ", charset
    html = html.decode(charset, 'ignore')

    print "regx_page", regx_page

    # 根据xpath解析top news的链接和标题
    doc = HTML.fromstring(html)
    for xpath_item in xpath_list:
        xpath = xpath_item.text
        print "xpath: ", xpath
        news_items = doc.xpath(xpath)
        print "len: ", len(news_items)

        # 逐个解析 这个需要两个list，一个记录href 一个记录满足page url格式的
        for news_item in news_items:
            title = news_item.text
            href = news_item.get('href')

            # 判断是否是加粗字体
            print title, href
            if title is not None and re.match(regx_page, href):
                string.write(title + "\t" + href + "\n")
                href_list.append(href)

    # 将结果记录到文件中
    string.close()
    return href_list


# 解析herf列表中的所有文章
def parse_interest_of_herf(herf_list):
    print "get_and_parse_herf_list->"
    for herf in herf_list:
        html = get_html_from_url(herf)
        tree = etree.HTML(html.decode('gbk', 'ignore'))
        try:
            # 获取主题
            title = tree.xpath(xpath_title)[0].text

            # 获取时间
            pub_time_raw = tree.xpath(xpath_pub_time)[0].text
            for match in re.finditer(regx_pub_time, pub_time_raw):
                pub_time = match.group()

            # 获取来源
            source = tree.xpath(xpath_source)[0].text

            #  主体内容
            content = StringIO.StringIO("")
            for section in tree.xpath(xpath_content):
                content.write(section.text)
        except:
            pass
        
        print "herf: ", herf
        print "title: ", title
        print "pub_time: ", pub_time
        print "source: ", source
        print "content: ", content.getvalue()


def parse_content(html, node):
    doc = HTML.fromstring(html.decode('gbk', 'ignore'))
    content = ''

    # 如果配置文件中有xpath，则根据xpath取出内容
    xpath = node.find('xpath')
    if  xpath != None:
        result = doc.xpath(xpath.text)
        if len(result) > 0:
            content = result[0].text

    # 如果配置文件中存在正则表达式，则用正则进行过滤
    regx = node.find('regx')
    if  regx != None:
        result = re.finditer(regx.text, content)
        content = result[0].group()
    print content
    return content

# 从html中解析用户感兴趣的内容
def parse_interest_of_html(html, features):
    interest = ''
    #print html[:500]
    charset = get_charset_of_html(html)
    doc = HTML.fromstring(html.decode(charset, 'ignore'))
    #doc = HTML.fromstring(html)
    
    for key in features.keys():
        print key," : ",
        feature = features[key]
        
        content = ''
        # 根据xpath获取内容
        if feature.get('xpath') is not None:
            for item in doc.xpath(unicode(feature['xpath'])):
                tmp_content = item.text_content().strip()
                content += (tmp_content + '\n')
        else:
            pass
        
        # 根据正则表达式过滤处理
        if feature.get('regx') is not None:
            value = ''
            regx = unicode(feature['regx'])

            #print "type, regx: ", type(regx), "  content: ", type(content)
            
            if feature.get('regx_type', 'search') == 'sub':
                value = re.sub(regx, '', content)
            else:
                match_item = re.search(regx, content)
                if match_item is not None:
                    value = match_item.groups(0)[0].strip()
                #for item in re.finditer(feature['regx'], content.getvalue()):
                #    value = item.group()
            content = value
        else:
            print " ",
        print content
        #interest.write(str(content) + '\t')
    #return interest_content



# 从html中解析用户感兴趣的内容
def test_parse_interest_of_html(html, features):
    interest = ''
    #print html[:500]
    charset = get_charset_of_html(html)
    doc = HTML.fromstring(html.decode(charset, 'ignore'))
    #doc = HTML.fromstring(html)
    
    for key in features.keys():
        print key," : ",
        feature = features[key]
        
        content = StringIO.StringIO('')
        # 根据xpath获取内容
        if feature.get('xpath') is not None:
            for item in doc.xpath(feature['xpath']):
                content.write(item.text_content().strip())
                content.write('\n')
        else:
            pass
        
        # 根据正则表达式过滤处理
        if feature.get('regx') is not None:
            value = ''
            if feature.get('regx_type', 'match') == 'sub':
                value = re.sub(feature['regx'], '', content.getvalue())
            else:
                match_item = re.search(feature['regx'], content.getvalue())
                if match_item is not None:
                    value = match_item.groups(0)[0].strip()
                #for item in re.finditer(feature['regx'], content.getvalue()):
                #    value = item.group()
            content = StringIO.StringIO(value)
        else:
            print " ",
        print content.getvalue()
        #interest.write(str(content) + '\t')
    #return interest_content

# 解析链接列表对应网页中感兴趣的内容
def parse_interest_of_href_list(href_list, node):
    print "parse_interest_of_href_list ==> "

    if node == None:
        print "page tag of config.xml error"
        return None

    # 获取感兴趣的属性字典
    feature_map = {}
    for feature in node.iterchildren():
        tmap = {}
        for child in feature.iterchildren():
            tmap[child.tag] = child.text
        feature_map[feature.tag] = tmap

    
    # 获取待抓取的属性值
    for href in href_list:
        html = get_html_from_url(href)
        if html == '':
            continue
        parse_interest_of_html(html, feature_map)


     
if __name__ == "__main__":
    urllist = ['http://news.163.com/13/0723/11/94FDGUA10001124J.html']
    get_and_parse_herf_list(urllist)
    
