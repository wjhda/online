"""
locust -f locustfile.py
可视化展示高并发请求下的接口情况
"""

from locust import HttpUser, task


class ProductUser(HttpUser):
    @task
    def get_product(self):
        self.client.get("/api/product/product-info/", params={"product_name": "iphone"})
