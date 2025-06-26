"""
查询商品信息 模拟高并发测试
"""
import requests
from concurrent.futures import ThreadPoolExecutor
from testTime import testTime

url = 'http://127.0.0.1:9000/api/product/product-info/'


def get_response(i):
    response = requests.get(url, params={"product_name": "iphone"})
    print(f"第{i}次请求结果: {response.json()}")
@testTime
def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(get_response, range(1000))

if __name__ == '__main__':
    main()
