# from getFreeProxy import GetFreeProxy
# get = GetFreeProxy()

# # 获取类对象中所有可执行的方法
# public_method_names = [method for method in dir(get) if callable(getattr(
#     get, method)) if not method.startswith('_')]  # 'private' methods start from _
# for method in public_method_names:
#     # getattr(x, method)()  # call
#     if method.startswith('parse_haoip'):
#         print('exec')
#         for i in getattr(get, method)():
#             print(i)
#     print(method)
import requests


# ip = '61.153.145.202:25'
# proxies = {"http": "http://{proxy}".format(proxy=ip),
#            "https": "https://{proxy}".format(proxy=ip)}
# r = requests.get('https://www.baidu.com/',
#                  proxies=proxies, timeout=30, verify=False)
# print(r.status_code)
