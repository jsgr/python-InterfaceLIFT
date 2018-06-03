#coding:utf-8
from __future__ import print_function
# 兼容(python3.6 和 python2.7)
try:
    from urllib.request import urlopen, Request
    import queue
except ImportError:
    from urllib2 import urlopen, Request
    import Queue as queue

import os
import sys
import re
import threading
import time


import argparse
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
# print("随机 UserAgent ", ua.random)

import mysql_orm
import py_mongo


# 合并字典
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


HOST = 'http://interfacelift.com'
RES_WIDESCREEN_16_10 = {
    # widescreen 16:10
    '6400x4000': '/wallpaper/downloads/date/wide_16:10/6400x4000/',
    '5120x3200': '/wallpaper/downloads/date/wide_16:10/5120x3200/',
    '3840x2400': '/wallpaper/downloads/date/wide_16:10/3840x2400/',
    '3360x2100': '/wallpaper/downloads/date/wide_16:10/3360x2100/',
    '2880x1800': '/wallpaper/downloads/date/wide_16:10/2880x1800/',
    '2560x1600': '/wallpaper/downloads/date/wide_16:10/2560x1600/',
    '2304x1440': '/wallpaper/downloads/date/wide_16:10/2304x1440/',
    '2048x1280': '/wallpaper/downloads/date/wide_16:10/2048x1280/',
    '1920x1200': '/wallpaper/downloads/date/wide_16:10/1920x1200/',
    '1680x1050': '/wallpaper/downloads/date/wide_16:10/1680x1050/',
    '1440x900': '/wallpaper/downloads/date/wide_16:10/1440x900/',
    '1280x800': '/wallpaper/downloads/date/wide_16:10/1280x800/',
    '1152x720': '/wallpaper/downloads/date/wide_16:10/1152x720/',
    '1024x640': '/wallpaper/downloads/date/wide_16:10/1024x640/',
}
RES_WIDESCREEN_16_9 = {
    # widescreen 16:9
    '5120x2880': '/wallpaper/downloads/date/wide_16:9/5120x2880/',
    '4096x2304': '/wallpaper/downloads/date/wide_16:9/4096x2304/',
    '3840x2160': '/wallpaper/downloads/date/wide_16:9/3840x2160/',
    '3200x1800': '/wallpaper/downloads/date/wide_16:9/3200x1800/',
    '2880x1620': '/wallpaper/downloads/date/wide_16:9/2880x1620/',
    '2560x1440': '/wallpaper/downloads/date/wide_16:9/2560x1440/',
    '1920x1080': '/wallpaper/downloads/date/wide_16:9/1920x1080/',
    '1600x900': '/wallpaper/downloads/date/wide_16:9/1600x900/',
    '1366x768': '/wallpaper/downloads/date/wide_16:9/1366x768/',
    '1280x720': '/wallpaper/downloads/date/wide_16:9/1280x720/',
}
RES_WIDESCREEN_21_9 = {
    # widescreen 21:9
    '6400x3600': '/wallpaper/downloads/date/wide_21:9/6400x3600/',
    '3440x1440': '/wallpaper/downloads/date/wide_21:9/3440x1440/',
    '2560x1080': '/wallpaper/downloads/date/wide_21:9/2560x1080/',
}
RES_DUAL_MONITORS = {
    # dual monitors
    '5120x1600': '/wallpaper/downloads/date/2_screens/5120x1600/',
    '5120x1440': '/wallpaper/downloads/date/2_screens/5120x1440/',
    '3840x1200': '/wallpaper/downloads/date/2_screens/3840x1200/',
    '3840x1080': '/wallpaper/downloads/date/2_screens/3840x1080/',
    '3360x1050': '/wallpaper/downloads/date/2_screens/3360x1050/',
    '3200x1200': '/wallpaper/downloads/date/2_screens/3200x1200/',
    '2880x900': '/wallpaper/downloads/date/2_screens/2880x900/',
    '2560x1024': '/wallpaper/downloads/date/2_screens/2560x1024/',
}
RES_TRIPLE_MONITORS = {
    # triple monitors
    '7680x1600': '/wallpaper/downloads/date/3_screens/7680x1600/',
    '7680x1440': '/wallpaper/downloads/date/3_screens/7680x1440/',
    '5760x1200': '/wallpaper/downloads/date/3_screens/5760x1200/',
    '5760x1080': '/wallpaper/downloads/date/3_screens/5760x1080/',
    '5040x1050': '/wallpaper/downloads/date/3_screens/5040x1050/',
    '4800x1200': '/wallpaper/downloads/date/3_screens/4800x1200/',
    '4800x900': '/wallpaper/downloads/date/3_screens/4800x900/',
    '4320x900': '/wallpaper/downloads/date/3_screens/4320x900/',
    '4200x1050': '/wallpaper/downloads/date/3_screens/4200x1050/',
    '4096x1024': '/wallpaper/downloads/date/3_screens/4096x1024/',
    '3840x1024': '/wallpaper/downloads/date/3_screens/3840x1024/',
    '3840x960': '/wallpaper/downloads/date/3_screens/3840x960/',
    '3840x720': '/wallpaper/downloads/date/3_screens/3840x720/',
    '3072x768': '/wallpaper/downloads/date/3_screens/3072x768/',
}
RES_IPHONE = {
    # iPhone
    'iphone_x': '/wallpaper/downloads/date/iphone/iphone_x/',
    'iphone_6_7_8_plus': '/wallpaper/downloads/date/iphone/iphone_6,_7,_8_plus/',
    'iphone_6_7_8': '/wallpaper/downloads/date/iphone/iphone_6,_7,_8/',
    'iphone_5_5s_5c': '/wallpaper/downloads/date/iphone/iphone_5,_5s,_5c/',
    'iphone_4_4s': '/wallpaper/downloads/date/iphone/iphone_4,_4s/',
    'iphone_3g_3gs': '/wallpaper/downloads/date/iphone/iphone,_3g,_3gs/',
}
RES_IPAD = {
    # iPad
    'ipad_pro_(12.9)': '/wallpaper/downloads/date/ipad/ipad_pro_(12.9)/',
    'ipad_pro_(10.5)': '/wallpaper/downloads/date/ipad/ipad_pro_(10.5)/',
    'ipad_air_4_3_retina_mini': '/wallpaper/downloads/date/ipad/ipad_air,_4,_3,_retina_mini/',
    'ipad_mini_ipad_1,_2': '/wallpaper/downloads/date/ipad/ipad_mini,_ipad_1,_2/',
}
RES_ANDROID = {
    # android
    '1080x1920_phone': '/wallpaper/downloads/date/android/1080x1920_phone/',
    '720x1280_phone': '/wallpaper/downloads/date/android/720x1280_phone/',
    '480x854_phone': '/wallpaper/downloads/date/android/480x854_phone/',
    '480x800_phone': '/wallpaper/downloads/date/android/480x800_phone/',
    '1280x800_tablet': '/wallpaper/downloads/date/android/1280x800_tablet/',
}

# 添加 壁纸路径
RES_PATHS = merge_dicts(
    RES_WIDESCREEN_16_10,
    RES_WIDESCREEN_16_9,
    RES_WIDESCREEN_21_9,
    RES_DUAL_MONITORS,
    RES_TRIPLE_MONITORS,
    RES_IPHONE,
    RES_IPAD,
    RES_ANDROID
)

# 提取图片路径
IMG_PATH_PATTERN = re.compile(r'<a href=\"(?P<path>.+)\"><img.+?src=\"/img_NEW/button_download')
IMG_FILE_PATTERN = re.compile(r'[^/]*$')


# 下载指定的url并将它写入指定目录中
def download_file(url, saveDir):
    print("TABLES", TABLES)
    print("下载指定的url并将它写入指定目录中", url, saveDir)

    data = {
        'proportion': args.resolution,
        'url': url,
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    print("要写入的表", TABLES)
    print("要写入的数据", data)

    # 写入mongodb数据库
    mongo_obj = py_mongo.Mongo()
    mongo_obj.add_one(TABLES, data)

    # 写入mysql数据库
    mysql_obj = mysql_orm.MysqlOrmInit()
    if TABLES == 'RES_WIDESCREEN_16_9':
        TABLES_table = mysql_orm.RES_WIDESCREEN_16_9
    elif TABLES == 'RES_WIDESCREEN_16_10':
        TABLES_table = mysql_orm.RES_WIDESCREEN_16_10
    elif TABLES == 'RES_WIDESCREEN_21_9':
        TABLES_table = mysql_orm.RES_WIDESCREEN_21_9
    elif TABLES == 'RES_DUAL_MONITORS':
        TABLES_table = mysql_orm.RES_DUAL_MONITORS
    elif TABLES == 'RES_TRIPLE_MONITORS':
        TABLES_table = mysql_orm.RES_TRIPLE_MONITORS
    elif TABLES == 'RES_IPHONE':
        TABLES_table = mysql_orm.RES_IPHONE
    elif TABLES == 'RES_IPAD':
        TABLES_table = mysql_orm.RES_IPAD
    elif TABLES == 'RES_ANDROID':
        TABLES_table = mysql_orm.RES_ANDROID

    mysql_obj.add_one(TABLES_table, data)

    headers = {
        'User-Agent': ua.random,
        'Referer': url}
    # 构造请求
    req = Request(url, None, headers)
    # 文件名字
    filename = IMG_FILE_PATTERN.search(url).group()
    print("文件名字", filename)
    # 保存路径
    saveFile = os.path.join(saveDir, filename)
    print("保存路径", saveFile)
    if DOWNLOAD == 'y':
        with open(saveFile, 'wb') as f:
            try:
                # 获取请求之后的返回值
                res = urlopen(req)
                print("获取请求之后的返回值", res)
                # 保存文件
                f.write(res.read())
                # 打印日志
                print('下载 %s' % filename)
            except Exception as e:
                print("下载失败 %s" % e)
                try:
                    os.remove(saveFile)
                except:
                    pass


# 下载壁纸url队列
def download_worker():
    while True:
        url = queue.get()
        download_file(url, SAVE_DIR)
        queue.task_done()


# 返回指定页码的路径
def get_page_path(pageNumber):
    print("返回指定页码的路径", '%sindex%d.html' % (RES_PATH, pageNumber))
    return '%sindex%d.html' % (RES_PATH, pageNumber)


# 返回指定路径的完整的URL
def get_url_from_path(path):
    print("返回指定路径的完整的URL", '%s/%s' % (HOST, path))
    return '%s/%s' % (HOST, path)


# 返回指定页码的完整的URL
def get_page_url(pageNumber):
    complete_url = get_url_from_path(get_page_path(pageNumber))
    print("返回指定页码的完整的URL", complete_url)
    return complete_url


# 判断下一页是否存在,存在返回True,不存在返回False
def has_next_page(pageContent, currentPage):
    print("判断下一页是否存在,存在返回True,不存在返回False")
    return True if pageContent.find(get_page_path(currentPage + 1)) > -1 else False


# 打开指定的页面,返回页面的HTML内容
def open_page(pageNumber):
    # 获取完整的url
    url = get_page_url(pageNumber)
    print("获取完整的url", url)
    headers = {'User-Agent': ua.random,
               'Referer': url}
    try:
        # 构造请求
        req = Request(url, None, headers)
        # 发起请求
        f = urlopen(req)
    except IOError as e:
        print("无法打开页面", url)
        if hasattr(e, 'code'):
            print('错误代码', e.code)
    return f.read().decode(errors='ignore')


# 返回指定的秒数在H:MM:SS格式
def pretty_time(seconds):
    m, s = divmod(round(seconds), 60)
    h, m = divmod(m, 60)
    print("返回指定的秒数在H:MM:SS格式", "%d:%02d:%02d" % (h, m, s))
    return "%d:%02d:%02d" % (h, m, s)


# 打印列表支持的下载参数
def print_resolution_list():
    print('\n[Widescreen 16:10]')
    print(', '.join(key for key in RES_WIDESCREEN_16_10))
    print('\n[Widescreen 16:9]')
    print(', '.join(key for key in RES_WIDESCREEN_16_9))
    print('\n[Widescreen 21:9]')
    print(', '.join(key for key in RES_WIDESCREEN_21_9))
    print('\n[Dual Monitors]')
    print(', '.join(key for key in RES_DUAL_MONITORS))
    print('\n[Triple Monitors]')
    print(', '.join(key for key in RES_TRIPLE_MONITORS))
    print('\n[iPhone resolutions]')
    print(', '.join(key for key in RES_IPHONE))
    print('\n[iPad resolutions]')
    print(', '.join(key for key in RES_IPAD))
    print('\n[android]')
    print(', '.join(key for key in RES_ANDROID))


# 验证参数
def validate_args(parser, args):
    if args.list:
        print('可用的决议:')
        print_resolution_list()
        sys.exit(0)
    if args.resolution not in list(RES_PATHS.keys()):
        print('指定的分辨率无效 (%s)' % args.resolution)
        print('可用的分辨率如下:  %s --list' % os.path.basename(__file__))
        sys.exit(1)


# 打印开始脚本的变量
def print_starting_vars():
    print('选择的分辨率: %s' % args.resolution)
    print('目标目录: %s' % SAVE_DIR)
    print('线程: %s' % THREADS)

    if OVERWRITE:
        print('覆盖:启用')


# 解析参数
parser = argparse.ArgumentParser(description='从interfacelift.com下载壁纸')
parser.add_argument('-down', help='是否下载到本地，默认否', default='y')
parser.add_argument('resolution', nargs='?', help='解析下载(默认值:1920 x1080)', default='1920x1080')
parser.add_argument('-d', '--dest', help='下载目录 (默认: ./wallpapers)', default='wallpapers/1920x1080')
parser.add_argument('-t', '--threads', help='使用线程的数量 (默认: 4)', default=4, type=int)
parser.add_argument('-o', '--overwrite', help='覆盖同名文件 (默认: 不覆盖)', action='store_true')
parser.add_argument('-l', '--list', help='可用的下载列表', action='store_true')
parser.add_argument('-table', help='数据库', default='RES_WIDESCREEN_16_9')
args = parser.parse_args()
validate_args(parser, args)

# 初始化变量
RES_PATH = RES_PATHS[args.resolution]
SAVE_DIR = args.dest
THREADS = args.threads
OVERWRITE = args.overwrite
TABLES = args.table
DOWNLOAD = args.down
print_starting_vars()

# 如果不存在创建目录
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

#队列
queue = queue.Queue();
#开始计时
timeStart = time.time()

# 创建线程
for i in range(THREADS):
    t = threading.Thread(target=download_worker)
    t.daemon = True
    t.start()

# 添加图片url到队列中
page = 1
count = 0
while True:
    pageContent = open_page(page)
    links = IMG_PATH_PATTERN.finditer(pageContent)
    for link in links:
        url = get_url_from_path(link.group('path'))
        filename = IMG_FILE_PATTERN.search(url).group()
        saveFile = os.path.join(SAVE_DIR, filename)

        if OVERWRITE or not os.path.isfile(saveFile):
            queue.put(url)
            count += 1
        else:
            print('跳过 %s (已经存在)' % filename)

    # 如果没有下一页
    if has_next_page(pageContent, page):
        page += 1
    else:
        break

# 阻塞,直到所有url处理
queue.join()
print('下载完成 (%d 文件)' % count)
print('时间：%s' % pretty_time(time.time() - timeStart))
