from mongoClient import MongoDB
from getFreeProxy import GetFreeProxy


class ProxyManager:
    def __init__(self):
        self.ips = 'ips'
        self.useful_ips = 'useful_ips'
        self.db = MongoDB()

    def get(self):
        self.db.change_table(self.useful_ips)
        return self.db.get()

    def getAll(self):
        self.db.change_table(self.useful_ips)
        return self.db.get_all()

    def delete(self, value):
        self.db.change_table(self.useful_ips)
        print('delete %s' % value)
        self.db.delete(value)

    def refresh(self):
        ips = set()
        get = GetFreeProxy()  # 获取类实例
        # 执行类中所有方法
        public_method_names = [method for method in dir(get) if callable(getattr(
            get, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in public_method_names:
            for ip in getattr(get, method)():  # call
                if ip.strip():
                    ips.add(ip.strip())
        self.db.change_table(self.ips)
        print('crawl ips count:%s' % len(ips))
        for ip in ips:
            self.db.add(ip)

    def getStatus(self):
        self.db.change_table(self.ips)
        ips = self.db.get_all()
        self.db.change_table(self.useful_ips)
        useful_ips = self.db.get_all()
        return {'all proxy': ips, 'useful proxy': useful_ips}
if __name__ == '__main__':

    pass
