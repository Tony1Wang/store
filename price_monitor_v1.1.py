from multiprocessing import Process,Pool
import csv
import datetime
import re
import time
import requests
import os

t = datetime.datetime.now().strftime('%Y%m%d%H')
path = 'D:/programs/Price/'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Referer': 'https://www.asus.com.cn/',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'Keep-Alive':'300',
    'Connection':'keep-alive'
}

def write_to_csv(data):
    # csv文件写入链接时需要指定编码格式为utf-8.
    # encoding使用utf-8会乱码，使用utf-8-sig防止乱码
    # 写入指定文件夹方法，文件名前加入路径path
    out = open(path + '%s.csv' % t, 'a', newline='', encoding='utf-8-sig')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(data)

def write(url):
    info = []
    r = requests.get(url,headers=header)
    r.raise_for_status
    r.encoding = r.apparent_encoding
    html = r.text
    try:
        price = re.search(r'<span class="price_box">总计：<span class="price">￥(.*?)</span></span>', html, re.S)
        p = price.group(1)
    except:
        p = 'none'

    try:
        title = re.search(r'<title>(.*?)</title>', html, re.S)
        t = title.group(1)
    except:
        t = 'none'

    try:
        now_time = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
    except:
        now_time = 'none'

    info.append(now_time)
    info.append(t)
    info.append(p)
    info.append(url)
    if info[1] != 'ASUS华硕商城-笔记本、手机、一体机、台式机官方直营':
        print('Run task %s...' % os.getpid())#打印进程
        write_to_csv(info)

if __name__ == '__main__':
    while 1 < 2:
        start = time.time()
        urls = ['https://www.asus.com.cn/store/product-' + '{}.html'.format(str(x)) for x in range(1, 2770)]
        pool = Pool(6)
        pool.map(write,urls) # 注意map函数的第二个参数是urls，list格式
        pool.close()  # 这里的pool.close()是说关闭pool，使其不在接受新的（主进程）任务
        pool.join()  # 这里的pool
        end = time.time()
        print("共计用时%.4f秒"%(end-start))
        time.sleep(3600)
