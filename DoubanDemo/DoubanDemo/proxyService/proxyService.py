import requests
# import flaskService


class Proxy:
    def __init__(self):
        pass

    def get_proxy(self):
        proxy = requests.get('http://127.0.0.1:5000/get/').content
        if proxy:
            return proxy.decode('utf-8')
        return None

    def delete_proxy(self, proxy):
        if bytes(proxy, encoding='utf8') in self.get_all_proxy():
            requests.get('http://127.0.0.1:5000/delete?proxy={}'.format(proxy))
            return 'success'
        return 'defeat'

    def refresh_proxy(self):
        requests.get('http://127.0.0.1:5000/refresh/')

    def get_all_proxy(self):
        return requests.get('http://127.0.0.1:5000/getAll/').content

if __name__ == '__main__':
    p = Proxy()
    p.delete_proxy('211.54.3.133:3128')