from multiprocessing import Pool
import csv
import datetime
import re
import time
import requests
import os
import yagmail

t = datetime.datetime.now().strftime('%Y%m%d%H')  # 用来命名csv文件
t1 = datetime.datetime.now().strftime('%Y%m%d')  # 用来命名文件夹

# 将数据转换成字典来对比两个表单的价格
h2 = t
h1 = (str(int(t) - 1))
n = h1 + '.csv'

path = 'D:/programs/Price/'
path1 = os.path.join(path, t1)
if not os.path.isdir(path1):
    os.makedirs(path1)
new_path = 'D:/programs/Price/%s/' % t1

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Referer': 'https://www.asus.com.cn/',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'Keep-Alive': '300',
    'Connection': 'keep-alive'
}


def write_to_csv(data):
    # csv文件写入链接时需要指定编码格式为utf-8.
    # encoding使用utf-8会乱码，使用utf-8-sig防止乱码
    # 写入指定文件夹方法，文件名前加入路径path
    out = open(new_path + '%s.csv' % t, 'a', newline='', encoding='utf-8-sig')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(data)


def write(url):
    info = []
    r = requests.get(url, headers=header)
    r.raise_for_status
    r.encoding = r.apparent_encoding
    html = r.text
    try:
        price = re.search(r'<span class="price_box">总计：<span class="price">￥(.*?)</span></span>', html, re.S)
        p = price.group(1)
    except:
        p = '3333'

    try:
        title = re.search(r'<title>(.*?)</title>', html, re.S)
        tle = title.group(1)
    except:
        tle = '2222'

    try:
        now_time = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
    except:
        now_time = '1111'

    info.append(now_time)
    info.append(tle)
    info.append(p)
    info.append(url)
    if info[1] != 'ASUS华硕商城-笔记本、手机、一体机、台式机官方直营':
        # print('Run task %s...' % os.getpid())  # 打印进程
        write_to_csv(info)


def csv_to_dict(h):
    dictionary = {}
    with open(new_path + '%s.csv' % h, 'r', encoding='gb18030', errors='ignore') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for i in range(len(rows)):
            dict_tony = {rows[i][3]: rows[i][2]}
            dictionary.update(dict_tony)
    return dictionary


def send_email(data):
    yag = yagmail.SMTP("*********@qq.com", '*******', 'smtp.qq.com', 465)
    yag.send(['13764881640@163.com', '619959298@qq.com'], '商品价格异常紧急提醒', data)


if __name__ == '__main__':
    while 1 < 2:
        print("八核齐飞...")
        print(datetime.datetime.now())
        start = time.time()
        urls = ['https://www.asus.com.cn/store/product-' + '{}.html'.format(str(x)) for x in range(1, 2800)]
        pool = Pool(6)
        pool.map(write, urls)  # 注意map函数的第二个参数是urls，list格式
        pool.close()  # 这里的pool.close()是说关闭pool，使其不在接受新的（主进程）任务
        pool.join()  # 这里的pool
        end = time.time()
        print("共计用时%.4f秒" % (end - start))
        if os.path.exists('%s%s' % (new_path, n)):
            print("正在检查价格...")
            dict1 = csv_to_dict(h1)
            dict2 = csv_to_dict(h2)
            for k in dict2:
                if k in dict1:
                    if eval(dict1[k]) != 0:
                        try:
                            pron = (eval(dict1[k]) - eval(dict2[k])) / eval(dict1[k])
                            if pron > 0.25:
                                print(k)
                                send_email(k)
                        except Exception as e:
                            print(e)
            print("检查完毕！")
        time.sleep(3600 - (end - start))
