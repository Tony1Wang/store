之前挂错商品价格，用户低价购买商城产品，导致损失，写个商城所有产品的价格监控，出现价格异常时及时提醒相关运营人员。

·1.0版本，爬取速度过慢，得一个多小时。
![name](https://github.com/Tony1Wang/store/blob/master/pic/1567510580(1).png)


·1.1版本，采用多线程，速度提升明显，毕竟我可是8核齐飞、、、
![name](https://github.com/Tony1Wang/store/blob/master/pic/1567588377(1).png)

·1.1版本同时加入了定时器，定时运行

多进程+定时器，这里遇到好多坑，记录下：
刚开始是想用schedule或者是Timer来弄的，但是总是提示not callable，放弃！！
然后想要windouw任务计划来弄，简单的程序是可以定时运行，但是这个复杂一点的吗也总是各种失败，放弃！！

最后用while 1<2 加上time.sleep，简单搞定。。。
