#coding=utf8

import re, sys
from lxml import etree as TREE
from crawler import get_html_from_url
from parse import parse_href_list_of_url,parse_interest_of_href_list
from parse import test_parse_href_list_of_url
    

# 解析配置文件
def parse_config(config_path = "config.xml"):
    print "parse_xml ==>  "
    
    fd = open(config_path, 'r')
    doc = TREE.parse(fd)
    for site in doc.xpath('//site'):
        try:
            name = site.find('name').text
            url  = site.find('url').text
            index = site.find('index')
            page = site.find('page')
        except:
            print "error in parse_config()"
            pass

        #  获得site首页中的新闻列表
        href_list = test_parse_href_list_of_url(url, index)

        if len(href_list) == 0:
            print "href list of ", url, " is empty"
            return None
        
        # 对链接列表进行定向抓取
        parse_interest_of_href_list(href_list, page)
        #print dir(page)


            
    fd.close()


if __name__ == "__main__":
    parse_config()
