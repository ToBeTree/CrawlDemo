from apscheduler.schedulers.blocking import BlockingScheduler
import time
import requests
from multiprocessing import Process
# from getFreeProxy import GetFreeProxy
from mongoClient import MongoDB
from proxyManager import ProxyManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Scheduler(ProxyManager):
    def __init__(self):
        self.ips = 'ips'
        self.useful_ips = 'useful_ips'
        self.db = MongoDB()

    def vaild_ip(self):
        self.db.change_table(self.ips)
        ip = self.db.pop()
        print('%s start vaild ip' % time.time())
        while ip:
            proxies = {"http": "http://{proxy}".format(proxy=ip), "https": "https://{proxy}".format(proxy=ip)
                       }
            try:
                r = requests.get('https://www.baidu.com/',
                                 proxies=proxies, timeout=30, verify=False)
                if r.status_code == 200:
                    self.db.change_table(self.useful_ips)
                    self.db.add(ip)
                    print('%s is pass' % ip)
            except Exception as e:
                print('out %s' % ip)
                pass
            self.db.change_table(self.ips)
            ip = self.db.pop()
        print('%s vaild ip complete' % time.time())


def vaild():
    s = Scheduler()
    s.vaild_ip()
    # 进程不能使用类方法


def main(process_num=10):
    s = Scheduler()
    s.refresh()
    # 进程数组
    procs = []
    for i in range(process_num):
        proc = Process(target=vaild, args=())
        procs.append(proc)

    for i in range(process_num):
        procs[i].start()

    for i in range(process_num):
        procs[i].join()

if __name__ == '__main__':
    main()
    print('main')
    # 设置调度模块，20分钟执行一次
    sche = BlockingScheduler()
    sche.add_job(main, 'interval', minutes=20)
    sche.start()
