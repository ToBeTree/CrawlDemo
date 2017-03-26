
from pymongo import MongoClient
import random
# CRUD


class MongoDB:
    """
    封装的Mongodb操作方法
    """

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.database = client['ip_proxy']
        # print(client.database_names())
        self.collection = self.database['ips']
        # self.collection = database['useful_ips']

    def get(self):
        # ip_list = self.get_all()
        # num = random.randint(0,len(ip_list)-1)
        # proxy = ip_list[num]
        # return proxy
        proxy = self.get_all()
        return random.choice(proxy) if proxy else None

    def get_all(self):
        return [p['host'] for p in self.collection.find()]

    def delete(self, value):
        # TODO
        self.collection.remove({'host': value})

    def delete_all(self):
        pass

    def change_table(self, name):
        self.collection = self.database[name]

    def add(self, value):
        # print(self.collection.find_one({'host': 2}))
        if not self.collection.find_one({'host': value}):
            self.collection.insert_one({'host': value})

    def pop(self):
        value = self.get()
        if value:
            self.delete(value)
        return value

if __name__ == '__main__':
    if not None:
        print('f')
    m = MongoDB()
    print(m.add('2'))
    # print(m.pop())
    print(m.delete('2'))
    print(m.get_all())

    # print(m.delete(7))
