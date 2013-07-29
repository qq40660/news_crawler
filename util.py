#coding=utf8

from datetime import datetime

# 获取现在的时间，精确到小时
def get_now_of_hour():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

# 获取现在的时间字符串格式
def get_now_str():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M")




# 获取今天的日期，精确到日
def get_today():
    now = datetime.now()
    return now.strftime("%Y%m%d")

if __name__ == "__main__":
    print get_now_of_hour()
    print get_today()
