from flask import jsonify, Flask, request
from proxyManager import ProxyManager
app = Flask(__name__)
api_list = {
    'get': u'get an usable proxy',
    'refresh': u'refresh proxy pool',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:5000': u'delete an unable proxy',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/refresh/')
def refresh():
    ProxyManager().refresh()
    return 'success'


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    if proxy:
        return proxy
    return 'failed'


@app.route('/getAll/')
def get_all():
    proxys = ProxyManager().getAll()
    return jsonify(list(proxys))


@app.route('/delete/', methods=['GET'])
def delete():
    # 获取URL链接中的proxy键值对的值
    proxy = request.args.get('proxy')
    print(proxy)
    if proxy:
        ProxyManager().delete(proxy)
        return 'delete success'
    return 'delete failed'


@app.route('/getStatus/')
def get_status():
    status = ProxyManager().getStatus()
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
